import uuid
from datetime import datetime, timedelta
from infection_tracker.exceptions import InvalidDateError


class Meeting:
    def __init__(self, person1, person2, date, duration):

        try:
            date = datetime.fromisoformat(date)
            duration = timedelta(minutes=int(duration))
        except ValueError:
            raise InvalidDateError(date)

        # Creating an universally unique identifier for a meeting
        self._uuid = uuid.uuid4()
        self._person1 = person1
        self._person2 = person2
        self._date = date
        self._duration = duration

    def duration(self):
        return self._duration

    def people(self):
        return (self._person1, self._person2)

    def person1(self):
        return self._person1

    def person2(self):
        return self._person2

    def date(self):
        return self._date

    def uuid(self):
        return self._uuid
