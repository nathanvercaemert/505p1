from parser import datetime


class logEntry:
    def __init__(self, entry):
        self.entry = entry
        datetimeString = str(self.entry[:25])
        datetimeString = datetimeString[2:]
        datetimeString = datetimeString[:-1]
        self.datetime = datetime.fromisoformat(datetimeString)

    def isLessThan(self, other):
        selfDatetimeString = str(self.entry[:25])
        selfDatetimeString = selfDatetimeString[2:]
        selfDatetimeString = selfDatetimeString[:-1]
        selfDatetimeObject = datetime.fromisoformat(selfDatetimeString)
        otherDatetimeString = str(other.entry[:25])
        otherDatetimeString = otherDatetimeString[2:]
        otherDatetimeString = otherDatetimeString[:-1]
        otherDatetimeObject = datetime.fromisoformat(otherDatetimeString)
        return selfDatetimeObject < otherDatetimeObject

    def isLessThanOrEqual(self, other):
        selfDatetimeString = str(self.entry[:25])
        selfDatetimeString = selfDatetimeString[2:]
        selfDatetimeString = selfDatetimeString[:-1]
        selfDatetimeObject = datetime.fromisoformat(selfDatetimeString)
        otherDatetimeString = str(other.entry[:25])
        otherDatetimeString = otherDatetimeString[2:]
        otherDatetimeString = otherDatetimeString[:-1]
        otherDatetimeObject = datetime.fromisoformat(otherDatetimeString)
        return selfDatetimeObject <= otherDatetimeObject

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime
