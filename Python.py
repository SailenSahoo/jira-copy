import requests
import csv
import os
import json
from requests.auth import HTTPBasicAuth

# --- 1. Configuration ---
JIRA_URL = 'https://amd.atlassian.net' # Updated based on your screenshot
EMAIL = 'your-email@example.com'
API_TOKEN = 'your_api_token'

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
OUTPUT_FILE = os.path.join(downloads_path, "rejected_issues_report.csv")

# Ensure JQL matches your requirement
JQL_QUERY = 'status = Closed AND status WAS Rejected AND "Rejected Date" is EMPTY'

# --- 2. Setup ---
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

all_issues = []
start_at = 0
max_results = 100

print("Connecting to the new Jira Search JQL API...")

# --- 3. The Fetch Loop (Using POST as required) ---
while True:
    # This is the NEW endpoint you were instructed to migrate to
    search_url = f"{JIRA_URL}/rest/api/3/search/jql"
    
    # In the new API, we send data in a JSON body (POST), not in the URL (GET)
    payload = {
        "jql": JQL_QUERY,
        "startAt": start_at,
        "maxResults": max_results,
        "expand": ["changelog"],
        "fields": ["key"] 
    }

    response = requests.post(
        search_url, 
        data=json.dumps(payload), 
        headers=headers, 
        auth=auth
    )
    
    if response.status_code != 200:
        print(f"Failed! HTTP {response.status_code}: {response.text}")
        break

    data = response.json()
    batch = data.get('issues', [])
    
    if not batch:
        break

    all_issues.extend(batch)
    print(f"Retrieved {len(all_issues)} of {data.get('total')} issues...")
    
    if len(all_issues) >= data.get('total', 0):
        break
        
    start_at += max_results

# --- 4. Write to CSV ---
print(f"Writing results to {OUTPUT_FILE}...")

with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Issue Key', 'Latest Rejected Date'])

    for issue in all_issues:
        issue_key = issue['key']
        latest_rejected = "Not Found"
        
        # Access the changelog histories
        histories = issue.get('changelog', {}).get('histories', [])
        
        # Reverse to find the most recent transition to 'Rejected'
        for history in reversed(histories):
            found_transition = False
            for item in history.get('items', []):
                if item.get('field') == 'status' and item.get('toString') == 'Rejected':
                    latest_rejected = history.get('created')
                    found_transition = True
                    break
            if found_transition:
                break
        
        writer.writerow([issue_key, latest_rejected])

print("Process Complete.")
