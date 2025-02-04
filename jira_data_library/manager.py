"""
Módulo que contiene la clase JiraManager,
la cual es la interfaz principal para interactuar con la API de Jira.
"""

from .api import JiraAPI
from .entities import JiraTasks, JiraSprints, JiraProjects, JiraBoards, JiraComments

class JiraManager:
    """
    JiraManager serves as the main interface for interacting with Jira's API, providing
    methods to manage projects, boards, sprints, tasks, and comments.

    Attributes:
        api (JiraAPI): An instance of JiraAPI for API interactions.
        tasks (JiraTasks): Manages Jira tasks.
        sprints (JiraSprints): Manages Jira sprints.
        projects (JiraProjects): Manages Jira projects.
        boards (JiraBoards): Manages Jira boards.
        comments (JiraComments): Manages comments on Jira tasks.

    Methods:
        get_list_projects(): Lists all Jira projects.
        get_project(project_key): Retrieves details of a specific project.
        get_board(board_key): Retrieves details of a specific board.
        get_project_boards(project_key): Lists all boards associated with a project.
        get_board_sprints(project_key): Lists all sprints associated with a board.
        get_sprint(sprint_key): Retrieves details of a specific sprint.
        get_task(task_id): Retrieves details of a specific task.
        get_project_issues(project_key, issue_type=None, assignee=None): Lists issues in a project.
        get_sprint_issues(sprint_id, issue_type=None, assignee=None): Lists issues in a sprint.
        get_task_comments(issue_id): Retrieves comments of a task.
        add_task_comment(issue_id, comment_body): Adds a comment to a task.
        update_task_comment(issue_id, comment_id, new_body): Updates a comment on a task.
        delete_task_comment(issue_id, comment_id): Deletes a comment from a task.
        get_task_attachments(issue_id): Retrieves attachments of a task.
    """
    def __init__(self, base_url, username, token):
        self.api = JiraAPI(base_url, username, token)
        self.tasks = JiraTasks(self.api)
        self.sprints = JiraSprints(self.api)
        self.projects = JiraProjects(self.api)
        self.boards = JiraBoards(self.api)
        self.comments = JiraComments(self.api)

    ## Project related methods

    def get_list_projects(self):
        """
        Lists all Jira projects.

        Returns:
            list: A list of all projects available in Jira.
        """
        return self.projects.list_projects()

    def get_project(self, project_key):
        """
        Retrieve details of a specific Jira project.

        Args:
            project_key (str): The key of the project to retrieve.

        Returns:
            dict: A dictionary containing the project's details.
        """
        return self.projects.get_project(project_key)

    ## Board related methods

    def get_board(self, board_key):
        """
        Retrieve details of a specific Jira board.

        Args:
            board_key (str): The key of the board to retrieve.

        Returns:
            dict: A dictionary containing the board's details.
        """
        return self.boards.get_board(board_key)

    def get_project_boards(self, project_key):
        """
        Lists all boards associated with a specific Jira project.

        Args:
            project_key (str): The key of the project for which to list boards.

        Returns:
            list: A list of boards associated with the specified project.
        """
        return self.boards.get_project_boards(project_key)

    ## Sprint related methods

    def get_board_sprints(self, project_key):
        """
        Lists all sprints associated with a specific Jira board.

        Args:
            project_key (str): The key of the project for which to list sprints.

        Returns:
            list: A list of sprints associated with the specified board.
        """
        return self.sprints.get_board_sprints(project_key)

    def get_sprint(self, sprint_key):
        """
        Retrieve details of a specific Jira sprint.

        Args:
            sprint_key (str): The key of the sprint to retrieve.

        Returns:
            dict: A dictionary containing the sprint's details.
        """
        return self.sprints.get_sprint(sprint_key)

    def get_task(self, task_id):
        """
        Retrieve details of a specific Jira task.

        Args:
            task_id (str): The ID or key of the task to retrieve.

        Returns:
            dict: A dictionary containing the task's details.
        """
        return self.tasks.get_task(task_id)

    def get_project_issues(self, project_key, issue_type=None, assignee=None):
        """
        Retrieves issues from a specified Jira project with optional filtering by issue type
        and assignee.

        Args:
            project_key (str): The key of the project to retrieve issues from.
            issue_type (str, optional): The type of issues to filter by (e.g., "Bug", "Task").
            Defaults to None.
            assignee (str, optional): The username or email of the assignee to filter by.
            Defaults to None.

        Returns:
            list: A list of issues matching the specified criteria.
        """
        return self.tasks.get_project_issues(project_key, issue_type, assignee)

    def get_sprint_issues(self, sprint_id, issue_type=None, assignee=None):
        """
        Retrieves issues from a specified Jira sprint with optional filtering by issue type
        and assignee.

        Args:
            sprint_id (int): The ID of the sprint to retrieve issues from.
            issue_type (str, optional): The type of issues to filter by (e.g., "Bug", "Task").
            Defaults to None.
            assignee (str, optional): The username or email of the assignee to filter by.
            Defaults to None.

        Returns:
            list: A list of issues matching the specified criteria.
        """
        return self.tasks.get_sprint_issues(sprint_id, issue_type, assignee)

    def get_task_comments(self, issue_id):
        """
        Obtiene los comentarios de una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.

        Returns:
            list: Lista de comentarios asociados a la tarea.
        """
        return self.comments.get_comments(issue_id)

    def add_task_comment(self, issue_id, comment_body):
        """
        Agrega un comentario a una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.
            comment_body (str): Cuerpo del comentario.

        Returns:
            dict: Detalles del comentario agregado.
        """
        return self.comments.add_comment(issue_id, comment_body)

    def update_task_comment(self, issue_id, comment_id, new_body):
        """
        Actualiza un comentario de una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.
            comment_id (str): ID del comentario.
            new_body (str): Nuevo contenido del comentario.

        Returns:
            dict: Detalles del comentario actualizado.
        """
        return self.comments.update_comment(issue_id, comment_id, new_body)

    def delete_task_comment(self, issue_id, comment_id):
        """
        Elimina un comentario de una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.
            comment_id (str): ID del comentario.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        return self.comments.delete_comment(issue_id, comment_id)

    def get_task_attachments(self, issue_id):
        """
        Retrieves the attachments of a specified Jira task.

        Args:
            issue_id (str): The ID or key of the task.

        Returns:
            dict: A dictionary containing the task key and a list of its attachments.
        """
        return self.tasks.get_attachments(issue_id)
