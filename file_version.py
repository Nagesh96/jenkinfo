from jira import JIRA
import sys

def update_issue_field_with_args(username, password, issue_key, field_id, new_value):
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
if len(sys.argv) < 4:
    print("Usage: python script.py Username Password")
else:
    username = sys.argv[1]
    password = sys.argv[2]
    
    # You can hardcode these values or ask the user to provide them within the script
    issue_key = "YOUR-PROJECT-KEY-123"
    field_id = "custom_field_id"
    new_value = "new_value"
    
    update_issue_field_with_args(username, password, issue_key, field_id, new_value)
