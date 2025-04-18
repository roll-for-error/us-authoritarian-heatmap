
import feedparser
import csv
from datetime import datetime
import re

TIER1_PHRASES = ['abolish FINRA and PCAOB; fold into SEC', 'abolish the Federal Reserve (proposed)', 'ban gender identity language in policy', 'bar mixed-status families from federal programs', 'centralize Medicaid oversight under state block-style grants', 'centralize immigration enforcement under federal control', 'defund foreign aid that promotes equity, LGBTQ+, or climate justice', 'defund oversight programs', 'dismantle DEI scorecards, dashboards, and committees', 'eliminate Climate Strategy and climate-related offices', 'eliminate DEI departments, infrastructure, and language', 'eliminate asylum pathways including parole, TPS, and DACA-style discretion', 'eliminate gender-based mandates in aid and health', 'eliminate independent agencies and commissions', 'eliminate judicial review for removal or asylum', 'exclude gender-diverse imagery in government communications', 'expand ICE enforcement zones nationwide', 'install pro-life leadership in health and gender policy', 'mandate E-Verify for all federal contractors', 'mandate prosecution for federal violations aligned with administration ideology', 'prohibit Notices to Report and federal migrant travel', 'prohibit abortion training without opt-in conscience clauses', 'prohibit education on gender identity and sexual orientation', 'propose gold standard and “free banking” alternatives to Federal Reserve', 'redefine “gender equality” to mean support for cisgender women', 'reinstate Remain in Mexico and Asylum Cooperative Agreements', 'remove DEI from all systems, websites, publications', 'remove LGBTQ+ references from government programs', 'remove protections for immigrant children, LGBTQ+ asylum seekers', 'rename DEI offices to “Women, Children, and Families”', 'repeal civil rights statutes and financial oversight mechanisms', 'repeal mandates advancing DEI or reproductive equity', 'repeal waivers enabling environmental or social healthcare spending', 'rescind ACA mandates on contraception and abortion', 'rescind Ryan White HIV/AIDS guidance supporting gender-affirming care', 'restrict access to contraception, emergency contraception', 'restrict prosecutorial discretion (esp. immigration)', 'revoke funding from progressive-aligned nonprofits', 'revoke prosecutorial discretion for immigration enforcement', 'subject nonprofit grantees to loyalty vetting']

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
        try:
            pub_date = datetime.strptime(published[:16], "%a, %d %b %Y")
        except:
            continue
        if pub_date < START_DATE:
            continue
        full_text = (title + " " + summary).lower()
        for phrase in TIER1_PHRASES:
            if phrase.lower() in full_text:
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
