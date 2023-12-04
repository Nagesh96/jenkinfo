from jira import JIRA

# Connect to Jira
options = {
    'server': 'https://your-jira-instance.atlassian.net'
}
jira = JIRA(options, basic_auth=('your_username', 'your_password'))

# Define the dashboard details
dashboard_name = 'My Python Dashboard'
dashboard_description = 'Dashboard created using Python'

# Create the dashboard
dashboard = jira.create_dashboard(dashboard_name, description=dashboard_description)

# Print the dashboard URL
print(f"Dashboard created! URL: {dashboard.permalink()}")

# Manipulate version field value in the JQL query
version_name = '1.0'  # Example version name
formatted_version_name = f'"{version_name}"'  # Format version name for JQL query

# Define JQL query with version field manipulation
jql_query = f'project = MYPROJECT AND fixVersion = {formatted_version_name}'

# Perform the query
issues = jira.search_issues(jql_query)

# Process the retrieved issues
for issue in issues:
    print(f"Issue: {issue.key} - Summary: {issue.fields.summary}")
