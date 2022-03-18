from parser import isoparse

class logEntry:
    def __init__(self, entry):
        self.entry = entry
        self.datetime = isoparse(self.entry[:25])

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime
