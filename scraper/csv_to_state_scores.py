import csv
import json
from collections import defaultdict

CSV_PATH = 'tier1-map/tier1_events.csv'
JSON_PATH = 'tier1-map/state_scores.json'

def convert_csv_to_state_scores():
    scores = defaultdict(int)
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = row["state"]
            weight = int(row.get("weight", 1))
            scores[state] += weight
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

if __name__ == "__main__":
    convert_csv_to_state_scores()