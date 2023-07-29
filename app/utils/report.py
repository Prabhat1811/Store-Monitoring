import os
from json import dumps
from typing import List

from sqlalchemy.engine.row import Row

from app.utils.utils import *

from .db_operations import *
from .lock import Lock


class Store:
    def __init__(self, store_id, local_timezone, date_today, store_timings):
        self.store_id = store_id
        self.local_timezone = local_timezone
        self.date_today = date_today

        self.buisness_hours = self.calculate_buisness_hours(store_timings)
        self.opening_hours_week = self.calculate_store_opening_hours_week(
            self.buisness_hours, date_today
        )

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

    def calculate_store_opening_hours_week(self, buisness_hours, common_date):
        """Total time (Rounded) a store is supposed to be open for in a week"""

        opening_hours = 0

        for day in buisness_hours:
            for schedule in buisness_hours[day]:
                opening_hours += time_difference(schedule[1], schedule[0], common_date)

        return opening_hours

    def uptime_downtime_last_hour(self):
        """Uptime and downtime for the last recorded hour.
        1. Fetch all logs that have data regarding last hour
        2.
        """

    def uptime_downtime_last_day(self, store_status, buisness_hours):
        """Uptime and downtime for the last recorded day.
        What I already have?
        1. A list containing hourly status of the store.
        2. A dictionary containing opening hours of the store.

        Approach?
        1. Find exactly where does the fist status lies for the last day in the status list.
        2. Calculate what day was the last status recorded.
        3. I now have the last day statuses and the store timings for that day.
        4. Iterate through each status and calculate if it lies within the store open timings and if the status shows active or inactive.
        5. This method can also be used to get the total uptime and downtime for a whole week.
        """

    def uptime_downtime_last_week(self):
        pass

    def get_calculated_data(self):
        # self.uptime_downtime_last_hour()
        self.uptime_downtime_last_day()
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

    def pretty_print(self, data):
        # For testing
        print(dumps(data, indent=2))


class Report:
    def __init__(self):
        self.path = "./app/report"
        self.filename = "report.csv"
        self.media_type = "text/csv"
        self.headers = [
            "store_id",
            "uptime_last_hour(in minutes)",
            "uptime_last_day(in hours)",
            "update_last_week(in hours)",
            "downtime_last_hour(in minutes)",
            "downtime_last_day(in hours)",
            "downtime_last_week(in hours)",
        ]
        self.batch_size = 5000

    def generate_report(self, lock: Lock, session: Session):
        lock.acquire()

        date_today = date.today()

        # Get all store ids and their corresponding timezones
        for store_timezone in get_all_store_timezones(session):
            # store_id = store_timezone.store_id
            # local_timezone = store_timezone.timezone

            store_id = 778281888660867776
            local_timezone = "America/New_York"
            print(store_id)

            # Oening and closing times for store
            db_store_timings = get_store_timings(store_id, session)
            # print(db_store_timings.Store_Timezone.store_id)

            # Hourly(Loose) logs for store status
            db_store_status = get_store_status(store_id, session)

            store = Store(
                store_id, local_timezone, date_today, db_store_timings, db_store_status
            )

            store.get_calculated_data()

            break

        lock.release()

    def store_into_csv(self, csv_name: str, read_mode: str, data: List):
        pass

    def get_full_file_path(self):
        return os.path.join(os.getcwd(), self.path, self.filename)

    def exists(self):
        file = self.get_full_file_path()
        return os.path.exists(file)
