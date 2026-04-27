def parse_rules(workflow_name, transition, rules_container, control_type):
    rows = []
    if not rules_container:
        return rows

    # Get the "To Status" safely
    to_data = transition.get("to")
    if isinstance(to_data, dict):
        to_status = to_data.get("name", "N/A")
    else:
        # If it's already a string or None
        to_status = str(to_data) if to_data else "N/A"

    for rule_type, rules in rules_container.items():
        for rule in rules:
            rule_key = rule.get("type", "")
            
            found_app = next((name for key, name in APP_IDENTIFIERS.items() if key in rule_key), None)
            
            if found_app:
                config = rule.get("configuration", {})
                
                # JSU often nests data in a 'value' string, we try to extract it
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
    
