import uuid
from datetime import datetime, timedelta
from infection_tracker.exceptions import (InvalidDateError,
                                          InvalidDurationError)


class Meeting:
    '''
    Class Meeting. Contains attributes:

    :param uuid: Meeting's id
    :type uuid: str

    :param person1: First person
    :type person1: Person

    :param person2: Second person
    :type person2: Person

    :param date: Meeting's date
    :type date: datetime

    :param duration: Meeting's duration
    :type duration: timedelta
    '''
    def __init__(self,
                 person1,
                 person2,
                 date: str,
                 duration: int) -> None:
        '''
        Initializes Meeting object
        '''

        # Try to convert date string to datetime object
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            raise InvalidDateError(date)

        # Try to convert duration string to timedelta object
        try:
            duration = timedelta(
                minutes=abs(int(duration)))
        except ValueError:
            raise InvalidDurationError(duration)

        # Create an universally unique identifier for a meeting
        self._uuid = uuid.uuid4()
        self._person1 = person1
        self._person2 = person2
        self._date = date
        self._duration = duration

    def duration(self) -> timedelta:
        '''
        Returns meeting's duration
        '''
        return self._duration

    def people(self) -> tuple:
        '''
        Returns both people that had a meeting
        '''
        return (self._person1, self._person2)

    def person1(self):
        '''
        Returns first person from meeting
        '''
        return self._person1

    def person2(self):
        '''
        Returns second person from meeting
        '''
        return self._person2

    def date(self) -> datetime:
        '''
        Returns meeting's date
        '''
        return self._date

    def uuid(self) -> str:
        '''
        Returns meeting's id
        '''
        return self._uuid
