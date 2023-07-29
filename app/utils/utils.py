from datetime import date, datetime
from json import dumps

import pytz
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


def local_to_utc(
    local_timezone,
    local_time,
):
    to_zone = pytz.UTC
    from_zone = pytz.timezone(local_timezone)

    current_date = date.today()

    local_time_obj = datetime.strptime(local_time, "%H:%M:%S").time()

    local_datetime = datetime.combine(current_date, local_time_obj)

    local_datetime = from_zone.localize(local_datetime)

    utc_datetime = local_datetime.astimezone(to_zone)

    utc_time = utc_datetime.time()

    return utc_time


def time_difference(time2, time1, common_date):
    # Convert the datetime.time objects to datetime objects with a common date
    time1 = datetime.strptime(time1, "%H:%M:%S").time()
    time2 = datetime.strptime(time2, "%H:%M:%S").time()

    datetime1 = datetime.combine(common_date, time1)
    datetime2 = datetime.combine(common_date, time2)

    # Calculate the time difference
    time_difference = (datetime2 - datetime1).total_seconds() / 3600

    return time_difference


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
        print(data, sep="\n")
    else:
        print(data)
