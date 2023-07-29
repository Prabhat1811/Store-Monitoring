import os
from datetime import date
from typing import List

from .db_operations import *
from .lock import Lock
from .store import Store

# from app.utils.utils import *


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
            db_store_status_logs = get_store_status_logs(store_id, session)

            store = Store(
                store_id,
                local_timezone,
                date_today,
                db_store_timings,
                db_store_status_logs,
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
