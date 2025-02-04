""" Módulo para interactuar con la API de Jira. """
import requests

class JiraAPI:
    """
    Clase para interactuar con la API de Jira, permitiendo realizar solicitudes
    GET y POST, así como inicializar campos personalizados para puntos de historia
    y sprints. Utiliza autenticación básica HTTP y maneja errores de solicitud.
    """
    HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def __init__(self, base_url, username, token, download_path='/'):
        self.base_url_sprint = f"{base_url}.atlassian.net/rest/agile/1.0"
        self.base_url = f"{base_url}.atlassian.net/rest/api/3"
        self.auth = requests.auth.HTTPBasicAuth(username, token)
        self.story_points_field = None
        self.sprint_field = None
        self.download_path = download_path
        self._initialize_custom_fields()

    def get(self, endpoint, params=None, use_sprint_base=False):
        """
        Sends a GET request to the specified Jira API endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to.
            params (dict, optional): Query parameters to include in the request.
            use_sprint_base (bool, optional): Whether to use the sprint base URL.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ValueError: If the request results in an HTTP error.
        """
        url = f"{self.base_url_sprint if use_sprint_base else self.base_url}/{endpoint}"
        response = requests.get(url,
                                auth=self.auth,
                                params=params,
                                headers=self.HEADERS,
                                timeout=10)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Error en la solicitud a {url}: {e.response.text}") from e
        return response.json()

    def post(self, endpoint, data=None):
        """
        Sends a POST request to the specified Jira API endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to.
            data (dict, optional): The JSON payload to include in the request body.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.HTTPError: If the request results in an HTTP error.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, auth=self.auth, json=data, timeout=10)
        response.raise_for_status()
        return response.json()

    def _initialize_custom_fields(self):
        """
        Initializes custom fields for story points and sprints by querying the Jira API.

        Retrieves all fields from the Jira API and searches for fields related to
        "story points" and "sprint". Sets the corresponding field IDs to
        `self.story_points_field` and `self.sprint_field`. Raises a ValueError if
        either field is not found.

        Returns:
            dict: A dictionary containing the IDs of the story points and sprint fields.
        """
        response = self.get("field")
        if not isinstance(response, list):
            raise ValueError("La respuesta esperada de 'field' debe ser una lista.")
        for field in response:
            if "story points" in field.get("name", "").lower():
                self.story_points_field = field.get("id")
            if "sprint" in field.get("name", "").lower():
                self.sprint_field = field.get("id")

        if not self.story_points_field:
            raise ValueError("No se encontró el campo de Story Points.")
        if not self.sprint_field:
            raise ValueError("No se encontró el campo de Sprint.")

        return {
            "story_points_field": self.story_points_field,
            "sprint_field": self.sprint_field,
        }
