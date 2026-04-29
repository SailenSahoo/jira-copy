import csv
from jira import JIRA

# --- Configuration ---
# Use your full Jira Cloud URL
JIRA_SERVER = 'https://your-company.atlassian.net' 
# Use the email address associated with your Atlassian account
JIRA_USER = 'your-email@example.com'
# Use the API Token generated from id.atlassian.com
JIRA_API_TOKEN = 'your_generated_api_token'
OUTPUT_FILE = 'rejected_issues_report.csv'

# JQL: Current status Closed, was Rejected, but Rejected Date field is empty
JQL_QUERY = 'status = Closed AND status WAS Rejected AND "Rejected Date" is EMPTY'

# Connect to Jira Cloud
jira = JIRA(
    server=JIRA_SERVER, 
    basic_auth=(JIRA_USER, JIRA_API_TOKEN)
)

print("Searching for issues...")

# We use expand='changelog' here to pull history data for all issues at once
issues = jira.search_issues(JQL_QUERY, expand='changelog', maxResults=100)

print(f"Found {len(issues)} issues. Writing to {OUTPUT_FILE}...")

with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Issue Key', 'Latest Rejected Date'])

    for issue in issues:
        latest_rejected = "Not Found"
        
        # Access the changelog we expanded in the search
        # We reverse it to find the MOST RECENT transition to 'Rejected' first
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
