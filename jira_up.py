from jira import JIRA
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) % 2 != 1 or len(sys.argv) < 10:
    print("Usage: python jira_up_arg.py JIRA_TICKET <issue_key> ENVIRONMENT <environment> COMMENT <comment> USERNAME <username> PASSWORD <password> ")
    sys.exit(1)

# Parse key-value pairs from command line arguments
args = dict(zip(sys.argv[1::2], sys.argv[2::2]))

# Retrive the JIRA ticket  and environment and comment from the arguments

issue_key = args.get("JIRA_TICKET")
environment = args.get("ENVIRONMENT")
comment = args.get("COMMENT")
jira_username = args.get("USERNAME")
jira_password = args.get("PASSWORD")

# Ensure required arguments are provided
if not issue_key or not environment or not comment or not jira_username or not jira_password:
    print("Please provide 'JIRA_TICKET', 'ENVIRONMENT', 'COMMENT', 'USERNAME' and 'PASSWORD' ")
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
        #issue.update(fields={"status": "new_status"})
        print(f"JIRA issue {issue_key} status updated to {new_status}. Comment added.")
    else:
        print(f"Environment '{environment}' not found in the mapping")
except Exception as e:
    print(f"An error occured: {str(e)}")
