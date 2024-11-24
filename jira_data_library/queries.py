class JiraQueries:
    def __init__(self, api):
        self.api = api

    def get_project_issues(self, project_key):
        return self.api.get(f"search?jql=project={project_key}")

    def get_issue_details(self, issue_key):
        return self.api.get(f"issue/{issue_key}")
