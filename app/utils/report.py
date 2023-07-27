import os

from .db_operations import *
from .lock import Lock


class Report:
    def __init__(self):
        self.path = "./app/report"
        self.filename = "report.csv"
        self.media_type = "text/csv"

    def generate_report(self, lock: Lock, session: Session):
        lock.acquire()

        get_store_ids(session)

        lock.release()

    def get_full_file_path(self):
        return os.path.join(os.getcwd(), self.path, self.filename)

    def exists(self):
        file = self.get_full_file_path()
        return os.path.exists(file)
