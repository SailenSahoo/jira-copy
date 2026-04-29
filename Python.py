import csv
import os
from jira import JIRA

# --- Configuration ---
JIRA_SERVER = 'https://your-company.atlassian.net' 
JIRA_USER = 'your-email@example.com'
JIRA_API_TOKEN = 'your_api_token'

# Ensure the Downloads path is correct for Windows
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
OUTPUT_FILE = os.path.join(downloads_path, "rejected_issues_report.csv")

JQL_QUERY = 'status = Closed AND status WAS Rejected AND "Rejected Date" is EMPTY'

# Connect
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

print("Fetching all issues (automatically handling pagination)...")

# This one method replaces the entire while loop and start_at logic
# It is the most robust way to get all results in the new library version
all_issues = jira.search_all_issues(JQL_QUERY, expand='changelog')

print(f"Found {len(all_issues)} issues. Writing to CSV...")

with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Issue Key', 'Latest Rejected Date'])

    for issue in all_issues:
        latest_rejected = "Not Found"
        
        # Check if changelog exists (just in case)
        if hasattr(issue, 'changelog'):
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

print(f"Success! File saved to: {OUTPUT_FILE}")
