#!/usr/bin/env python3
import base64
import csv
import sys
import time
import requests
import os
from typing import Dict, List, Optional
from datetime import datetime

# ==========================================
# # CONFIG - EDIT THESE
# ==========================================
JIRA_BASE_URL    = "https://amd.atlassian.net"
JIRA_EMAIL       = "sailen.sahoo@amd.com"
JIRA_API_TOKEN   = "YOUR_NEW_TOKEN"  # Update this!

# JQL updated to find issues that have performed this specific transition
JQL_QUERY        = 'project = DECH AND status CHANGED FROM "Automated Review Submit" TO "Peer Review"'

downloads_path   = os.path.join(os.path.expanduser("~"), "Downloads")
OUTPUT_CSV_PATH  = os.path.join(downloads_path, "peer_review_first_dates.csv")

SEARCH_PAGE_SIZE = 50
CHANGELOG_PAGE_SIZE = 100

# ==========================================
# # HELPER FUNCTIONS
# ==========================================

def jira_headers(email: str, api_token: str) -> Dict[str, str]:
    token = base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def request_json(session, method, url, **kwargs):
    max_attempts = 8
    backoff_seconds = 2
    for attempt in range(1, max_attempts + 1):
        resp = session.request(method, url, **kwargs)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", backoff_seconds)))
            continue
        if resp.status_code in (502, 503, 504) and attempt < max_attempts:
            time.sleep(backoff_seconds)
            backoff_seconds *= 2
            continue
        if not resp.ok:
            raise RuntimeError(f"HTTP {resp.status_code} for {url}: {resp.text}")
        return resp.json()

def search_issues(session, base_url, jql, page_size=100):
    issues = []
    next_page_token = None
    while True:
        url = f"{base_url}/rest/api/3/search/jql"
        body = {"jql": jql, "maxResults": page_size, "fields": ["summary"]}
        if next_page_token:
            body["nextPageToken"] = next_page_token
        
        data = request_json(session, "POST", url, json=body)
        batch = data.get("issues", [])
        for issue in batch:
            issues.append({
                "key": issue["key"], 
                "summary": issue.get("fields", {}).get("summary", "")
            })
        
        next_page_token = data.get("nextPageToken")
        if data.get("isLast", True) or not next_page_token:
            break
    return issues

def fetch_full_changelog(session, base_url, issue_key, page_size=100):
    histories = []
    start_at = 0
    while True:
        url = f"{base_url}/rest/api/3/issue/{issue_key}/changelog"
        params = {"startAt": start_at, "maxResults": page_size}
        data = request_json(session, "GET", url, params=params)
        values = data.get("values", [])
        histories.extend(values)
        start_at += len(values)
        if start_at >= data.get("total", 0) or not values:
            break
    return histories

def get_first_specific_transition(histories, from_status, to_status):
    """Finds the timestamp of the EARLIEST specific status transition."""
    # Ensure histories are sorted by creation date (earliest first)
    histories_sorted = sorted(histories, key=lambda h: h.get("created", ""))
    
    for history in histories_sorted:
        for item in history.get('items', []):
            if item.get('field') == 'status':
                if item.get('fromString') == from_status and item.get('toString') == to_status:
                    # Return the very first match found
                    return history.get("created")
    return None

# ==========================================
# # MAIN LOGIC
# ==========================================

def main():
    base_url = JIRA_BASE_URL.rstrip("/")
    with requests.Session() as session:
        session.headers.update(jira_headers(JIRA_EMAIL, JIRA_API_TOKEN))
        
        print(f"Fetching issues via JQL...")
        issues = search_issues(session, base_url, JQL_QUERY, page_size=SEARCH_PAGE_SIZE)
        print(f"Found {len(issues)} issues. Extracting first transition dates...")

        with open(OUTPUT_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["issue_key", "summary", "first_peer_review_date"])
            writer.writeheader()

            for idx, issue in enumerate(issues, start=1):
                key = issue["key"]
                try:
                    histories = fetch_full_changelog(session, base_url, key, page_size=CHANGELOG_PAGE_SIZE)
                    
                    # Logic: 1st time moved from Automated Review Submit -> Peer Review
                    first_date = get_first_specific_transition(
                        histories, 
                        "Automated Review Submit", 
                        "Peer Review"
                    )

                    writer.writerow({
                        "issue_key": key,
                        "summary": issue["summary"],
                        "first_peer_review_date": first_date or "N/A"
                    })

                except Exception as e:
                    print(f"[WARN] Error processing {key}: {e}", file=sys.stderr)

                if idx % 10 == 0:
                    print(f"Processed {idx}/{len(issues)} issues...")

    print(f"\nDone! Results saved to: {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    main()
    
