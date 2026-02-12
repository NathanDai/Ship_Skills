---
name: Vesselfinder Ship Details
description: Extract ship details (Name, Type, Flag, GT, DWT, etc.) from Vesselfinder using IMO number.
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

The output is a JSON object with the following fields:

- `imo`: The IMO number of the ship.
- `name`: The name of the ship.
- `vessel_type`: Type of the vessel (e.g., "Offshore Support Vessel").
- `flag`: The flag under which the ship sails.
- `gross_tonnage`: Gross Tonnage.
- `summer_deadweight`: Summer Deadweight in tonnes.
- `length_overall`: Length Overall in meters.
- `year_of_built`: Year the ship was built.

### Dependencies

- python3
- requests
- beautifulsoup4

To install dependencies:

```bash
pip install requests beautifulsoup4
```
