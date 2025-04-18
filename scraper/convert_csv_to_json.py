import csv
import json
from collections import defaultdict

CSV_PATH = "../tier1-map/tier1_events.csv"
JSON_PATH = "../tier1-map/state_scores.json"

# Full name to abbreviation mapping
state_abbr = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

score_by_abbr = defaultdict(int)

try:
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            full_name = row["state"]
            weight = int(row.get("weight", 1))
            abbr = state_abbr.get(full_name)
            if abbr:
                score_by_abbr[abbr] += weight
            else:
                print(f"Unknown state: {full_name}")
except FileNotFoundError:
    print("tier1_events.csv not found.")

with open(JSON_PATH, "w") as f:
    json.dump(score_by_abbr, f, indent=2)

print(f"State scores written to {JSON_PATH}")