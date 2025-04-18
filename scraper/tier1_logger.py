
import feedparser
import csv
import json
from datetime import datetime

# Load rules from JSON file
with open("tier1_rules.json", "r") as f:
    TIER1_RULES = json.load(f)

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming"
]

RSS_FEEDS = {
    "NPR": "https://www.npr.org/rss/rss.php?id=1001",
    "ProPublica": "https://www.propublica.org/feeds/articles"
}

OUTPUT_FILE = "../tier1-map/tier1_events.csv"
START_DATE = datetime(2025, 1, 25)

def extract_state(text):
    for state in US_STATES:
        if state.lower() in text.lower():
            return state
    return "Federal"

def parse_feed(name, url):
    feed = feedparser.parse(url)
    entries = []

    for entry in feed.entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        link = entry.get("link", "")
        published = entry.get("published", "") or entry.get("updated", "")
        pub_date = None

        try:
            pub_date = datetime.strptime(published[:16], "%a, %d %b %Y")
        except:
            try:
                pub_date = datetime.strptime(published[:10], "%Y-%m-%d")
            except:
                print("[⚠️] Failed to parse date:", published)
                continue

        if pub_date < START_DATE:
            continue

        full_text = (title + " " + summary).lower()

        for rule_name, rule_data in TIER1_RULES.items():
            match_count = sum(1 for kw in rule_data["keywords"] if kw in full_text)
            if match_count >= rule_data["required"]:
                print(f"[✅ MATCH] Rule: {rule_name} | Title: {title}")
                state = extract_state(full_text)
                entries.append({
                    "date": pub_date.strftime("%Y-%m-%d"),
                    "phrase": rule_name,
                    "state": state,
                    "source": name,
                    "url": link,
                    "weight": 1
                })
                break  # avoid double logging same entry
    return entries

def write_to_csv(entries):
    if not entries:
        print("No new matches found.")
        return
    with open(OUTPUT_FILE, "a", newline="") as csvfile:
        fieldnames = ["date", "phrase", "state", "source", "url", "weight"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for entry in entries:
            writer.writerow(entry)
    print(len(entries), "new entries written to", OUTPUT_FILE)

def run():
    all_entries = []
    for name, url in RSS_FEEDS.items():
        entries = parse_feed(name, url)
        all_entries.extend(entries)
    write_to_csv(all_entries)

if __name__ == "__main__":
    run()
