from .api import JiraAPI
from .entities import JiraTasks, JiraSprints, JiraProjects, JiraBoards, JiraComments

class JiraManager:
    def __init__(self, base_url, username, token):
        self.api = JiraAPI(base_url, username, token)
        self.tasks = JiraTasks(self.api)
        self.sprints = JiraSprints(self.api)
        self.projects = JiraProjects(self.api)
        self.boards = JiraBoards(self.api)
        self.comments = JiraComments(self.api)

    ## Project related methods

    def get_list_projects(self):
        return self.projects.list_projects()

    def get_project(self, project_key):
        return self.projects.get_project(project_key)

    ## Board related methods

    def get_board(self, board_key):
        return self.boards.get_board(board_key)

    def get_project_boards(self, project_key):
        return self.boards.get_project_boards(project_key)

    ## Sprint related methods

    def get_board_sprints(self, project_key):
        return self.sprints.get_board_sprints(project_key)

    def get_sprint(self, sprint_key):
        return self.sprints.get_sprint(sprint_key)

    def get_task(self, task_id):
        return self.tasks.get_task(task_id)

    def get_project_issues(self, project_key, issue_type=None, assignee=None):
        return self.tasks.get_project_issues(project_key, issue_type, assignee)

    def get_sprint_issues(self, sprint_id, issue_type=None, assignee=None):
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
        return self.tasks.get_attachments(issue_id)
