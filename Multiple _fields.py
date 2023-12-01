from jira import JIRA
import sys

# Function to update multiple custom fields in a Jira issue
def update_issue_fields(username, password, issue_key, fields_dict):
    jira_url = "https://jira.charter.com"
    
    try:
        jira = JIRA(server=jira_url, basic_auth=(username, password))
        issue = jira.issue(issue_key)
        
        # Set the custom field values using the fields dictionary
        issue.update(fields=fields_dict)
        
        print(f"Fields in issue '{issue_key}' updated successfully.")
    except Exception as e:
        print(f"Failed to update the fields. Error:", str(e))

# Ensure the correct number of arguments is provided
if len(sys.argv) < 7 or (len(sys.argv) - 1) % 2 != 0:
    print("Usage: python jira_up_arg.py JIRA_TICKET=<issue_key> ENVIRONMENT=<environment> COMMENT=<comment> USERNAME=<username> PASSWORD=<password> FieldID1=<field_id_1> NewValue1=<new_value_1> [FieldID2=<field_id_2> NewValue2=<new_value_2> ...]")
    sys.exit(1)

# Parse key-value pairs from command line arguments
args = {}
for arg in sys.argv[1:]:
    key_value = arg.split('=')
    if len(key_value) == 2:
        args[key_value[0]] = key_value[1]

# Retrieve the JIRA ticket, environment, comment, username, password, and field-value pairs from the arguments
issue_key = args.get("JIRA_TICKET")
environment = args.get("ENVIRONMENT")
comment = args.get("COMMENT")
jira_username = args.get("USERNAME")
jira_password = args.get("PASSWORD")

# Extract field-value pairs from arguments
field_value_pairs = {k: v for k, v in args.items() if k.startswith('FieldID') and args.get(f'NewValue{k.split("FieldID")[1]}')}

# Ensure required arguments are provided
if not issue_key or not environment or not comment or not jira_username or not jira_password or not field_value_pairs:
    print("Please provide 'JIRA_TICKET', 'ENVIRONMENT', 'COMMENT', 'USERNAME', 'PASSWORD', and at least one 'FieldID'-'NewValue' pair")
    sys.exit(1)

jira_url = "https://jira.charter.com"

# Map environment names to JIRA status
status_mapping = {
    "QA": "IN QA",
    "UAT": "IN UAT",
    "PROD": "READY FOR PRODUCTION"
}

try:
    jira = JIRA(server=jira_url, basic_auth=(jira_username, jira_password))

    if environment in status_mapping:
        new_status = status_mapping[environment]
        
        text = f"{comment}"

        # Update the JIRA issue status
        issue = jira.issue(issue_key)
        jira.transition_issue(issue, new_status)
        jira.add_comment(issue, body=text)
        
        # Call the function to update multiple custom fields
        update_issue_fields(jira_username, jira_password, issue_key, field_value_pairs)
        
        print(f"JIRA issue {issue_key} status updated to {new_status}. Comment added.")
    else:
        print(f"Environment '{environment}' not found in the mapping")
except Exception as e:
    print(f"An error occurred: {str(e)}")
