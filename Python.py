import requests
import csv
import os
from requests.auth import HTTPBasicAuth

# --- Configuration ---
JIRA_URL = 'https://your-company.atlassian.net'
EMAIL = 'your-email@example.com'
API_TOKEN = 'your_api_token'

# Path for Windows Downloads
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
OUTPUT_FILE = os.path.join(downloads_path, "rejected_issues_report.csv")

# JQL Query
JQL_QUERY = 'status = Closed AND status WAS Rejected AND "Rejected Date" is EMPTY'

# Setup Authentication
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}

all_results = []
start_at = 0
max_results = 100

print("Fetching data directly from Jira API...")

while True:
    # Jira Cloud REST API v3 Search Endpoint
    url = f"{JIRA_URL}/rest/api/3/search"
    
    query_params = {
        'jql': JQL_QUERY,
        'startAt': start_at,
        'maxResults': max_results,
        'expand': 'changelog',
        'fields': 'key' # We only need the key and the history
    }

    response = requests.request("GET", url, headers=headers, params=query_params, auth=auth)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        break

    data = response.json()
    issues = data.get('issues', [])
    
    if not issues:
        break

    all_results.extend(issues)
    print(f"Retrieved {len(all_results)} issues...")
    
    # Check if we've reached the total
    if len(all_results) >= data.get('total', 0):
        break
        
    start_at += max_results

print(f"Processing {len(all_results)} issues and writing to CSV...")

with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Issue Key', 'Latest Rejected Date'])

    for issue in all_results:
        issue_key = issue['key']
        latest_rejected = "Not Found"
        
        # Dig into the changelog
        histories = issue.get('changelog', {}).get('histories', [])
        
        # Reverse to find the most recent transition to 'Rejected'
        for history in reversed(histories):
            found_rejected = False
            for item in history.get('items', []):
                if item.get('field') == 'status' and item.get('toString') == 'Rejected':
                    latest_rejected = history.get('created')
                    found_rejected = True
                    break
            if found_rejected:
                break
        
        writer.writerow([issue_key, latest_rejected])

print(f"Done! File saved to: {OUTPUT_FILE}")
