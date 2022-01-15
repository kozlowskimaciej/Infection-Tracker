from infection_tracker.exceptions import (InvalidDateError,
                                          InvalidDiseaseError,
                                          InvalidPersonError)
from infection_tracker.person import Person
from infection_tracker.disease import Disease
from datetime import datetime, timedelta
import pytest


def test_person_str():
    person = Person("Chelsy", "Southern")
    assert person.__str__() == "Chelsy Southern"


def test_person_empty_meeting_list():
    person = Person("Chelsy", "Southern")
    assert person.__str__() == "Chelsy Southern"
    assert person.meetings() == []


def test_person_two_people_meeting_list():
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    person1.add_meeting(person2, "2019-12-21 02:00", 257)
    person1_meeting = person1.meetings()[0]
    person2_meeting = person2.meetings()[0]
    assert person1_meeting == person2_meeting
    assert person1_meeting.uuid() == person2_meeting.uuid()
    assert person1 in person1_meeting.people()
    assert person2 in person1_meeting.people()
    assert person1_meeting.date() == datetime.fromisoformat("2019-12-21 02:00")
    assert person1_meeting.duration() == timedelta(minutes=257)


def test_person_meeting_invalid_date():
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    with pytest.raises(InvalidDateError):
        person1.add_meeting(person2, "2019-13-21 02:00", 257)


def test_person_meeting_invalid_time():
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    with pytest.raises(InvalidDateError):
        person1.add_meeting(person2, "2019-12-21 25:70", 257)


def test_person_meeting_invalid_person():
    person = Person("Chelsy", "Southern")
    with pytest.raises(InvalidPersonError):
        person.add_meeting("Chelsy Southern", "2019-12-21 20:10", 257)


def test_person_remove_meeting_one():
    people = []
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    person1.add_meeting(person2, "2019-12-21 02:00", 257)
    people.append(person1)
    people.append(person2)
    meeting_uuid = person1.meetings()[0].uuid()
    for person in people:
        assert person.remove_meeting(meeting_uuid) is True
    assert person1.meetings() == person2.meetings()
    assert person1.meetings() == []


def test_person_remove_meeting_two():
    people = []
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    person1.add_meeting(person2, "2019-12-21 02:00", 257)
    person1.add_meeting(person2, "2019-12-22 12:44", 120)
    people.append(person1)
    people.append(person2)
    meeting1_uuid = person1.meetings()[0].uuid()
    meeting2_uuid = person1.meetings()[1].uuid()
    for person in people:
        assert person.remove_meeting(meeting1_uuid) is True
    assert person1.meetings() == person2.meetings()
    assert person1.meetings()[0].uuid() == meeting2_uuid


def test_person_remove_meeting_empty():
    people = []
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    people.append(person1)
    people.append(person2)
    meeting_uuid = "uuid"
    for person in people:
        assert person.remove_meeting(meeting_uuid) is False
    assert person1.meetings() == person2.meetings()
    assert person1.meetings() == []


def test_person_who_is_infected_invalid_disease():
    person = Person("Chelsy", "Southern")
    with pytest.raises(InvalidDiseaseError):
        person.who_is_infected("disease", "2019-12-21 20:10")


def test_person_who_is_infected_list_valid():
    '''
    Person4 is not infected, because he had met Person3 before
    Person3 had been infected by Person2
    '''
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person3 = Person("Jasper", "Haworth")
    person4 = Person("Jackson", "Black")
    person1.add_meeting(person2, "2021-12-19 01:00", 60)
    person3.add_meeting(person4, "2021-12-19 01:00", 60)
    person1.add_meeting(person2, "2021-12-19 03:00", 60)
    person2.add_meeting(person3, "2021-12-19 04:00", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease, "2021-12-19 03:30") == (
        {'Jasper Haworth', 'Cally Fletcher', 'Carson Keeling'})


def test_person_who_is_infected_list_only_self():
    '''
    Person1 didn't have any meetings therefore no one was infected
    '''
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person3 = Person("Jasper", "Haworth")
    person4 = Person("Jackson", "Black")
    person4.add_meeting(person2, "2021-12-19 01:00", 60)
    person4.add_meeting(person2, "2021-12-19 03:00", 60)
    person2.add_meeting(person3, "2021-12-19 04:00", 60)
    person3.add_meeting(person4, "2021-12-19 01:00", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease, "2021-12-19 03:30") == (
        {'Carson Keeling'})


def test_person_who_is_infected_list_only_one():
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person3 = Person("Jasper", "Haworth")
    person4 = Person("Jackson", "Black")
    person4.add_meeting(person2, "2021-12-19 01:00", 60)
    person4.add_meeting(person2, "2021-12-19 03:00", 60)
    person4.add_meeting(person3, "2021-12-19 04:00", 60)
    person1.add_meeting(person4, "2021-12-19 05:00", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease, "2021-12-19 05:30") == (
        {'Carson Keeling', 'Jackson Black'})


def test_person_who_is_infected_list_infection_duration_pass():
    '''
        Infectious period was exceeded by a minute (after the first meeting
        has finished at 3:00, the infectious period was 30 minutes and at
        3:31 it wasn't infectious anymore) so Person4 was not infected.
    '''
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person4 = Person("Jackson", "Black")
    person1.add_meeting(person2, "2021-12-19 01:00", 120)
    person4.add_meeting(person2, "2021-12-19 03:31", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease, "2021-12-19 01:30") == (
        {'Carson Keeling', 'Cally Fletcher'})
