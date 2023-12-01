from jira import JIRA
import sys

def update_issue_fields(username, password, issue_key, fields_dict):
    jira_url = "https://jira.charter.com"
    
    try:
        jira = JIRA(server=jira_url, basic_auth=(username, password))
        issue = jira.issue(issue_key)
        
        issue.update(fields=fields_dict)
        
        print(f"Fields in issue '{issue_key}' updated successfully.")
    except Exception as e:
        print(f"Failed to update the fields. Error:", str(e))

if len(sys.argv) < 6 or not all(arg.startswith(('JIRA_TICKET=', 'ENVIRONMENT=', 'COMMENT=', 'USERNAME=', 'PASSWORD=')) for arg in sys.argv[1:]):
    print("Usage: python jira_up_arg.py JIRA_TICKET=<issue_key> ENVIRONMENT=<environment> COMMENT=<comment> USERNAME=<username> PASSWORD=<password> [field_name1=value1 field_name2=value2 ...]")
    sys.exit(1)

args = {}
for arg in sys.argv[1:]:
    key_value = arg.split('=')
    if len(key_value) == 2:
        args[key_value[0]] = key_value[1]

issue_key = args.get("JIRA_TICKET")
environment = args.get("ENVIRONMENT")
comment = args.get("COMMENT")
jira_username = args.get("USERNAME")
jira_password = args.get("PASSWORD")

fields_dict = {k: v for k, v in args.items() if k not in ['JIRA_TICKET', 'ENVIRONMENT', 'COMMENT', 'USERNAME', 'PASSWORD']}

if not issue_key or not environment or not comment or not jira_username or not jira_password or not fields_dict:
    print("Please provide 'JIRA_TICKET', 'ENVIRONMENT', 'COMMENT', 'USERNAME', 'PASSWORD', and at least one 'field_name'='value' pair")
    sys.exit(1)

jira_url = "https://jira.charter.com"

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

        issue = jira.issue(issue_key)
        jira.transition_issue(issue, new_status)
        jira.add_comment(issue, body=text)
        
        update_issue_fields(jira_username, jira_password, issue_key, fields_dict)
        
        print(f"JIRA issue {issue_key} status updated to {new_status}. Comment added.")
    else:
        print(f"Environment '{environment}' not found in the mapping")
except Exception as e:
    print(f"An error occurred: {str(e)}")
