import datetime


def get_current_promotion(date: str) -> dict[str, str] | None:
    """
    Returns the current promotion based on the provided datetime.

    Args:
        datetime (str): The datetime in "YYYY-MM-DD H:M:S" format.

    Returns:
        dict[str, str] | None: A dictionary describing the current promotion, or None if not found.
    """

    # Give more examples from this mock with day of week:
    promotions = [
        {
            "day_of_week": 0,
            "special": {
                "name": "Espresso Elixir",
                "deal": "Get a free pastry with any purchase!",
            },
        },
        {
            "day_of_week": 1,
            "special": {
                "name": "Double Shot Tuesday",
                "deal": "Earn 2x loyalty points on all espresso drinks today!",
            },
        },
        {
            "day_of_week": 2,
            "special": {
                "name": "Cold Brew Friday",
                "deal": "Enjoy 20% off all Cold Brews and Nitro coffees.",
            },
        },
        {
            "day_of_week": 3,
            "special": {
                "name": "Morning Combo Deal",
                "deal": "Buy any large coffee and get a breakfast sandwich for half price.",
            },
        },
        {
            "day_of_week": 4,
            "special": {
                "name": "No Daily Special",
                "deal": "Currently, there are no special promotions running. Check back tomorrow!",
            },
        },
    ]

    day = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").weekday()

    for promotion in promotions:
        if promotion["day_of_week"] == day:
            return promotion["special"]  # type: ignore[return-value]

    return None
