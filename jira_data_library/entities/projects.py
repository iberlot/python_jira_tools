""" A module for interacting with Jira projects using a provided API. """

class JiraProjects:
    """
    A class to interact with Jira projects using a provided API.

    Attributes:
        api: An API client instance used to fetch project data.

    Methods:
        _customize_project(project): Extracts necessary fields from a project.
        get_project(project_key): Retrieves project details and returns customized fields.
        list_projects(): Lists all projects with customized fields.
    """

    def __init__(self, api):
        self.api = api

    def _customize_project(self, project):
        """
        Extracts and returns a dictionary with selected fields from a project.

        Args:
            project (dict): A dictionary containing project details.

        Returns:
            dict: A dictionary with the project's 'id', 'key', 'name', and 'uuid'.
        """
        return {
            "id": project.get("id"),
            "key": project.get("key"),
            "name": project.get("name"),
            "uuid": project.get("uuid"),
        }

    def get_project(self, project_key):
        """
        Retrieve and customize details of a Jira project.

        Args:
            project_key (str): The key of the project to retrieve.

        Returns:
            dict: A dictionary containing the customized fields of the project.
        """
        project = self.api.get(f"project/{project_key}")
        return self._customize_project(project)

    def list_projects(self):
        """
        A class to interact with Jira projects using a provided API.

        Attributes:
            api: An API client instance used to fetch project data.

        Methods:
            _customize_project(project): Extracts necessary fields from a project.
            get_project(project_key): Retrieves project details and returns customized fields.
            list_projects(): Lists all projects with customized fields.
        """
        projects = self.api.get("project")
        return [self._customize_project(project) for project in projects]
