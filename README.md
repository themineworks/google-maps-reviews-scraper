# Google Maps Reviews Scraper: Ratings, Text & Replies

Scrape Google Maps reviews by place URL: star rating, reviewer name, full text, date, owner response and photo count. Works on hotels, restaurants, shops and attractions. Pay per review delivered. Failed results are never charged.

**Run it on Apify:** [apify.com/themineworks/google-maps-reviews](https://apify.com/themineworks/google-maps-reviews)
**Docs, FAQ and pricing:** [themineworks.com/actors/google-maps-reviews](https://themineworks.com/actors/google-maps-reviews/)

**Price:** From $7.00 per 1,000 reviews on Apify's higher plans ($10.00 on the free plan), plus a $0.01 start fee per run. Failed and empty results are never charged.

## What it returns

* Full review text, rating, date and reviewer profile
* Owner responses captured when present
* Sort by newest, highest/lowest rating or most relevant
* Photo count per review
* Residential proxy included. No extra setup

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/google-maps-reviews").call(run_input={
    "placeUrls": [
        "https://www.google.com/maps/place/Starbucks/@40.7566447,-73.9859019,17z/data=!3m1!4b1!4m6!3m5!1s0x89c258552071bcb3:0x5cc7129cc313de1a!8m2!3d40.75664!4d-73.9859!16s%2Fg%2F1tj6vr2s"
    ],
    "maxReviews": 10,
    "sortBy": "newest",
    "language": "en"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/google-maps-reviews').call({
    "placeUrls": [
        "https://www.google.com/maps/place/Starbucks/@40.7566447,-73.9859019,17z/data=!3m1!4b1!4m6!3m5!1s0x89c258552071bcb3:0x5cc7129cc313de1a!8m2!3d40.75664!4d-73.9859!16s%2Fg%2F1tj6vr2s"
    ],
    "maxReviews": 10,
    "sortBy": "newest",
    "language": "en"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~google-maps-reviews/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"placeUrls": ["https://www.google.com/maps/place/Starbucks/@40.7566447,-73.9859019,17z/data=!3m1!4b1!4m6!3m5!1s0x89c258552071bcb3:0x5cc7129cc313de1a!8m2!3d40.75664!4d-73.9859!16s%2Fg%2F1tj6vr2s"], "maxReviews": 10, "sortBy": "newest", "language": "en"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 google_maps_reviews_scraper.py --token YOUR_APIFY_TOKEN --place-urls "https://www.google.com/maps/place/Starbucks/@40.7566447,-73.9859019,17z/data=!3m1!4b1!4m6!3m5!1s0x89c258552071bcb3:0x5cc7129cc313de1a!8m2!3d40.75664!4d-73.9859!16s%2Fg%2F1tj6vr2s" --max-reviews "10" --sort-by "newest" --language "en"
node google_maps_reviews_scraper.mjs --token YOUR_APIFY_TOKEN --place-urls "https://www.google.com/maps/place/Starbucks/@40.7566447,-73.9859019,17z/data=!3m1!4b1!4m6!3m5!1s0x89c258552071bcb3:0x5cc7129cc313de1a!8m2!3d40.75664!4d-73.9859!16s%2Fg%2F1tj6vr2s" --max-reviews "10" --sort-by "newest" --language "en"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `placeUrls` | array |  | Google Maps place URLs to scrape reviews from, for example… |
| `maxReviews` | integer | `20` | Maximum reviews PER PLACE (not per run), so 50 with three places can return up to 150 |
| `sortBy` | string | `"newest"` | Which reviews to take first |
| `language` | string | `"en"` | Two-letter language code for the results, for example en, hi, fr |
| `includeReviewInsights` | boolean | `false` | Adds one extra insights row PER PLACE: rating breakdown, the most common phrases in negative reviews, the… |
| `country` | string |  | Two-letter country code to localise results, for example in, us, gb |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `reviewId` | string | Unique review identifier from Google |
| `placeId` | string | Google Maps place identifier |
| `placeName` | string | Name of the business or landmark |
| `placeUrl` | string | Input Google Maps URL |
| `reviewerName` | string | Display name of the reviewer |
| `reviewerUrl` | string | Link to the reviewer's Google Maps profile |
| `rating` | number | Star rating (1 to 5) |
| `reviewText` | string | Full review text (expanded) |
| `reviewDate` | string | When the review was posted |
| `ownerResponse` | string | Business owner reply, if present |
| `photoCount` | number | Number of photos attached to the review |
| `helpfulVotes` | number | Number of helpful votes |
| `charged` | boolean | Whether this result consumed a paid credit |
| `scraped_at` | string | ISO timestamp when the review was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/google-maps-reviews
```

## FAQ

### Do I need a Google Maps API key?

No. The actor uses a real browser with residential proxy to access publicly visible Google Maps pages. No API key or Google account needed.

### How many reviews can I scrape per place?

Up to 1,000 per run by default. Google Maps loads reviews in batches as you scroll; the actor automates that scroll loop. Set maxReviews to cap the count.

### Does it capture owner responses?

Yes. When a business owner has replied to a review, the ownerResponse field contains the full response text.

### What format is the review date?

Google Maps shows relative dates ("3 months ago"). The actor records the raw text as displayed. ISO conversion would require an additional enrichment step.

### How much does the Google Maps Reviews Scraper cost?

From $7.00 per 1,000 reviews on Apify's higher plans ($10.00 on the free plan), plus a $0.01 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [B2B Leads Finder](https://themineworks.com/actors/b2b-leads-finder/): Business emails and LinkedIn profiles for target companies
* [LinkedIn Company Scraper](https://themineworks.com/actors/linkedin-company-details/): Company size, industry, website, and followers without login
* [Zillow Rental Listings Scraper](https://themineworks.com/actors/zillow-rental-listings/): Scrape Zillow for-rent listings by city or zip. $1 per 1,000 results

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
