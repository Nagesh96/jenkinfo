from jira import JIRA
import sys

# Set username, password, and issue_key as variables
username = "your_username"
password = "your_password"
issue_key = "YOUR-PROJECT-KEY-123"

def update_issue_field_with_args(field_id, new_value):
    try:
        options = {
            'server': 'https://your-jira-instance.atlassian.net'
        }

        jira = JIRA(options, basic_auth=(username, password))
        issue = jira.issue(issue_key)

        setattr(issue.fields, field_id, new_value)
        issue.update(fields={field_id: new_value})

        print(f"Field with ID '{field_id}' in issue '{issue_key}' updated successfully to '{new_value}'.")
    except Exception as e:
        print(f"Failed to update the field with ID '{field_id}'. Error:", str(e))

# Check if enough arguments are provided
if len(sys.argv) < 3:
    print("Usage: python script.py FieldId=Value")
else:
    argument = sys.argv[1].split('=')
    if len(argument) != 2:
        print("Please provide FieldId=Value")
    else:
        field_id = argument[0]
        new_value = argument[1]
        
        update_issue_field_with_args(field_id, new_value)
