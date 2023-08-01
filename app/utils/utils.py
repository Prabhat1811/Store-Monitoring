from datetime import date, datetime, time
from json import dumps

import pytz


def utc_to_local(utc_time_str: time, local_timezone: str) -> time:
    """
    Converts utc to local.

    Returns time object, Format: "%H:%M:%S"
    """

    to_zone = pytz.timezone(local_timezone)
    from_zone = pytz.UTC

    current_date = date.today()

    utc_time_obj = datetime.strptime(str(utc_time_str).split(".")[0], "%H:%M:%S").time()

    utc_datetime = datetime.combine(current_date, utc_time_obj)

    utc_datetime = from_zone.localize(utc_datetime)

    local_datetime = utc_datetime.astimezone(to_zone)

    local_time = local_datetime.strftime("%H:%M:%S")

    return str_to_time(local_time)


def time_difference(time1, time2, common_date):

    datetime1 = datetime.combine(common_date, time1)
    datetime2 = datetime.combine(common_date, time2)

    # Calculate the time difference
    time_diff = (datetime1 - datetime2).total_seconds() / 3600

    return time_diff


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

    utc_time = str(utc_time).split(".")[0]

    utc = datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S")
    day_of_week = utc.strftime("%A")

    return day_mapping[day_of_week.lower()]


def pretty_print(data, indent=2):
    # For testing

    if type(data) == dict:
        print(dumps(data, indent))
    elif type(data) == list:
        for i in data:
            print(i, "\n")
    else:
        print(data)


def str_to_time(time: str) -> time:
    """
    Takes in time as datetime obj or str.
    Returns time object.
    """
    time = datetime.strptime(str(time).split(".")[0], "%H:%M:%S")

    return time.time()

