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
# 1. Update your JIRA_BASE_URL (no trailing slash)
# 2. Update your JIRA_EMAIL
# 3. Update your JIRA_API_TOKEN (highly recommend generating a new one)
# 4. Ensure the Custom Field ID for 'Rejected Date' is correct for your instance

JIRA_BASE_URL    = "https://amd.atlassian.net"
JIRA_EMAIL       = "sailen.sahoo@amd.com"
JIRA_API_TOKEN   = "YOUR_NEW_API_TOKEN_HERE"

# Updated JQL: Finds Closed issues that passed through both statuses
JQL_QUERY        = 'project = DECH AND status = Closed AND status WAS Rejected AND status WAS Implemented'

# Path configuration
downloads_path   = os.path.join(os.path.expanduser("~"), "Downloads")
OUTPUT_CSV_PATH  = os.path.join(downloads_path, "issues_to_clear_rejected_date.csv")

SEARCH_PAGE_SIZE = 50

# ==========================================
# # HELPER FUNCTIONS
# ==========================================

def jira_headers(email: str, api_token: str) -> Dict[str, str]:
    token = base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def get_latest_transition_date(histories: List[Dict], from_status: str, to_status: str) -> Optional[datetime]:
    """Finds the timestamp of the most recent specific transition."""
    latest_dt = None
    for history in histories:
        for item in history.get('items', []):
            if item.get('field') == 'status':
                if item.get('fromString') == from_status and item.get('toString') == to_status:
                    # Jira format: '2024-05-05T10:00:00.000+0000'
                    # We strip the timezone for a simpler comparison
                    dt_str = history.get('created')[:23]
                    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f')
                    if not latest_dt or dt > latest_dt:
                        latest_dt = dt
    return latest_dt

# ==========================================
# # MAIN EXECUTION
# ==========================================

def main():
    headers = jira_headers(JIRA_EMAIL, JIRA_API_TOKEN)
    matched_issues = []
    start_at = 0
    
    print(f"Starting extraction from {JIRA_BASE_URL}...")

    while True:
        # Search for issues with changelog expanded
        search_url = f"{JIRA_BASE_URL}/rest/api/3/search"
        params = {
            "jql": JQL_QUERY,
            "startAt": start_at,
            "maxResults": SEARCH_PAGE_SIZE,
            "expand": "changelog"
        }
        
        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        issues = data.get('issues', [])
        
        if not issues:
            break

        for issue in issues:
            key = issue.get('key')
            histories = issue.get('changelog', {}).get('histories', [])
            
            # Identify the latest dates for both paths
            rej_to_closed = get_latest_transition_date(histories, "Rejected", "Closed")
            imp_to_closed = get_latest_transition_date(histories, "Implemented", "Closed")
            
            if rej_to_closed and imp_to_closed:
                # Logic: If Implemented-to-Closed happened AFTER Rejected-to-Closed
                if imp_to_closed > rej_to_closed:
                    print(f"[MATCH] {key}: Implemented ({imp_to_closed}) > Rejected ({rej_to_closed})")
                    matched_issues.append(key)
            
        start_at += SEARCH_PAGE_SIZE
        if start_at >= data.get('total', 0):
            break

    # Save results to CSV
    if matched_issues:
        with open(OUTPUT_CSV_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Issue Key"])
            for issue_key in matched_issues:
                writer.writerow([issue_key])
        print(f"\nSuccess! Found {len(matched_issues)} issues.")
        print(f"File saved to: {OUTPUT_CSV_PATH}")
    else:
        print("\nNo issues found matching the transition criteria.")

if __name__ == "__main__":
    main()
        
