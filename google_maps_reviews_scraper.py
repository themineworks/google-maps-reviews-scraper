#!/usr/bin/env python3
"""Star ratings, full review text and owner replies for any Maps listing. Python, Node.js and cURL clients for the Google Maps Reviews Scraper on Apify, pay per result.

Command-line client for the themineworks/google-maps-reviews actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/google-maps-reviews/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/google-maps-reviews"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--place-urls", help="Comma-separated. Google Maps place URLs to scrape reviews from, for example…")
    ap.add_argument("--max-reviews", type=int, help="Maximum reviews PER PLACE (not per run), so 50 with three places can return up to 150")
    ap.add_argument("--sort-by", help="Which reviews to take first")
    ap.add_argument("--language", help="Two-letter language code for the results, for example en, hi, fr")
    ap.add_argument("--include-review-insights", action=argparse.BooleanOptionalAction, help="Adds one extra insights row PER PLACE: rating breakdown, the most common phrases in…")
    ap.add_argument("--country", help="Two-letter country code to localise results, for example in, us, gb")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.place_urls: run_input["placeUrls"] = [s.strip() for s in a.place_urls.split(",") if s.strip()]
    if a.max_reviews is not None: run_input["maxReviews"] = a.max_reviews
    if a.sort_by is not None: run_input["sortBy"] = a.sort_by
    if a.language is not None: run_input["language"] = a.language
    if a.include_review_insights is not None: run_input["includeReviewInsights"] = a.include_review_insights
    if a.country is not None: run_input["country"] = a.country

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
