import requests
from requests.auth import HTTPBasicAuth
import csv
import json

# --- CONFIGURATION ---
DOMAIN = "your-company.atlassian.net"
EMAIL = "your-email@example.com"
API_TOKEN = "your-api-token-here"
OUTPUT_FILE = "jira_statuses.csv"

def export_jira_statuses():
    url = f"https://{DOMAIN}/rest/api/3/status"
    
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)
    headers = {
        "Accept": "application/json"
    }

    print(f"Connecting to {DOMAIN}...")

    try:
        response = requests.request("GET", url, headers=headers, auth=auth)
        response.raise_for_status()
        
        statuses = response.json()

        # Define the CSV headers
        fieldnames = ['ID', 'Name', 'Category', 'Description']

        with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for status in statuses:
                writer.writerow({
                    'ID': status.get('id'),
                    'Name': status.get('name'),
                    'Category': status.get('statusCategory', {}).get('name', 'N/A'),
                    'Description': status.get('description', '')
                })

        print(f"Success! Exported {len(statuses)} statuses to {OUTPUT_FILE}")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    export_jira_statuses()
    
