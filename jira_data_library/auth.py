""" This module contains the JiraAuth class, which is used to validate Jira credentials. """
from jira_data_library.api import JiraAPI


class JiraAuth:
    """
    A class for validating Jira credentials.

    This class provides a static method to validate Jira credentials by
    attempting to authenticate with the Jira API.

    Methods:
        validate_credentials(base_url, username, token): Validates the provided
        Jira credentials and returns a boolean indicating the success of the
        authentication.
    """
    def __init__(self):
        pass

    @staticmethod
    def validate_credentials(base_url, username, token):
        """
        Validates Jira credentials by attempting to authenticate with the Jira API.

        Args:
            base_url (str): The base URL of the Jira instance.
            username (str): The username for Jira authentication.
            token (str): The API token for Jira authentication.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        try:
            api = JiraAPI(base_url, username, token)
            api.get("myself")
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
