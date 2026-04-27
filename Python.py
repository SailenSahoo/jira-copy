import requests
from requests.auth import HTTPBasicAuth
import csv
import json

# --- CONFIGURATION ---
DOMAIN = "your-domain.atlassian.net"
EMAIL = "your-email@example.com"
API_TOKEN = "your-api-token"
OUTPUT_FILE = "jira_workflow_audit.csv"

# Target app keys/identifiers
APP_IDENTIFIERS = {
    "com.innovalog.jmwe": "JWT/JMWE",
    "com.googlecode.jsu": "JSU",
    "com.onresolve.jira.groovy": "ScriptRunner",
    "com.adaptavist.sr.cloud": "ScriptRunner"
}

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}

def get_workflows():
    url = f"https://{DOMAIN}/rest/api/3/workflow/search"
    params = {
        "isActive": "true",
        "expand": "transitions,transitions.rules"
    }
    
    all_workflows = []
    start_at = 0
    
    while True:
        params["startAt"] = start_at
        response = requests.get(url, headers=headers, auth=auth, params=params)
        data = response.json()
        
        all_workflows.extend(data.get("values", []))
        
        if data.get("isLast", True):
            break
        start_at += len(data.get("values", []))
        
    return all_workflows

def parse_rules(workflow_name, transition, rules_container, control_type):
    rows = []
    if not rules_container:
        return rows

    # Jira lists rules in categories: postFunctions, conditions, validators
    for rule_type, rules in rules_container.items():
        for rule in rules:
            rule_key = rule.get("type", "")
            
            # Check if rule belongs to target add-ons
            found_app = next((name for key, name in APP_IDENTIFIERS.items() if key in rule_key), None)
            
            if found_app:
                config = rule.get("configuration", {})
                rows.append({
                    "Workflow": workflow_name,
                    "Transition ID": transition.get("id"),
                    "Transition Name": transition.get("name"),
                    "From Status": ", ".join(transition.get("from", ["Any"])),
                    "To Status": transition.get("to", {}).get("name", "N/A"),
                    "Add-on": found_app,
                    "Control Type": control_type, # Condition, Validator, or Post Function
                    "Function Type": rule_key.split(":")[-1],
                    "Field ID(s)": config.get("fieldId", "N/A"),
                    "Value / Expression": config.get("value") or config.get("expression") or "See Description",
                    "Description": json.dumps(config) # Full config for context
                })
    return rows

def main():
    workflows = get_workflows()
    csv_data = []

    for wf in workflows:
        wf_name = wf.get("id", {}).get("name")
        for trans in wf.get("transitions", []):
            rules = trans.get("rules", {})
            
            # Audit Post Functions, Conditions, and Validators
            csv_data.extend(parse_rules(wf_name, trans, {"postFunctions": rules.get("postFunctions", [])}, "Post Function"))
            csv_data.extend(parse_rules(wf_name, trans, {"conditions": rules.get("conditions", [])}, "Condition"))
            csv_data.extend(parse_rules(wf_name, trans, {"validators": rules.get("validators", [])}, "Validator"))

    # Write to CSV
    fields = ["Workflow", "Transition ID", "Transition Name", "From Status", "To Status", 
              "Add-on", "Control Type", "Function Type", "Field ID(s)", "Value / Expression", "Description"]
    
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"Audit complete. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
          
