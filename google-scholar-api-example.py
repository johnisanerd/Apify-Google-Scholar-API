"""
Example: call the Google Scholar API Apify Actor from Python.

The Actor has six modes:
  search           papers for a query (one dataset row per paper)
  cite             citation formats (MLA, APA, ...) for a paper
  author_profile   an author's profile and metrics
  author_articles  an author's article list
  author_citation  one article from an author's profile
  author_co_authors  an author's co-authors

This example runs 'search' and prints each paper with its authors and cited-by
count. Inputs are kept small so the first run stays inexpensive (each result
page is one billed query).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
Set it in a .env file (see .env.example) or export APIFY_API_TOKEN.
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise SystemExit(
        "APIFY_API_TOKEN is not set. Copy .env.example to .env and add your key, "
        "or run: export APIFY_API_TOKEN=your_api_key_here"
    )

client = ApifyClient(APIFY_API_TOKEN)

run_input = {
    "mode": "search",
    "q": "machine learning",
    "num": 5,
    "max_pages": 1,
    # "as_ylo": 2020,   # earliest year
    # "as_sdt": "4",    # case law (US courts) instead of articles
}

print(f"Google Scholar {run_input['mode']}: {run_input['q']}")
run = client.actor("johnvc/google-scholar-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not start. Check your API token and inputs.")

# In search mode, each dataset row is one paper.
papers = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"\nReturned {len(papers)} papers.\n")

for paper in papers:
    info = paper.get("publication_info") or {}
    links = paper.get("inline_links") or {}
    authors = ", ".join(a.get("name", "") for a in (info.get("authors") or [])) or info.get("summary", "")

    print(f"{paper.get('position')}. {paper.get('paper_title')}")
    print(f"   {info.get('summary', '')}")
    if authors:
        print(f"   Authors: {authors}")
    print(f"   Cited by: {links.get('cited_by_total', 0)}  |  versions: {links.get('versions_total', 0)}")
    print(f"   result_id={paper.get('result_id')}")
    print(f"   {paper.get('link')}")
    print()
