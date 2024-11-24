import re
import os

from ..utils.adf_converter import ADFConverter

class JiraTasks:
    def __init__(self, api):
        self.api = api
    def _customize_task(self, task):
        fields = task.get("fields", {})
        subtasks = fields.get("subtasks", [])

        processed_subtasks = [self._customize_task(subtask) for subtask in subtasks]

        sprint_data = fields.get(self.api.sprint_field, []) or []
        last_sprint = sprint_data[-1] if sprint_data else None
        old_sprints = sprint_data[:-1] if len(sprint_data) > 1 else []

        attachments = []
        for attachment in fields.get('attachment', []):
            attachments.append(
                {
                    "id": attachment.get("id"),
                    "filename": attachment.get("filename"),
                    "mimeType": attachment.get("mimeType"),
                    "content_url": attachment.get("content"),
                }
            )

        return {
            "id": task.get("id"),
            "key": task.get("key"),
            "issuetype": fields.get("issuetype", {}).get("name"),
            "issuetype_subtask": fields.get("issuetype", {}).get("subtask", False),
            "parent_id": fields.get("parent", {}).get("id"),
            "parent_key": fields.get("parent", {}).get("key"),
            "parent_is_epic": fields.get("parent", {}).get("fields", {}).get("issuetype", {}).get("name") == "Epic",
            "project_id": fields.get("project", {}).get("id"),
            "project_key": fields.get("project", {}).get("key"),
            "sprint_id": last_sprint.get("id") if last_sprint else None,
            "old_sprints": [sprint.get("id") for sprint in old_sprints],
            "boardId": fields.get("boardId"),
            "priority_id": fields.get("priority", {}).get("id"),
            "priority_name": fields.get("priority", {}).get("name"),
            "assignee": fields.get("assignee", {}).get("accountId"),
            "assignee_emailAddress": fields.get("assignee", {}).get("emailAddress"),
            "status_name": fields.get("status", {}).get("name"),
            "status_id": fields.get("status", {}).get("id"),
            "status_color": fields.get("status", {}).get("statusCategory", {}).get("colorName"),
            "summary": fields.get("summary"),
            "description": ADFConverter.convert(fields.get("description")) if fields.get("description") else None,
            "story_points": fields.get(self.api.story_points_field),
            "subtasks": processed_subtasks,
            "attachments": attachments,
        }


    def _extract_sprint_id(self, fields):
        """
        Extrae el ID del sprint de los campos personalizados.

        Args:
            fields (dict): Campos de una tarea.

        Returns:
            int or None: El ID del sprint si está disponible, de lo contrario None.
        """
        sprint_field_value = fields.get(self.api.sprint_field)
        if isinstance(sprint_field_value, list) and sprint_field_value:
            # Usualmente el valor de sprint es una lista con objetos o strings
            first_sprint = sprint_field_value[0]
            if isinstance(first_sprint, str):
                # Intentar extraer el ID del sprint de un string como "id=18, ..."
                match = re.search(r"id=(\d+)", first_sprint)
                if match:
                    return int(match.group(1))
            elif isinstance(first_sprint, dict):
                # Si es un diccionario, buscar el campo 'id'
                return first_sprint.get("id")
        return None

    def get_task(self, task_key):
        """Obtiene los detalles de una tarea específica."""
        return self._customize_task(self.api.get(f"issue/{task_key}"))


    def get_project_issues(self, project_key, issue_type=None, assignee=None):
        """
        Obtiene todas las issues de un proyecto, con opciones de filtrado por tipo de issue y usuario asignado.

        Args:
            project_key (str): Clave del proyecto.
            issue_type (str, optional): Tipo de issue (ej. "Bug", "Task"). Default es None.
            assignee (str, optional): Usuario asignado (username o email). Default es None.

        Returns:
            list: Lista de issues filtradas.
        """
        jql = [f'project="{project_key}"']
        if issue_type:
            jql.append(f'issuetype="{issue_type}"')
        if assignee:
            jql.append(f'assignee="{assignee}"')
        query = " AND ".join(jql)

        endpoint = f"search?jql={query}"
        response = self.api.get(endpoint=endpoint)
        return response.json().get("issues", [])

    def get_sprint_issues(self, sprint_id, issue_type=None, assignee=None):
        """
        Obtiene todas las issues de un sprint, con opciones de filtrado por tipo de issue y usuario asignado.

        Args:
            sprint_id (int): ID del sprint.
            issue_type (str, optional): Tipo de issue (ej. "Bug", "Task"). Default es None.
            assignee (str, optional): Usuario asignado (username o email). Default es None.

        Returns:
            list: Lista de issues filtradas.
        """
        jql = [f'sprint={sprint_id}']
        if issue_type:
            jql.append(f'issuetype="{issue_type}"')
        if assignee:
            jql.append(f'assignee in ("{assignee}")')
        query = " AND ".join(jql)

        endpoint = f"search?jql={query}"
        response = self.api.get(endpoint=endpoint)
        return response.get("issues", [])


    def create_task(self, project_key, summary, description, issue_type):
        """Crea una nueva tarea en un proyecto."""
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
            }
        }
        return self.api.post("issue", data=data)
    def _download_attachment(self, attachment_url, filename):
        """
        Descarga el archivo adjunto desde Jira y lo guarda localmente.

        Args:
            attachment_url (str): URL del archivo adjunto en Jira.
            filename (str): Nombre del archivo a guardar.

        Returns:
            str: Ruta del archivo descargado.
        """
        print(attachment_url)
        response = self.api.get(endpoint=attachment_url)
        print(response)
        if response.status_code == 200:
            file_path = os.path.join(self.api.download_path, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
        else:
            print(f"Error al descargar el archivo: {response.status_code}")
            return None

    def get_attachments(self, task_key):
        """
        Obtiene los adjuntos de una tarea, los descarga y devuelve una lista con los datos.

        Args:
            task_key (str): Clave de la tarea.

        Returns:
            dict: Diccionario con la clave de la tarea y los adjuntos descargados.
        """
        response = self.get_task(task_key)
        attachments = []

        for attachment in response.get('attachments'):
            filename = attachment.get('filename')
            print(filename)
            print(f"/attachment/content/{attachment.get('id')}")
            file_path = self._download_attachment(f"/attachment/content/{attachment.get('id')}", filename)

            if file_path:
                attachments.append({
                    'content_url': file_path,
                    'filename': filename,
                    'type': filename.split('.')[-1]
                })

        return {
            'task': task_key,
            'attachments': attachments
        }
