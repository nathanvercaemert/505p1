from parser import datetime

class logEntry:
    def __init__(self, entry):
        self.entry = entry
        self.datetime = datetime.fromisoformat(self.entry[:25])

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime
