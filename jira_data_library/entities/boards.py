class JiraBoards:
    def __init__(self, api):
        self.api = api

    def _customize_board(self, board):
        """
        Extrae y retorna un diccionario con campos seleccionados de un tablero.

        Args:
            board (dict): Un diccionario con detalles del tablero.

        Returns:
            dict: Un diccionario con los campos 'id', 'name', 'projectName' y 'projectKey'.
        """
        location = board.get("location", {})
        return {
            "id": board.get("id"),
            "name": board.get("name"),
            "projectName": location.get("projectName"),
            "projectKey": location.get("projectKey"),
        }

    def get_project_boards(self, project_key):
        """
        Obtiene todos los tableros asociados a un proyecto.

        Args:
            project_key (str): Clave del proyecto.

        Returns:
            list[dict]: Lista de tableros asociados al proyecto.
        """
        endpoint = f"board?projectKeyOrId={project_key}"
        response = self.api.get(endpoint, use_sprint_base=True)

        response_data = response if isinstance(response, dict) else response.json()

        if 'values' in response_data and response_data['values']:
            boards = response_data['values']
            return [self._customize_board(board) for board in boards]

        raise ValueError(f"No se encontraron tableros para el proyecto {project_key}")

    def get_board(self, board_id):
        """
        Obtiene la información de un tablero específico.

        Args:
            board_id (int): ID del tablero.

        Returns:
            dict: Información del tablero.
        """
        endpoint = f"board/{board_id}"
        return self._customize_board(self.api.get(endpoint, use_sprint_base=True))
