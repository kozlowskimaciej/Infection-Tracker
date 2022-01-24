from infection_tracker.files import (write_file_infected_handled,
                                     read_meetings_csv_handled)
from infection_tracker.exceptions import (InvalidDateError,
                                          InvalidDurationError)
from io import StringIO
import pytest


def test_read_meetings_csv():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,165"
    file_handle = StringIO(data)
    people = read_meetings_csv_handled(file_handle)
    assert "Sofia Baker" in people.keys()
    assert "Marcus Moore" in people.keys()


def test_read_meetings_csv_two_rows():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,165\n"
    data += "Jenna,Payne,Vanessa,Reed,2021-12-01 14:31,36"
    file_handle = StringIO(data)
    people = read_meetings_csv_handled(file_handle)
    assert "Sofia Baker" in people.keys()
    assert "Marcus Moore" in people.keys()
    assert "Jenna Payne" in people.keys()
    assert "Vanessa Reed" in people.keys()


def test_read_meetings_csv_invalid_date():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-49 12:48,165"
    file_handle = StringIO(data)
    with pytest.raises(InvalidDateError):
        read_meetings_csv_handled(file_handle)


def test_read_meetings_csv_invalid_duration():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,abc"
    file_handle = StringIO(data)
    with pytest.raises(InvalidDurationError):
        read_meetings_csv_handled(file_handle)


def test_read_meetings_csv_invalid_data():
    data = "Name_1,Surname_1,Name_2,Surname_2,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,abc"
    file_handle = StringIO(data)
    with pytest.raises(Exception):
        read_meetings_csv_handled(file_handle)


def test_write_file_infected_handled():
    data = "Sofia Baker"
    file_handle = StringIO()
    write_file_infected_handled(file_handle, data)
    assert file_handle.getvalue() == "Sofia Baker"
