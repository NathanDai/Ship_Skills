import sys
import json
import requests
import argparse


def search_vessel(vessel_name):
    url = "http://172.16.28.22:3000/rest/vesselfinder/get_vesselfinder_by_name"
    headers = {"Content-Type": "application/json"}
    payload = {"vessel_name": vessel_name}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for vessel details by name.")
    parser.add_argument("vessel_name", help="The name of the vessel to search for.")
    args = parser.parse_args()

    result = search_vessel(args.vessel_name)
    if result:
        print(json.dumps(result.get("data", []), indent=2, ensure_ascii=False))
    else:
        sys.exit(1)
