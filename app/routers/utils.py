import os
from time import sleep


class Report:
    """
    Class containing methods related to reports
    """

    def __init__(self):
        self.__lock = False
        self.path = "./app/report"
        self.filename = "report.csv"
        self.media_type = "text/csv"

    def generate_report(self):
        self.__lock = True
        print("Report triggered. Please wait...")
        sleep(10)
        print("Report generation complete.")
        self.__lock = False

    def is_locked(self):
        return self.__lock

    def get_full_file_path(self):
        return os.path.join(os.getcwd(), self.path, self.filename)

    def exists(self):
        file = self.get_full_file_path()
        return os.path.exists(file)
