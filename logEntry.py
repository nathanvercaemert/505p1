import dateutil.parser
class logEntry:
    def __init__(self, entry):
        self.entry = entry
        self.datetime = dateutil.parser.isoparse(self.entry[:25])

    def __lt__(self, other):
        return self.datetime < other.datetime
