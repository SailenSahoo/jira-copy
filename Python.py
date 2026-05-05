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
JIRA_API_TOKEN   = "YOUR_TOKEN_HERE"

# JQL to find potential candidates who reached Closed via both paths
JQL_QUERY        = 'project = DECH AND status = Closed AND status WAS Rejected AND status WAS Implemented'

downloads_path   = os.path.join(os.path.expanduser("~"), "Downloads")
OUTPUT_CSV_PATH  = os.path.join(downloads_path, "issues_to_clear_rejected_date.csv")

SEARCH_PAGE_SIZE = 50
CHANGELOG_PAGE_SIZE = 100

# ==========================================
# # HELPER FUNCTIONS (From your screenshots)
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
            issues.append({"key": issue["key"], "summary": issue.get("fields", {}).get("summary", "")})
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

def get_latest_transition(histories, from_status, to_status):
    """Finds the latest timestamp for a specific status transition."""
    latest_dt = None
    for hist in histories:
        for item in hist.get("items", []):
            if item.get("field") == "status":
                if item.get("fromString") == from_status and item.get("toString") == to_status:
                    # Parse Jira date: '2024-05-05T10:00:00.000+0000'
                    dt_str = hist.get("created")[:23]
                    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
                    if not latest_dt or dt > latest_dt:
                        latest_dt = dt
    return latest_dt

# ==========================================
# # MAIN LOGIC
# ==========================================

def main():
    base_url = JIRA_BASE_URL.rstrip("/")
    with requests.Session() as session:
        session.headers.update(jira_headers(JIRA_EMAIL, JIRA_API_TOKEN))
        
        print(f"Searching for issues...")
        issues = search_issues(session, base_url, JQL_QUERY, page_size=SEARCH_PAGE_SIZE)
        print(f"Found {len(issues)} candidate issues. Analyzing histories...")

        with open(OUTPUT_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["issue_key", "summary", "reason"])
            writer.writeheader()

            for idx, issue in enumerate(issues, start=1):
                key = issue["key"]
                try:
                    histories = fetch_full_changelog(session, base_url, key, page_size=CHANGELOG_PAGE_SIZE)
                    
                    # Get latest of both types of transitions
                    rejected_dt = get_latest_transition(histories, "Rejected", "Closed")
                    implemented_dt = get_latest_transition(histories, "Implemented", "Closed")

                    if rejected_dt and implemented_dt:
                        # CORE LOGIC: Check if Implemented -> Closed happened LATER
                        if implemented_dt > rejected_dt:
                            writer.writerow({
                                "issue_key": key,
                                "summary": issue["summary"],
                                "reason": f"Implemented({implemented_dt}) > Rejected({rejected_dt})"
                            })
                            print(f"[MATCH] {key}")

                except Exception as e:
                    print(f"[ERROR] {key}: {e}", file=sys.stderr)

                if idx % 25 == 0:
                    print(f"Processed {idx}/{len(issues)} issues...")

    print(f"Done. Results written to: {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    main()
