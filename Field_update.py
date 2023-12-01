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

# The existing code you provided remains unchanged

# Ensure required arguments are provided
if not issue_key or not environment or not comment or not jira_username or not jira_password:
    print("Please provide 'JIRA_TICKET', 'ENVIRONMENT', 'COMMENT', 'USERNAME', and 'PASSWORD'")
    sys.exit(1)

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
        field_id = "customfield_17856"  # Replace with the actual field ID
        new_value = "New value for the custom field"  # Replace with the desired new value
        update_issue_field(jira_username, jira_password, issue_key, field_id, new_value)
        
        print(f"JIRA issue {issue_key} status updated to {new_status}. Comment added.")
    else:
        print(f"Environment '{environment}' not found in the mapping")
except Exception as e:
    print(f"An error occurred: {str(e)}")
