---
name: weather
description: Query current weather for a specific city
---

# Weather Skill

This skill allows you to query the current weather conditions for a specified city.

## Usage

You can use the python script directly from the command line.

### Prerequisites

- Python 3.7+
- `httpx` library installed (`pip install httpx`)

### Commands

Run the script with the city name as an argument:

```bash
python3 scripts/weather_skill.py <city_name>
```

**Example:**

```bash
python3 scripts/weather_skill.py Beijing
```

## Output

The script returns a JSON-like dictionary containing:
- City name
- Temperature (°C)
- Weather description
- Humidity
- Wind speed
