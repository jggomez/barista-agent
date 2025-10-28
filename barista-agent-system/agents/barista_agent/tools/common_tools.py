import datetime


def get_today_date() -> str:
    """Returns today's date in YYYY-MM-DD H:M:S" format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
