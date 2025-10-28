def check_availability_coffee(datetime: str) -> list[str]:
    """
    Checks the availability of coffee types based on the provided datetime.

    Args:
        datetime (str): The datetime in "HH:MM" format (military time).

    Returns:
        list[str]: A list of available coffee types for the given time.
    """
    try:
        # Create a dictionary where the key is the military time and the value is the type of coffee based on this information RULES
        availability_coffee_type = {
            "08:00": ["Mocha Magic", "Hazelnut Harmony"],
            "09:00": ["Mocha Magic", "Hazelnut Harmony"],
            "10:00": ["Mocha Magic", "Hazelnut Harmony"],
            "11:00": ["Mocha Magic", "Hazelnut Harmony"],
            #
            "12:00": ["Vanilla Dream", "Hazelnut Harmony"],
            "13:00": ["Vanilla Dream", "Hazelnut Harmony"],
            #
            "14:00": ["Vanilla Dream"],
            "15:00": ["Vanilla Dream"],
            #
            "16:00": ["Caramel Delight"],
            "17:00": ["Caramel Delight"],
            "18:00": ["Caramel Delight"],
            "19:00": ["Caramel Delight"],
        }

        hour = datetime.split(":")[0]
        hour_key = hour + ":00"

        if hour_key in availability_coffee_type:
            return availability_coffee_type[hour_key]

        return []

    except Exception as e:
        print(f"An error occurred in check_availability_coffee: {e}")
        return []
