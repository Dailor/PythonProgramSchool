from datetime import datetime


def get_utc_date_in_iso(dt: datetime) -> str:
    return dt.isoformat()[:-3] + 'Z'
