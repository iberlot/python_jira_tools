"""
This module contains the JiraSprints class, which provides methods to interact with Jira's
sprint-related API endpoints.
"""

class JiraSprints:
    """
    A class to interact with Jira's sprint-related API endpoints.

    This class provides methods to retrieve, create, update, and delete sprints,
    as well as to manage sprint states and retrieve sprint reports and metrics.

    Attributes:
        api: An instance of the API client used to make requests to Jira.

    Methods:
        get_sprint(sprint_id): Retrieves details of a specific sprint.
        get_board_sprints(board_key): Retrieves all sprints for a specific board.
        get_open_sprints(board_key): Retrieves all open sprints for a specific board.
        get_current_sprint(board_key): Retrieves the current active sprint for a board.
        create_sprint(project_id, name, start_date, end_date): Creates a new sprint.
        update_sprint(sprint_id, name, start_date, end_date, goal): Updates an existing sprint.
        delete_sprint(sprint_id): Deletes a sprint.
        start_sprint(sprint_id): Starts a sprint.
        complete_sprint(sprint_id): Marks a sprint as completed.
        get_sprint_changelog(sprint_id): Retrieves the changelog of a sprint.
        get_sprint_velocity(sprint_id): Retrieves the velocity of a sprint.
        get_sprint_report(sprint_id): Retrieves a report of the sprint.
        get_sprint_board(sprint_id): Retrieves the board associated with the sprint.
    """
    def __init__(self, api):
        self.api = api

    def get_sprint(self, sprint_id):
        """
        Retrieves details of a specific sprint.

        Args:
            sprint_id (int): The unique identifier of the sprint.

        Returns:
            Response: API response containing sprint details.
        """
        return self.api.get(endpoint=f"sprint/{sprint_id}", use_sprint_base=True)

    def get_board_sprints(self, board_key):
        """
        Obtiene todos los sprints de un tablero específico.

        Args:
            board_key (str): Clave del tablero.

        Returns:
            Response: Respuesta de la API con los sprints del tablero.
        """
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
        """
        Creates a new sprint for a specified project.

        Args:
            project_id (int): The unique identifier of the project board.
            name (str): The name of the sprint.
            start_date (str): The start date of the sprint in ISO 8601 format.
            end_date (str): The end date of the sprint in ISO 8601 format.

        Returns:
            Response: API response after attempting to create the sprint.
        """
        payload = {
            "name": name,
            "startDate": start_date,
            "endDate": end_date,
            "originBoardId": project_id
        }
        return self.api.post("sprint", json=payload)

    def update_sprint(self, sprint_id, name=None, start_date=None, end_date=None, goal=None):
        """
        Updates an existing sprint with the provided details.

        Args:
            sprint_id (int): The unique identifier of the sprint to update.
            name (str, optional): The new name for the sprint.
            start_date (str, optional): The new start date for the sprint in ISO 8601 format.
            end_date (str, optional): The new end date for the sprint in ISO 8601 format.
            goal (str, optional): The new goal for the sprint.

        Returns:
            Response: API response after attempting to update the sprint.
        """
        payload = {}
        if name:
            payload["name"] = name

        if start_date:
            payload["startDate"] = start_date

        if end_date:
            payload["endDate"] = end_date

        if goal:
            payload["goal"] = goal

        return self.api.put(f"sprint/{sprint_id}", json=payload)

    def delete_sprint(self, sprint_id):
        """
        Deletes a sprint with the specified ID.

        Args:
            sprint_id (int): The unique identifier of the sprint to delete.

        Returns:
            Response: API response after attempting to delete the sprint.
        """
        return self.api.delete(f"sprint/{sprint_id}")

    def start_sprint(self, sprint_id):
        """
        Starts a sprint with the specified ID.

        Args:
            sprint_id (int): The unique identifier of the sprint to start.

        Returns:
            Response: API response after attempting to start the sprint.
        """
        return self.api.post(f"sprint/{sprint_id}/start")

    def complete_sprint(self, sprint_id):
        """
        Marks a sprint as completed.

        Args:
            sprint_id (int): The unique identifier of the sprint to complete.

        Returns:
            Response: API response after attempting to complete the sprint.
        """
        return self.api.post(f"sprint/{sprint_id}/complete")

    def get_sprint_changelog(self, sprint_id):
        """
        Retrieves the changelog of a specific sprint.

        Args:
            sprint_id (int): The unique identifier of the sprint.

        Returns:
            Response: API response containing the sprint changelog.
        """
        return self.api.get(f"sprint/{sprint_id}/changelog")

    def get_sprint_velocity(self, sprint_id):
        """
        Retrieves the velocity of a specific sprint.

        Args:
            sprint_id (int): The unique identifier of the sprint.

        Returns:
            Response: API response containing the sprint velocity data.
        """
        return self.api.get(f"sprint/{sprint_id}/velocity")

    def get_sprint_report(self, sprint_id):
        """
        Retrieves a report of a specific sprint.

        Args:
            sprint_id (int): The unique identifier of the sprint.

        Returns:
            Response: API response containing the sprint report.
        """
        return self.api.get(f"sprint/{sprint_id}/report")

    def get_sprint_board(self, sprint_id):
        """
        Retrieves the board associated with a specific sprint.

        Args:
            sprint_id (int): The unique identifier of the sprint.

        Returns:
            Response: API response containing the board details.
        """
        return self.api.get(f"sprint/{sprint_id}/board")
