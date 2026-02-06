from datetime import datetime, timezone


def utc_now():
    """
    # Get current UTC time
    :return:
    """
    return datetime.now(timezone.utc)