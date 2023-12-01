from jira import JIRA
import sys

# Function to update a specific custom field in a Jira issue
def update_issue_field(username, password, issue_key, field_id, new_value):
    jira_url = "https://jira.charter.com"
    
    try:
        jira = JIRA(server=jira_url, basic_auth=(username, password))
        issue = jira.issue(issue_key)
        
        # Set the custom field value using the field ID
        issue.update(fields={field_id: new_value})
        
        print(f"Field '{field_id}' in issue '{issue_key}' updated successfully to '{new_value}'.")
    except Exception as e:
        print(f"Failed to update the field '{field_id}'. Error:", str(e))

# Ensure the correct number of arguments is provided
if len(sys.argv) < 7:
    print("Usage: python jira_up_arg.py JIRA_TICKET=<issue_key> ENVIRONMENT=<environment> COMMENT=<comment> USERNAME=<username> PASSWORD=<password> FieldID=<field_id> NewValue=<new_value>")
    sys.exit(1)

# Parse key-value pairs from command line arguments
args = {}
for arg in sys.argv[1:]:
    key_value = arg.split('=')
    if len(key_value) == 2:
        args[key_value[0]] = key_value[1]

# Retrieve the JIRA ticket, environment, comment, username, password, field ID, and field value from the arguments
issue_key = args.get("JIRA_TICKET")
environment = args.get("ENVIRONMENT")
comment = args.get("COMMENT")
jira_username = args.get("USERNAME")
jira_password = args.get("PASSWORD")
field_id = args.get("FieldID")  # Capturing the FieldID argument
new_value = args.get("NewValue")  # Capturing the NewValue argument

# Ensure required arguments are provided
if not issue_key or not environment or not comment or not jira_username or not jira_password or not field_id or not new_value:
    print("Please provide 'JIRA_TICKET', 'ENVIRONMENT', 'COMMENT', 'USERNAME', 'PASSWORD', 'FieldID', and 'NewValue'")
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
        
        # Call the function to update a custom field
        update_issue_field(jira_username, jira_password, issue_key, field_id, new_value)
        
        print(f"JIRA issue {issue_key} status updated to {new_status}. Comment added.")
    else:
        print(f"Environment '{environment}' not found in the mapping")
except Exception as e:
    print(f"An error occurred: {str(e)}")
