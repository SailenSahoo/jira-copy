# --- UPDATED APP IDENTIFIERS ---
APP_IDENTIFIERS = {
    "com.onresolve.jira.groovy": "ScriptRunner",
    "com.adaptavist.sr.cloud": "ScriptRunner",
    "jsu": "JSU",
    "com.googlecode.jsu": "JSU",
    "workflowtoolbox": "JWT",  # Catching the 'fca' legacy key
    "innovalog": "JWT/JMWE",
    "appfire": "JWT/JMWE"
}

def parse_rules(workflow_name, transition, rules_container, control_type):
    rows = []
    if not rules_container:
        return rows

    # Robust "To Status" handling for that 'str' object error we saw earlier
    to_data = transition.get("to")
    to_status = to_data.get("name", "N/A") if isinstance(to_data, dict) else (str(to_data) if to_data else "N/A")

    for rule_type, rules in rules_container.items():
        for rule in rules:
            rule_key = rule.get("type", "").lower()
            config = rule.get("configuration", {})
            config_str = json.dumps(config).lower()
            
            found_app = None
            # Check for standard keys
            for key, name in APP_IDENTIFIERS.items():
                if key.lower() in rule_key or key.lower() in config_str:
                    found_app = name
                    break
            
            # Special check for your specific 'fca' JWT implementation
            if not found_app and ("fca" in rule_key or "fca" in config_str):
                found_app = "JWT"

            if found_app:
                # JWT stores expressions in 'value' (as seen in your screenshot)
                val_expr = config.get("value") or config.get("expression") or "See Description"
                
                rows.append({
                    "Workflow": workflow_name,
                    "Transition ID": transition.get("id"),
                    "Transition Name": transition.get("name"),
                    "From Status": ", ".join(transition.get("from", ["Any"])),
                    "To Status": to_status,
                    "Add-on": found_app,
                    "Control Type": control_type,
                    "Function Type": rule_key.split("__")[-1] if "__" in rule_key else rule_key.split(":")[-1],
                    "Field ID(s)": config.get("fieldId", "N/A"),
                    "Value / Expression": val_expr,
                    "Description": json.dumps(config)
                })
    return rows
    
