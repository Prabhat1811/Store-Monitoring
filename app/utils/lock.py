class Lock:
    def __init__(self):
        self.__applied = False
        self.__is_broken = False

    def acquire(self):
        if self.__is_broken:
            return

        self.__applied = True
        print("Lock acquired!")

    def release(self):
        self.__applied = False
        print("Lock released!")

    def is_applied(self):
        return self.__applied

    def shatter(self):
        """
        This is just for testing purposes.
        It will break the lock beyond repair.
        """
        self.__applied = False
        self.__is_broken = True
