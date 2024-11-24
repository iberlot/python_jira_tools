def format_date(date_str):
    """Convierte una fecha de Jira a un formato amigable."""
    from datetime import datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")
