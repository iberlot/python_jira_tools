class JiraAuth:
    @staticmethod
    def validate_credentials(base_url, username, token):
        try:
            api = JiraAPI(base_url, username, token)
            api.get("myself")
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
