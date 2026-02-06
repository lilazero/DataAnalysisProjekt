from datetime import datetime
from typing import Optional, Any


def parse_date(date_value: Any, formats: Optional[list] = None) -> Optional[datetime]:
    """
    Parse a date value into a datetime object.

    Attempts to parse the date using multiple common formats.

    Args:
        date_value: Date value (string, datetime, or other)
        formats: Optional list of date format strings to try

    Returns:
        datetime object if parsing succeeds, None otherwise

    Example:
        >>> parse_date("2023-05-15")
        datetime.datetime(2023, 5, 15, 0, 0)
    """
    if date_value is None:
        return None

    if isinstance(date_value, datetime):
        return date_value

    if not isinstance(date_value, str):
        date_value = str(date_value)

    date_value = date_value.strip()

    if formats is None:
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%m-%d-%Y",
            "%m/%d/%Y",
            "%Y-%m-%d %H:%M:%S",
            "%d.%m.%Y",
        ]

    for fmt in formats:
        try:
            return datetime.strptime(date_value, fmt)
        except ValueError:
            continue

    return None
