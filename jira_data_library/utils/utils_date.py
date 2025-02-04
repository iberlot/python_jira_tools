""" This module contains functions to handle date and time operations. """
from datetime import datetime

def format_date(date_str):
    """
    Convert an ISO 8601 formatted date string to a formatted date string.

    Args:
        date_str (str): The date string in ISO 8601 format.

    Returns:
        str: The formatted date string in "YYYY-MM-DD HH:MM:SS" format.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")
