class JiraSprints:
    def __init__(self, api):
        self.api = api

    def get_sprint(self, sprint_id):
        """Obtiene los detalles de un sprint específico."""
        return self.api.get(endpoint=f"sprint/{sprint_id}", use_sprint_base=True)

    def get_board_sprints(self, board_key):
        """Obtiene todos los sprints de un proyecto."""
        return self.api.get(endpoint=f"board/{board_key}/sprint", use_sprint_base=True)

    def get_open_sprints(self, board_key):
        """
        Obtiene los sprints no cerrados de un tablero.

        Args:
            board_key (str): Clave del tablero.

        Returns:
            list[dict]: Lista de sprints no cerrados.
        """
        response = self.get_board_sprints(board_key)
        sprints = response.json().get("values", [])
        return [sprint for sprint in sprints if sprint.get("state") != "CLOSED"]

    def get_current_sprint(self, board_key):
        """
        Obtiene el sprint actual (activo) de un tablero.

        Args:
            board_key (str): Clave del tablero.

        Returns:
            dict: Detalles del sprint actual, o None si no hay uno activo.
        """
        response = self.get_board_sprints(board_key)
        sprints = response.json().get("values", [])
        for sprint in sprints:
            if sprint.get("state") == "ACTIVE":
                return sprint
        return None


    def create_sprint(self, project_id, name, start_date, end_date):
        """Crea un nuevo sprint."""
        payload = {
            "name": name,
            "startDate": start_date,
            "endDate": end_date,
            "originBoardId": project_id
        }
        return self.api.post("sprint", json=payload)

    def update_sprint(self, sprint_id, name=None, start_date=None, end_date=None, goal=None):
        """Actualiza un sprint."""
        payload = {}
        if name: payload["name"] = name
        if start_date: payload["startDate"] = start_date
        if end_date: payload["endDate"] = end_date
        if goal: payload["goal"] = goal

        return self.api.put(f"sprint/{sprint_id}", json=payload)

    def delete_sprint(self, sprint_id):
        """Elimina un sprint."""
        return self.api.delete(f"sprint/{sprint_id}")

    def start_sprint(self, sprint_id):
        """Inicia un sprint."""
        return self.api.post(f"sprint/{sprint_id}/start")

    def complete_sprint(self, sprint_id):
        """Marca un sprint como completado."""
        return self.api.post(f"sprint/{sprint_id}/complete")

    def get_sprint_changelog(self, sprint_id):
        """Obtiene el historial de cambios de un sprint."""
        return self.api.get(f"sprint/{sprint_id}/changelog")

    def get_sprint_velocity(self, sprint_id):
        """Obtiene la velocidad del sprint (puntos de historia completados)."""
        return self.api.get(f"sprint/{sprint_id}/velocity")

    def get_sprint_report(self, sprint_id):
        """Obtiene un reporte del sprint."""
        return self.api.get(f"sprint/{sprint_id}/report")

    def get_sprint_board(self, sprint_id):
        """Obtiene el tablero del sprint (kanban o scrum)."""
        return self.api.get(f"sprint/{sprint_id}/board")
