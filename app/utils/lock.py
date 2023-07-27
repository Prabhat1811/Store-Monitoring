class Lock:
    def __init__(self):
        self.__lock = False

    def acquire(self):
        self.__lock = True
        print("Lock aquired!")

    def release(self):
        self.__lock = False
        print("Lock released!")

    def is_locked(self):
        return self.__lock
