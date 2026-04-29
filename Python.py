import csv
from jira import JIRA

# --- Configuration ---
JIRA_SERVER = 'https://your-company.atlassian.net' 
JIRA_USER = 'your-email@example.com'
JIRA_API_TOKEN = 'your_generated_api_token'
OUTPUT_FILE = 'rejected_issues_report.csv'

JQL_QUERY = 'status = Closed AND status WAS Rejected AND "Rejected Date" is EMPTY'

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

all_issues = []
block_size = 100
start_at = 0

print("Fetching all issues (this may take a moment)...")

# Loop to handle pagination
while True:
    # Fetch a block of issues
    issues_batch = jira.search_issues(
        JQL_QUERY, 
        startAt=start_at, 
        maxResults=block_size, 
        expand='changelog'
    )
    
    if len(issues_batch) == 0:
        break
        
    all_issues.extend(issues_batch)
    print(f"Retrieved {len(all_issues)} issues...")
    
    # Move the starting point for the next request
    start_at += block_size

print(f"Total issues found: {len(all_issues)}. Writing to {OUTPUT_FILE}...")

with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Issue Key', 'Latest Rejected Date'])

    for issue in all_issues:
        latest_rejected = "Not Found"
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

print("Done!")
