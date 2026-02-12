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
        "year_of_built": None,
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
    ship_data["vessel_type"] = technical_specs.get("ship type")

    # Flag
    ship_data["flag"] = technical_specs.get("flag")

    # Gross Tonnage
    ship_data["gross_tonnage"] = technical_specs.get("gross tonnage")

    # Summer Deadweight
    ship_data["summer_deadweight"] = technical_specs.get("deadweight (t)")

    # Length Overall
    if "length overall (m)" in technical_specs:
        ship_data["length_overall"] = technical_specs.get("length overall (m)")
    elif "length overall (m) / beam (m)" in technical_specs:
        ship_data["length_overall"] = (
            technical_specs.get("length overall (m) / beam (m)").split("/")[0].strip()
        )

    # Year of Built
    ship_data["year_of_built"] = technical_specs.get("year of build")

    # Correction: IMO is often part of a combined field or separate.
    # Since we passed IMO, we keep it.
    # But we can verify if "imo / mmsi" contains it.

    return ship_data


def main():
    parser = argparse.ArgumentParser(description="Fetch ship details from VesselFinder")
    parser.add_argument("imo", help="The IMO number of the ship")
    args = parser.parse_args()

    data = get_ship_details(args.imo)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
