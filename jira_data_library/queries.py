""" This module contains classes for interacting with the Jira API. """

class JiraQueries:
    """
    A class to interact with Jira API for retrieving project issues and issue details.

    Attributes:
        api (object): An API client instance used to make requests to the Jira API.

    Methods:
        get_project_issues(project_key):
            Retrieve issues for a specified project.
        get_issue_details(issue_key):
            Retrieve details for a specified issue.
    """

    def __init__(self, api):
        self.api = api

    def get_project_issues(self, project_key):
        """
        Retrieve issues for a specified project.

        Args:
            project_key (str): The key of the project to retrieve issues from.

        Returns:
            Response: The API response containing the list of issues for the project.
        """
        return self.api.get(f"search?jql=project={project_key}")

    def get_issue_details(self, issue_key):
        """
        Retrieve details for a specified issue.

        Args:
            issue_key (str): The key of the issue to retrieve details for.

        Returns:
            Response: The API response containing the details of the issue.
        """
        return self.api.get(f"issue/{issue_key}")
