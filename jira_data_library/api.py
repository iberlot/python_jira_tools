import requests

class JiraAPI:

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
        print("CASAS")
        url = f"{self.base_url_sprint if use_sprint_base else self.base_url}/{endpoint}"
        response = requests.get(url,
                                auth=self.auth,
                                params=params,
                                headers=self.HEADERS,
                                timeout=10)
        print(response)
        try:
            print(response.raise_for_status())
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Error en la solicitud a {url}: {e.response.text}") from e
        return response.json()

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, auth=self.auth, json=data)
        response.raise_for_status()
        return response.json()

    def _initialize_custom_fields(self):
        """
        Obtiene los campos configurados en Jira y asigna los IDs de los campos
        personalizados para story_points y sprints.
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
