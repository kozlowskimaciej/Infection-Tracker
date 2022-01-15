from infection_tracker.files import (read_meetings_csv,
                                     write_file_infected,
                                     read_meetings)
from infection_tracker.exceptions import (InvalidDateError,
                                          InvalidDurationError)
from io import StringIO
import pytest


def test_read_meetings_csv():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,165"
    file_handle = StringIO(data)
    people = read_meetings(file_handle)
    assert "Sofia Baker" in people.keys()
    assert "Marcus Moore" in people.keys()


def test_read_meetings_csv_invalid_date():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-49 12:48,165"
    file_handle = StringIO(data)
    with pytest.raises(InvalidDateError):
        read_meetings(file_handle)


def test_read_meetings_csv_invalid_duration():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,abc"
    file_handle = StringIO(data)
    with pytest.raises(InvalidDurationError):
        read_meetings(file_handle)


def test_read_meetings_csv_invalid_data():
    data = "Name_1,Surname_1,Name_2,Surname_2,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,abc"
    file_handle = StringIO(data)
    with pytest.raises(Exception):
        read_meetings(file_handle)


def test_read_meetings_csv_invalid_path():
    with pytest.raises(FileNotFoundError):
        read_meetings_csv("tests/example_data/invalid.csv")
