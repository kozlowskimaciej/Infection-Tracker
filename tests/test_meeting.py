from infection_tracker.meeting import Meeting
from infection_tracker.person import Person
from infection_tracker.exceptions import InvalidDateError, InvalidDurationError
from datetime import datetime, timedelta
import pytest


def test_meeting_valid():
    person1 = Person("Name1", "Surname1")
    person2 = Person("Name2", "Surname2")
    date = "2022-01-15 09:21"
    duration = 120
    meeting = Meeting(person1, person2, date, duration)
    assert person1 in meeting.people()
    assert person2 in meeting.people()
    assert meeting.date() == datetime.fromisoformat(date)
    assert meeting.duration() == timedelta(minutes=duration)


def test_meeting_invalid_date():
    person1 = Person("Name1", "Surname1")
    person2 = Person("Name2", "Surname2")
    date = "2022-01-15 9:21"
    duration = 120
    with pytest.raises(InvalidDateError):
        Meeting(person1, person2, date, duration)


def test_meeting_invalid_duration():
    person1 = Person("Name1", "Surname1")
    person2 = Person("Name2", "Surname2")
    date = "2022-01-15 09:21"
    duration = "abc"
    with pytest.raises(InvalidDurationError):
        Meeting(person1, person2, date, duration)


def test_meeting_two_unique_ids():
    person1 = Person("Name1", "Surname1")
    person2 = Person("Name2", "Surname2")
    meeting1 = Meeting(person1, person2, "2022-01-15 09:21", 120)
    meeting2 = Meeting(person1, person2, "2022-01-16 12:13", 90)
    assert meeting1.uuid() != meeting2.uuid()
    assert meeting1.people() == meeting2.people()
