# --- UPDATED CONFIGURATION ---
APP_IDENTIFIERS = {
    "com.onresolve.jira.groovy": "ScriptRunner",
    "com.adaptavist.sr.cloud": "ScriptRunner",
    "jsu": "JSU",
    "innovalog": "JWT/JMWE", # JWT is often under the Innovalog key
    "com.googlecode.jsu": "JSU"
}

def parse_rules(workflow_name, transition, rules_container, control_type):
    rows = []
    if not rules_container:
        return rows

    to_data = transition.get("to")
    to_status = to_data.get("name", "N/A") if isinstance(to_data, dict) else (str(to_data) if to_data else "N/A")

    for rule_type, rules in rules_container.items():
        for rule in rules:
            rule_key = rule.get("type", "").lower()
            config = rule.get("configuration", {})
            
            # Convert the whole config to a string to look for JSU/JWT signatures
            config_str = json.dumps(config).lower()
            
            found_app = None
            # Check the main type first
            for key, name in APP_IDENTIFIERS.items():
                if key.lower() in rule_key:
                    found_app = name
                    break
            
            # If not found in type, check if it's a Forge/Connect app (like your JSU screenshot)
            if not found_app:
                if "jsu" in config_str:
                    found_app = "JSU"
                elif "innovalog" in config_str or "jmwe" in config_str:
                    found_app = "JWT/JMWE"

            if found_app:
                val_expr = config.get("value") or config.get("expression") or "See Description"
                
                rows.append({
                    "Workflow": workflow_name,
                    "Transition ID": transition.get("id"),
                    "Transition Name": transition.get("name"),
                    "From Status": ", ".join(transition.get("from", ["Any"])),
                    "To Status": to_status,
                    "Add-on": found_app,
                    "Control Type": control_type,
                    "Function Type": rule_key.split(":")[-1],
                    "Field ID(s)": config.get("fieldId", "N/A"),
                    "Value / Expression": val_expr,
                    "Description": json.dumps(config)
                })
    return rows
    
