from jira import JIRA

def update_issue_field_with_id():
    try:
        # Hardcoded values
        username = "your_username"
        password = "your_password"
        issue_key = "YOUR-PROJECT-KEY-123"
        field_id = "custom_field_id"  # Replace with your custom field ID
        new_value = "new_value"

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

# Call the function to update the issue field with a custom field ID
update_issue_field_with_id()
