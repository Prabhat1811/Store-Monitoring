from typing import Dict, List

from sqlalchemy.engine.row import Row

from app.utils.utils import *


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

        self.buisness_hours = self.calculate_buisness_hours(db_store_timings)
        self.opening_hours_week = self.calculate_store_opening_hours_week(
            self.buisness_hours
        )

        self.db_store_status_logs = db_store_status_logs

        self.uptime_last_hour = 0
        self.downtime_last_hour = 0

        self.uptime_last_day = 0
        self._downtime_last_day = 0

        self.uptime_last_week = 0
        self.downtime_last_week = 0

    def calculate_buisness_hours(self, store_timings: List[Row]):

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
            start_time = str(row.Menu_Hours.start_time_local)
            end_time = str(row.Menu_Hours.end_time_local)

            buisness_hours[day].append(
                [
                    start_time,
                    end_time,
                ]
            )

        return buisness_hours

    def calculate_store_opening_hours_week(self, buisness_hours: Dict[int, List]):
        """Total time (Rounded) a store is supposed to be open for in a week"""

        opening_hours = 0

        for day in buisness_hours:
            for schedule in buisness_hours[day]:
                opening_hours += time_difference(
                    schedule[1], schedule[0], self.date_today
                )

        return opening_hours

    # def get_last_day(self):
    #     """Get the number of the last day for which the status was logged"""

    #     for status in range(len(self.db_store_status_logs)-1, 0, -1):
    #         pass

    def uptime_downtime_last_hour(self):
        """Uptime and downtime for the last recorded hour.\n
        1. Fetch all logs that have data regarding last hour
        2.
        """
        uptime = downtime = 0

    def uptime_downtime_day(self, day):
        """Uptime and downtime for a day.\n
        What I already have?
        1. A list containing hourly status of the store.
        2. A dictionary containing opening hours of the store.

        Approach?
        1. Find exactly where does the fist status lies for the particular day in the status list.
        2. Calculate what day was the last status recorded.
        3. I now have the last day statuses and the store timings for that day.
        4. Iterate through each status and calculate if it lies within the store open timings and if the status shows active or inactive.
        5. This method can also be used to get the total uptime and downtime for a whole week.
        """

        uptime = downtime = 0

        buisness_hours_on_day = self.buisness_hours[day]

        for i in self.db_store_status_logs:
            pretty_print(i)
        pretty_print(buisness_hours_on_day)
        print(day)

        # print(uptime, downtime)

    def uptime_downtime_last_week(self):
        uptime = downtime = 0

    def get_calculated_data(self):
        # self.uptime_downtime_last_hour()

        # Get last recorded day from logs
        # What if db_store_status_logs is empty?
        day = get_day_of_week_from_utc(
            self.db_store_status_logs[-1].Store_Status.timestamp_utc
        )
        self.uptime_downtime_day(day)
        # self.uptime_downtime_last_week()

        return [
            self.store_id,
            self.uptime_last_hour,
            self.uptime_last_day,
            self.uptime_last_week,
            self.downtime_last_hour,
            self._downtime_last_day,
            self.downtime_last_week,
        ]
