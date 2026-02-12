import requests
from bs4 import BeautifulSoup
import argparse
import json
import sys


def get_ship_details(imo):
    url = f"https://www.vesselfinder.com/vessels/details/{imo}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    # Default values
    ship_data = {
        "imo": imo,
        "name": None,
        "vessel_type": None,
        "flag": None,
        "gross_tonnage": None,
        "summer_deadweight": None,
        "length_overall": None,
        "beam": None,
        "year_of_built": None,
        "ais_type": None,
        "mmsi": None,
        "call_sign": None,
        "destination": None,
        "eta": None,
        "last_port": None,
        "atd": None,
    }

    # Extract Name
    title_section = soup.find("h1", class_="title")
    if title_section:
        ship_data["name"] = title_section.text.strip()

    # If name not found in h1, try to find it in the breadcrumb or other places
    if not ship_data["name"]:
        # Fallback to page title
        if soup.title:
            title_text = soup.title.text
            # Title format: "SHIP NAME, Ship Type - Details and current position - IMO 1234567 - VesselFinder"
            parts = title_text.split(",")
            if parts:
                ship_data["name"] = parts[0].strip()

    # Extract Voyage Data (Destination, ETA, Last Port, ATD)
    voyage_rows = soup.find_all("div", class_="vi__r1")
    for row in voyage_rows:
        label_div = row.find("div", class_="vilabel")
        if not label_div:
            continue

        label_text = label_div.text.strip().lower()

        # Destination & ETA
        if "destination" in label_text:
            dest_elem = row.find("a", class_="_npNa")
            if dest_elem:
                ship_data["destination"] = dest_elem.text.strip()

            eta_elem = row.find("div", class_="_value")
            if eta_elem:
                eta_span = eta_elem.find("span", class_="_mcol12")
                if eta_span:
                    eta_text = eta_span.text.strip()
                    if eta_text.upper().startswith("ETA:"):
                        ship_data["eta"] = eta_text[4:].strip()
                    else:
                        ship_data["eta"] = eta_text

        # Last Port & ATD
        elif "last port" in label_text:
            port_elem = row.find("a", class_="_npNa")
            if port_elem:
                ship_data["last_port"] = port_elem.text.strip()

            atd_elem = row.find("div", class_="_value")
            if atd_elem:
                # The text might contain "ATD: Feb 11, 03:28 UTC" and a span like "(1 day ago)"
                # We want just the text before the span, or the full text minus known prefixes
                # Let's get the full text first
                full_atd_text = atd_elem.get_text(
                    " ", strip=True
                )  # "ATD: Feb 11, 03:28 UTC (1 day ago)"

                # Check for "ATD:" prefix
                if "ATD:" in full_atd_text:
                    # simplistic parsing: split by "ATD:" and take the second part
                    atd_val = full_atd_text.split("ATD:")[1].strip()
                    # Remove the relative time in parens if present, e.g. "(1 day ago)"
                    if "(" in atd_val:
                        atd_val = atd_val.split("(")[0].strip()
                    ship_data["atd"] = atd_val

    # Parsers for the "Vessel Particulars" section
    # This section usually contains a table with keys and values
    # Based on observation, keys are often in 'td.tpc1' or similar, values in 'td.txv' or 'td.tpc2'
    # Use a generic approach to find the table rows and map keys to our fields

    technical_specs = {}

    # Look for all tables and rows
    rows = soup.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            key = cols[0].text.strip().lower().rstrip(":")
            value = cols[1].text.strip()
            technical_specs[key] = value

    # Map extracted specs to our ship_data
    # Common keys: "imo / mmsi", "call sign", "flag", "gross tonnage", "summer deadweight (t)", "length overall (m) / beam (m)", "year of built", "vessel type"

    # Debug: print found keys
    # print(f"Found keys: {list(technical_specs.keys())}", file=sys.stderr)

    # Vessel Type
    ship_data["vessel_type"] = technical_specs.get("ship type") or technical_specs.get(
        "vessel type"
    )

    # Flag
    ship_data["flag"] = technical_specs.get("flag")

    # MMSI & Call Sign
    # "imo / mmsi" -> "9333395 / 255806256"
    imo_mmsi = technical_specs.get("imo / mmsi")
    if imo_mmsi:
        parts = imo_mmsi.split("/")
        if len(parts) > 1:
            ship_data["mmsi"] = parts[1].strip()

    ship_data["call_sign"] = technical_specs.get("callsign") or technical_specs.get(
        "call sign"
    )

    # Gross Tonnage
    ship_data["gross_tonnage"] = technical_specs.get("gross tonnage")

    # Summer Deadweight
    ship_data["summer_deadweight"] = technical_specs.get(
        "deadweight (t)"
    ) or technical_specs.get("summer deadweight (t)")

    # Length Overall
    if "length overall (m)" in technical_specs:
        ship_data["length_overall"] = technical_specs.get("length overall (m)")
    elif "length overall (m) / beam (m)" in technical_specs:
        ship_data["length_overall"] = (
            technical_specs.get("length overall (m) / beam (m)").split("/")[0].strip()
        )

    # Beam
    if "beam (m)" in technical_specs:
        ship_data["beam"] = technical_specs.get("beam (m)")
    elif "length overall (m) / beam (m)" in technical_specs:
        parts = technical_specs.get("length overall (m) / beam (m)").split("/")
        if len(parts) > 1:
            ship_data["beam"] = parts[1].strip()

    # Year of Built
    ship_data["year_of_built"] = technical_specs.get(
        "year of build"
    ) or technical_specs.get("year of built")

    # AIS Info
    ship_data["ais_type"] = technical_specs.get("ais type")

    # Correction: IMO is often part of a combined field or separate.
    # Since we passed IMO, we keep it.
    # But we can verify if "imo / mmsi" contains it.

    # Filter out empty, None, or restricted ("-") values and return
    # final_ship_data = {
    #     k: v
    #     for k, v in ship_data.items()
    #     if v is not None and v != "-" and (isinstance(v, str) and v.strip() != "" or not isinstance(v, str))
    # }

    # User requested strict output format + voyage data
    allowed_keys = {
        "imo",
        "name",
        "vessel_type",
        "flag",
        "gross_tonnage",
        "summer_deadweight",
        "length_overall",
        "beam",
        "year_of_built",
        "ais_type",
        "mmsi",
        "call_sign",
        "destination",
        "eta",
        "last_port",
        "atd",
    }

    final_ship_data = {
        k: v
        for k, v in ship_data.items()
        if k in allowed_keys
        and v
        and v != "-"
        and (isinstance(v, str) and v.strip() != "" or not isinstance(v, str))
    }

    return final_ship_data


def main():
    parser = argparse.ArgumentParser(description="Fetch ship details from VesselFinder")
    parser.add_argument("imo", help="The IMO number of the ship")
    args = parser.parse_args()

    data = get_ship_details(args.imo)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
