from jira import JIRA
import sys

def update_issue_fields(username, password, issue_key, fields_dict):
    jira_url = "https://jira.charter.com"
    
    try:
        jira = JIRA(server=jira_url, basic_auth=(username, password))
        issue = jira.issue(issue_key)
        
        update_fields = {}
        for field_name, new_value in fields_dict.items():
            setattr(issue.fields, field_name, new_value)
            update_fields[field_name] = new_value
        
        issue.update(fields=update_fields)
        
        print(f"Fields in issue '{issue_key}' updated successfully.")
    except Exception as e:
        print("Failed to update the fields. Error:", str(e))

# Check if correct number of arguments is provided
if len(sys.argv) < 5:
    print("Usage: python jira_up_arg.py JIRA_TICKET=<issue_key> ENVIRONMENT=<environment> COMMENT=<comment> USERNAME=<username> PASSWORD=<password> [FieldName1=<new_value1> FieldName2=<new_value2> ...]")
    sys.exit(1)

# Parse key-value pairs from command line arguments
args = {}
for arg in sys.argv[1:]:
    key, value = arg.split('=')
    args[key] = value

# Retrieve necessary values from arguments
issue_key = args.get("JIRA_TICKET")
environment = args.get("ENVIRONMENT")
comment = args.get("COMMENT")
jira_username = args.get("USERNAME")
jira_password = args.get("PASSWORD")

# Ensure required arguments are provided
if not issue_key or not environment or not comment or not jira_username or not jira_password:
    print("Please provide 'JIRA_TICKET', 'ENVIRONMENT', 'COMMENT', 'USERNAME', and 'PASSWORD'")
    sys.exit(1)

fields_dict = {key: value for key, value in args.items() if key not in ["JIRA_TICKET", "ENVIRONMENT", "COMMENT", "USERNAME", "PASSWORD"]}

try:
    # Map environment names to JIRA status
    status_mapping = {
        "QA": "IN QA",
        "UAT": "IN UAT",
        "PROD": "READY FOR PRODUCTION"
    }

    jira = JIRA(server="https://jira.charter.com", basic_auth=(jira_username, jira_password))

    if environment in status_mapping:
        new_status = status_mapping[environment]

        text = f"{comment}"

        # Update the JIRA issue status
        issue = jira.issue(issue_key)
        jira.transition_issue(issue, new_status)
        jira.add_comment(issue, body=text)

        if fields_dict:
            update_issue_fields(jira_username, jira_password, issue_key, fields_dict)

        print(f"JIRA issue {issue_key} status updated to {new_status}. Comment added.")
    else:
        print(f"Environment '{environment}' not found in the mapping")
except Exception as e:
    print(f"An error occurred: {str(e)}")
