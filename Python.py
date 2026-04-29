import csv
import os
from jira import JIRA

# --- Configuration ---
JIRA_SERVER = 'https://your-company.atlassian.net' 
JIRA_USER = 'your-email@example.com'
JIRA_API_TOKEN = 'your_api_token'

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
OUTPUT_FILE = os.path.join(downloads_path, "rejected_issues_report.csv")

JQL_QUERY = 'status = Closed AND status WAS Rejected AND "Rejected Date" is EMPTY'

# Connect
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

all_issues = []
start_at = 0
max_results = 100

print("Fetching issues (manual pagination)...")

while True:
    # We use search_issues but keep the parameters very simple
    # If it throws a deprecation error, we use the dict-based approach below
    try:
        issues_batch = jira.search_issues(
            JQL_QUERY, 
            startAt=start_at, 
            maxResults=max_results, 
            expand='changelog'
        )
    except Exception:
        # Fallback for the newer versions that are being picky
        issues_batch = jira.search_issues(
            jql_str=JQL_QUERY,
            startAt=start_at,
            maxResults=max_results,
            expand='changelog'
        )
    
    if not issues_batch:
        break
        
    all_issues.extend(issues_batch)
    print(f"Retrieved {len(all_issues)} issues...")
    start_at += max_results

print(f"Total issues found: {len(all_issues)}. Writing to CSV...")

with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Issue Key', 'Latest Rejected Date'])

    for issue in all_issues:
        latest_rejected = "Not Found"
        # Accessing the history directly from the issue object
        for history in reversed(issue.changelog.histories):
            found = False
            for item in history.items:
                if item.field == 'status' and item.toString == 'Rejected':
                    latest_rejected = history.created
                    found = True
                    break
            if found:
                break
        writer.writerow([issue.key, latest_rejected])

print(f"Done! Check your Downloads folder for: {os.path.basename(OUTPUT_FILE)}")
