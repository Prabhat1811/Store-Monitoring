from datetime import datetime

from dateutil import tz


def utc_to_local(local_timezone, utc_time):
    to_zone = tz.gettz(local_timezone)
    from_zone = tz.gettz("UTC")

    # Remove milliseconds if present
    utc_time = utc_time.split(".")[0]

    utc = datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S")

    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)

    print("UTC Time:", utc)
    print("Local Time:", local)


def local_to_utc(local_timezone, local_time):
    to_zone = tz.gettz("UTC")
    from_zone = tz.gettz(local_timezone)

    local_time = local_time.split(".")[0]

    local = datetime.strptime(local_time, "%Y-%m-%d %H:%M:%S")

    local = local.replace(tzinfo=from_zone)
    utc = local.astimezone(to_zone)

    print("Local Time:", local)
    print("UTC Time:", utc)


def get_day_of_week_from_utc(utc_time):
    # dayOfWeek(0=Monday, 6=Sunday)

    day_mapping = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    utc_time = utc_time.split(".")[0]

    utc = datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S")
    day_of_week = utc.strftime("%A")

    return day_mapping[day_of_week.lower()]
