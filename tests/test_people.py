from infection_tracker.person import (
    Person,
    InvalidDiseaseError,
    InvalidMeetingDateError,
    InvalidPersonError
)
from infection_tracker.disease import Disease
from datetime import datetime, timedelta
import pytest


def test_person_valid_no_meetings():
    person = Person("Chelsy", "Southern")
    assert person.__str__() == "Chelsy Southern"
    assert person.meetings() == []


def test_person_meeting_valid():
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    person1.add_meeting(person2, "21.12.2019 2:00", 257)
    assert person1.meetings()[0]["date"] == datetime(2019, 12, 21, 2, 0)
    assert person1.meetings()[0]["duration"] == timedelta(minutes=257)
    assert person1.meetings()[0]["person"] == person2


def test_person_meeting_invalid_date():
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    with pytest.raises(InvalidMeetingDateError):
        person1.add_meeting(person2, "21.13.2019 2:00", 257)


def test_person_meeting_invalid_time():
    person1 = Person("Chelsy", "Southern")
    person2 = Person("Cally", "Fletcher")
    with pytest.raises(InvalidMeetingDateError):
        person1.add_meeting(person2, "21.12.2019 25:70", 257)


def test_person_meeting_invalid_person():
    person = Person("Chelsy", "Southern")
    with pytest.raises(InvalidPersonError):
        person.add_meeting("Chelsy Southern", "21.12.2019 20:10", 257)


def test_who_is_infected_invalid_disease():
    person = Person("Chelsy", "Southern")
    with pytest.raises(InvalidDiseaseError):
        person.who_is_infected("disease")


def test_who_is_infected_list_valid():
    '''
    person4 nie został wypisany, poniewaz spotkal sie z person3,
    zanim ten zostal zarazony przez person2
    '''
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person3 = Person("Jasper", "Haworth")
    person4 = Person("Jackson", "Black")
    person1.add_meeting(person2, "19.12.2021 1:00", 60)
    person1.add_meeting(person2, "19.12.2021 3:00", 60)
    person2.add_meeting(person3, "19.12.2021 4:00", 60)
    person3.add_meeting(person4, "19.12.2021 1:00", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease) == (
        {'Jasper Haworth', 'Cally Fletcher', 'Carson Keeling'})


def test_who_is_infected_list_only_self():
    '''
    nikt sie nie spotkal z person1, wiec nikogo nie zarazil
    '''
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person3 = Person("Jasper", "Haworth")
    person4 = Person("Jackson", "Black")
    person4.add_meeting(person2, "19.12.2021 1:00", 60)
    person4.add_meeting(person2, "19.12.2021 3:00", 60)
    person2.add_meeting(person3, "19.12.2021 4:00", 60)
    person3.add_meeting(person4, "19.12.2021 1:00", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease) == {'Carson Keeling'}


def test_who_is_infected_list_only_one():
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person3 = Person("Jasper", "Haworth")
    person4 = Person("Jackson", "Black")
    person4.add_meeting(person2, "19.12.2021 1:00", 60)
    person4.add_meeting(person2, "19.12.2021 3:00", 60)
    person4.add_meeting(person3, "19.12.2021 4:00", 60)
    person1.add_meeting(person4, "19.12.2021 5:00", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease) == (
        {'Carson Keeling', 'Jackson Black'})


def test_who_is_infected_list_infection_duration_pass():
    '''
        person4 pomimo spotkania z zarazonym person2 nie zostal zarazonym,
        bo czas zarazliwosci zostal przekroczony o minute
    '''
    person1 = Person("Carson", "Keeling")
    person2 = Person("Cally", "Fletcher")
    person4 = Person("Jackson", "Black")
    person1.add_meeting(person2, "19.12.2021 1:00", 120)
    person4.add_meeting(person2, "19.12.2021 3:31", 60)
    disease = Disease("Covid-19", 30)
    assert person1.who_is_infected(disease) == (
        {'Carson Keeling', 'Cally Fletcher'})
