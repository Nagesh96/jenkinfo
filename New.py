from jira import JIRA
import sys

def update_issue_fields(username, password, issue_key, fields_dict):
    options = {
        'server': 'https://your-jira-instance.atlassian.net'
    }
    
    try:
        jira = JIRA(options, basic_auth=(username, password))
        issue = jira.issue(issue_key)
        
        update_fields = {}
        for field_name, new_value in fields_dict.items():
            setattr(issue.fields, field_name, new_value)
            update_fields[field_name] = new_value
        
        issue.update(fields=update_fields)
        
        print(f"Fields in issue '{issue_key}' updated successfully.")
    except Exception as e:
        print("Failed to update the fields. Error:", str(e))

# Accepting arguments from the command line in the format 'Key=Value'
if len(sys.argv) < 5:
    print("Usage: python script.py Username=your_username Password=your_password IssueKey=YOUR-PROJECT-KEY-123 FieldName1=new_value1 FieldName2=new_value2 ...")
else:
    arguments = {}
    for arg in sys.argv[1:]:
        key, value = arg.split('=')
        arguments[key] = value
    
    username = arguments.get('Username')
    password = arguments.get('Password')
    issue_key = arguments.get('IssueKey')
    
    fields_dict = {}
    for key, value in arguments.items():
        if key != 'Username' and key != 'Password' and key != 'IssueKey':
            fields_dict[key] = value
    
    update_issue_fields(username, password, issue_key, fields_dict)
