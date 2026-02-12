---
name: Vesselfinder Ship Details
description: Extract specific ship details (Name, Type, Flag, Dimensions, Tonnages, Voyage Info, Last Port, etc.) from Vesselfinder using IMO number.
---

# Vesselfinder Ship Details Skill

This skill allows you to extract detailed information about a ship from Vesselfinder using its IMO number.

## Usage

The skill provides a Python script `scripts/get_ship_details.py` that takes an IMO number as an argument and outputs the ship details in JSON format.

### Command

```bash
python3 scripts/get_ship_details.py <IMO_NUMBER>
```

### Example

```bash
python3 scripts/get_ship_details.py 9648714
```

### Output Format

The output is a JSON object containing **only the available fields** from the following allowed list:

- `imo`: The IMO number of the ship.
- `name`: The name of the ship.
- `vessel_type`: Type of the vessel.
- `flag`: The flag under which the ship sails.
- `mmsi`: Maritime Mobile Service Identity.
- `call_sign`: Call Sign.
- `ais_type`: AIS Vessel Type.
- `gross_tonnage`: Gross Tonnage.
- `summer_deadweight`: Summer Deadweight in tonnes.
- `length_overall`: Length Overall in meters.
- `beam`: Beam in meters.
- `year_of_built`: Year the ship was built.
- `destination`: The ship's reported destination.
- `eta`: Estimated Time of Arrival.
- `last_port`: The last port visited.
- `atd`: Actual Time of Departure.

**Note:** Fields that are empty, null, or restricted (marked with `-`) are omitted from the output.

### Dependencies

- python3
- requests
- beautifulsoup4

To install dependencies:

```bash
pip install requests beautifulsoup4
```
