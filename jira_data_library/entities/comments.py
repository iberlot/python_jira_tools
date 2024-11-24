from ..utils.adf_converter import ADFConverter

class JiraComments:
    """
    Clase para gestionar los comentarios de una tarea en Jira.
    """

    def __init__(self, api):
        """
        Inicializa la clase con la instancia de JiraAPI.

        Args:
            api (JiraAPI): Instancia de JiraAPI para realizar las solicitudes.
        """
        self.api = api

    def _customize_comment(self, task_key: str, comments: list):
        """
        Personaliza los comentarios de una tarea, extrayendo los campos seleccionados y
        transformando el contenido del comentario con ADFConverter.convert.

        Args:
            task_key (str): Clave de la tarea.
            comments (list): Lista de comentarios obtenidos de la API de Jira.

        Returns:
            dict: Diccionario con la clave de la tarea y los comentarios personalizados.
        """
        customized_comments = []
        for comment in comments:
            customized_comments.append({
                "task_key": task_key,
                "id": comment.get("id"),
                "author": comment.get("author").get("accountId"),
                "body": ADFConverter.convert(comment.get("body", "")).get("result", None),
                "created": comment.get("created"),
            })
        return customized_comments

    def get_comments(self, issue_id):
        """
        Obtiene los comentarios de una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.

        Returns:
            list: Lista de comentarios asociados a la tarea.
        """
        endpoint = f"issue/{issue_id}/comment"
        data = self.api.get(endpoint)
        comments = data.get("comments", [])
        return self._customize_comment(issue_id, comments)

    def add_comment(self, issue_id, comment_body):
        """
        Agrega un comentario a una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.
            comment_body (str): Cuerpo del comentario.

        Returns:
            dict: Detalles del comentario agregado.
        """
        endpoint = f"issue/{issue_id}/comment"
        payload = {"body": comment_body}
        return self.api.post(endpoint, json=payload)

    def update_comment(self, issue_id, comment_id, new_body):
        """
        Actualiza un comentario existente en una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.
            comment_id (str): ID del comentario.
            new_body (str): Nuevo contenido del comentario.

        Returns:
            dict: Detalles del comentario actualizado.
        """
        endpoint = f"issue/{issue_id}/comment/{comment_id}"
        payload = {"body": new_body}
        return self.api.put(endpoint, json=payload)

    def delete_comment(self, issue_id, comment_id):
        """
        Elimina un comentario de una tarea.

        Args:
            issue_id (str): ID o clave de la tarea.
            comment_id (str): ID del comentario.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        endpoint = f"issue/{issue_id}/comment/{comment_id}"
        return self.api.delete(endpoint)
