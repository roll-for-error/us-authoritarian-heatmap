import feedparser
import csv
from datetime import datetime
import re

# Tier 1 phrases (simplified example - you can expand this)
TIER1_PHRASES = [
    "eliminate DEI",
    "restore merit-based hiring",
    "ban critical race theory",
    "end equity-related grants or contracts",
    "rescind DEI in education",
    "eliminate environmental justice offices",
    "end DEI programs in the military",
    "revoke federal DEI guidelines"
]

# US states for detection
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

# Sources
RSS_FEEDS = {
    "NPR": "https://www.npr.org/rss/rss.php?id=1001",
    "ProPublica": "https://www.propublica.org/feeds/articles"
}

# Output file
OUTPUT_FILE = "../tier1-map/tier1_events.csv"

# Only consider articles from Jan 25, 2025 onwards
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
        try:
            pub_date = datetime.strptime(published[:16], "%a, %d %b %Y")
        except:
            continue
        if pub_date < START_DATE:
            continue
        for phrase in TIER1_PHRASES:
            if phrase.lower() in title.lower() or phrase.lower() in summary.lower():
                state = extract_state(title + " " + summary)
                entries.append({
                    "date": pub_date.strftime("%Y-%m-%d"),
                    "phrase": phrase,
                    "state": state,
                    "source": name,
                    "url": link,
                    "weight": 1
                })
                break
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
    print(f"{len(entries)} new entries written to {OUTPUT_FILE}.")

def run():
    all_entries = []
    for name, url in RSS_FEEDS.items():
        entries = parse_feed(name, url)
        all_entries.extend(entries)
    write_to_csv(all_entries)

if __name__ == "__main__":
    run()