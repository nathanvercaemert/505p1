from parser import datetime


class logEntry:
    def __init__(self, entry):
        self.entry = entry
        datetimeString = str(self.entry[:25])
        datetimeString = datetimeString[2:]
        datetimeString = datetimeString[:-1]
        self.datetime = datetime.fromisoformat(datetimeString)

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime
