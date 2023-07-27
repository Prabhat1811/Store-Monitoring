from datetime import datetime

from dateutil import tz


def utc_to_local(local_timezone, utc_time):
    to_zone = tz.gettz(local_timezone)
    from_zone = tz.gettz("UTC")

    utc_time = utc_time.split(".")[0]

    utc = datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S")

    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)

    print("UTC Time:", utc)
    print("Local Time:", local)
