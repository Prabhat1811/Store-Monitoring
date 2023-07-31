from typing import Any, Dict, List

from sqlalchemy.engine.row import Row

from app.utils.utils import *


def get_start_end_day_index(db_store_status_logs, day):
    """Find the starting, ending log of a specific day"""

    start = end = -1

    for i in range(len(db_store_status_logs)):
        if db_store_status_logs[i].Store_Status.timestamp_utc.day == day:
            start = i
            break

    for i in range(start + 1, len(db_store_status_logs)):

        if db_store_status_logs[i].Store_Status.timestamp_utc.day != day:
            end = i
            break

    if end == -1:
        end = len(db_store_status_logs) - 1

    if start != 0:
        start += 1

    return start, end + 1


def get_start_day_index(db_store_status_logs, day):
    pass

    for i in range(len(db_store_status_logs)):
        if db_store_status_logs[i].Store_Status.timestamp_utc.day == day:
            break

    return i


def calculate_total_uptime(
    schedule: List[List[Any]],
    logs,
    start_index,
    end_index,
    local_timezone,
    status,
    date_today,
):
    """
    Total uptime of a day

    Time Complexity: O(n)

    Approach:
    Turns out, It was easier than what I had initially thought.

    I have divided this function into 3 parts/while loops.

    `1st Part`

    `2nd Part`

    `3rd Part`

    """
    i = start_index
    j = 0
    uptime = 0

    # print(schedule)
    # print(logs)
    # return

    # print(logs[i].Store_Status)
    # return

    while (
        i < end_index
        and j < len(schedule)
        and utc_to_local(logs[i].Store_Status.timestamp_utc.time(), local_timezone)
        >= schedule[j][1]
    ):
        if status == "active":
            uptime += time_difference(schedule[j][1], schedule[j][0], date_today)
        j += 1

    while i < end_index and j < len(schedule):
        logged_till = schedule[j][0]

        while (
            i < end_index
            and utc_to_local(logs[i].Store_Status.timestamp_utc.time(), local_timezone)
            <= schedule[j][1]
        ):
            if status == "active":
                uptime += time_difference(
                    utc_to_local(
                        logs[i].Store_Status.timestamp_utc.time(), local_timezone
                    ),
                    logged_till,
                    date_today,
                )

            logged_till = utc_to_local(
                logs[i].Store_Status.timestamp_utc.time(), local_timezone
            )
            status = logs[i].Store_Status.status
            i += 1

        if status == "active":
            uptime += time_difference(schedule[j][1], logged_till, date_today)

        j += 1

    while status == "active" and j < len(schedule):
        uptime += time_difference(schedule[j][1], schedule[j][0], date_today)
        j += 1

    return round(uptime, 2)


def sum_time_intervals(buisness_hours: List[str], date_today):
    """Get opening hours in a day"""

    opening_hours = 0

    for schedule in buisness_hours:
        opening_hours += time_difference(schedule[1], schedule[0], date_today)

    return opening_hours


class Store:
    def __init__(
        self,
        store_id,
        local_timezone,
        date_today,
        db_store_timings,
        db_store_status_logs,
    ):
        self.store_id = store_id
        self.local_timezone = local_timezone
        self.date_today = date_today

        self.buisness_hours = self.buisness_time_interval(db_store_timings)

        self.db_store_status_logs = db_store_status_logs

    def buisness_time_interval(self, store_timings: List[Row]) -> Dict[int, Any]:

        buisness_hours = {
            0: [],  # Monday
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],  # Sunday
        }

        for row in store_timings:
            day = row.Menu_Hours.day

            start_time = str_to_time(row.Menu_Hours.start_time_local)
            end_time = str_to_time(row.Menu_Hours.end_time_local)

            buisness_hours[day].append(
                [
                    start_time,
                    end_time,
                ]
            )

        return buisness_hours

    def uptime_downtime_last_hour(self):
        pass

    def uptime_downtime_last_day(self):

        if self.db_store_status_logs:
            start_day_date = get_start_day_index(
                self.db_store_status_logs,
                self.db_store_status_logs[-1].Store_Status.timestamp_utc.day,
            )
            end_day_date = len(self.db_store_status_logs)
            last_logged_day = get_day_of_week_from_utc(
                self.db_store_status_logs[-1].Store_Status.timestamp_utc
            )

            # Get previous log status, If previous log doesn't exists get current day status
            previous_log_status = self.db_store_status_logs[
                max(0, start_day_date - 1)
            ].Store_Status.status

            uptime = calculate_total_uptime(
                self.buisness_hours[last_logged_day],
                self.db_store_status_logs,
                start_day_date,
                end_day_date,
                self.local_timezone,
                previous_log_status,
                self.date_today,
            )

            total_supposed_uptime = round(
                sum_time_intervals(
                    self.buisness_hours[last_logged_day], self.date_today
                )
            )

            downtime = round(total_supposed_uptime - uptime, 2)
        else:
            uptime = "NO LOGS"
            downtime = "NO LOGS"

        return uptime, downtime

    def uptime_downtime_last_week(self):

        # print("Inside Week")

        if self.db_store_status_logs:
            uptime = 0

            start_index = 0
            start_day_date = self.db_store_status_logs[0].Store_Status.timestamp_utc.day

            # Iterate through the logs keeping track of start time and endtime
            for i, log in enumerate(self.db_store_status_logs):

                if i >= len(self.db_store_status_logs) - 1:
                    previous_log_status = self.db_store_status_logs[
                        len(self.db_store_status_logs) - 1
                    ].Store_Status.status

                    day = get_day_of_week_from_utc(
                        self.db_store_status_logs[
                            max(0, i - 1)
                        ].Store_Status.timestamp_utc
                    )

                    uptime += calculate_total_uptime(
                        self.buisness_hours[day],
                        self.db_store_status_logs,
                        start_index,
                        i,
                        self.local_timezone,
                        previous_log_status,
                        self.date_today,
                    )

                if log.Store_Status.timestamp_utc.day != start_day_date:

                    previous_log_status = self.db_store_status_logs[
                        max(0, i - 1)
                    ].Store_Status.status

                    day = get_day_of_week_from_utc(
                        self.db_store_status_logs[
                            max(0, i - 1)
                        ].Store_Status.timestamp_utc
                    )

                    uptime += calculate_total_uptime(
                        self.buisness_hours[day],
                        self.db_store_status_logs,
                        start_index,
                        i,
                        self.local_timezone,
                        previous_log_status,
                        self.date_today,
                    )

                    start_day_date = self.db_store_status_logs[
                        i
                    ].Store_Status.timestamp_utc.day

            # Calculate total time for which the store is supposed to be open
            total_supposed_uptime = 0
            for i in self.buisness_hours:
                total_supposed_uptime += round(
                    sum_time_intervals(self.buisness_hours[i], self.date_today)
                )

            downtime = round(total_supposed_uptime - uptime, 2)
            uptime = round(uptime, 2)
        else:
            uptime = "NO LOGS"
            downtime = "NO LOGS"

        return uptime, downtime

    def calculate_data(self):

        # uptime_last_hour, downtime_last_hour = self.uptime_downtime_last_hour()
        uptime_last_day, downtime_last_day = self.uptime_downtime_last_day()
        uptime_last_week, downtime_last_week = self.uptime_downtime_last_week()

        return [
            self.store_id,
            # uptime_last_hour,
            uptime_last_day,
            uptime_last_week,
            # downtime_last_hour,
            downtime_last_day,
            downtime_last_week,
        ]
