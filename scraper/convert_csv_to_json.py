import csv
import json
from collections import defaultdict

CSV_PATH = "../tier1-map/tier1_events.csv"
JSON_PATH = "../tier1-map/state_scores.json"

score_by_state = defaultdict(int)

try:
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = row["state"]
            weight = int(row.get("weight", 1))
            score_by_state[state] += weight
except FileNotFoundError:
    print("tier1_events.csv not found.")

with open(JSON_PATH, "w") as f:
    json.dump(score_by_state, f, indent=2)

print(f"State scores written to {JSON_PATH}")