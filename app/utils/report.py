import csv
import os
from datetime import date
from typing import Any, List

from tqdm import tqdm

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
        self.batch_size = 2000

    def generate_report(self, lock: Lock, session: Session):
        lock.acquire()

        self.store_to_csv("w+", [self.headers])

        date_today = date.today()

        batch = []
        # Get all store ids and their corresponding timezones
        for i, store_timezone in enumerate(tqdm(get_all_store_timezones(session))):
            store_id = store_timezone.store_id
            local_timezone = store_timezone.timezone

            # store_id = 7681219113084292190
            # local_timezone = "America/Chicago"
            # print(store_id)

            # Opening and closing times for store
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

            batch.append(store.calculate_data())

            del store

            # return

            if len(batch) >= self.batch_size:
                try:
                    self.store_to_csv("a+", batch)
                    batch = []
                except:
                    lock.release()
                    print("Error inserting. Check fields")
                    return

        if batch:
            try:
                self.store_to_csv("a+", batch)
            except:
                lock.release()
                print("Error inserting. Check fields")
                return

        lock.release()

    def store_to_csv(self, open_mode: str, data: List[List[Any]]):

        with open(f"{self.path}/{self.filename}", open_mode) as csv_file:
            writer = csv.writer(csv_file)

            writer.writerows(data)

    def get_full_file_path(self):
        return os.path.join(os.getcwd(), self.path, self.filename)

    def exists(self):
        file = self.get_full_file_path()
        return os.path.exists(file)
