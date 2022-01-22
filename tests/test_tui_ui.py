from infection_tracker.ui.tui_ui import TUI_UI
from infection_tracker.files import read_meetings_csv_handled
from io import StringIO


def fake_input_get_infected_people_list_person_invalid(input):
    return_value = {
        "Full name of infected person: ": "Mike Wazowsky",
    }
    return return_value[input]


def test_get_infected_people_list_person_invalid(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_get_infected_people_list_person_invalid)
    ui = TUI_UI()._get_infected_people_list()
    assert ui == "This person does not exist."


def fake_input_add_disease(input):
    return_value = {
        "Disease's name: ": "Covid-19",
        "Disease's infectious period in minutes: ": "1200"
    }
    return return_value[input]


def test_show_add_disease(monkeypatch):
    monkeypatch.setattr('builtins.input', fake_input_add_disease)
    ui = TUI_UI()._add_disease()
    assert ui == "Disease added."


def test_show_diseases(monkeypatch):
    monkeypatch.setattr('builtins.input', fake_input_add_disease)
    ui = TUI_UI()
    assert ui._add_disease() == "Disease added."

    diseases_table = str(ui._show_diseases())
    assert "Covid-19" in diseases_table
    assert "20:00:0" in diseases_table


def fake_input_add_disease_invalid_period(input):
    return_value = {
        "Disease's name: ": "Covid-19",
        "Disease's infectious period in minutes: ": "abc"
    }
    return return_value[input]


def test_show_add_disease_invalid_period(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_add_disease_invalid_period)
    ui = TUI_UI()._add_disease()
    assert ui == "Invalid period."


def fake_input_add_disease_valid(input):
    return_value = {
        "Disease's name: ": "Covid-19",
        "Disease's infectious period in minutes: ": "123"
    }
    return return_value[input]


def test_show_add_disease_valid(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_add_disease_valid)
    ui = TUI_UI()._add_disease()
    assert ui == "Disease added."


def fake_input_remove_disease_valid(input):
    return_value = {
        "Disease's name: ": "Covid-19",
        "Disease's infectious period in minutes: ": "1200",
        "Disease to remove (index): ": "1"
    }
    return return_value[input]


def test_remove_disease_valid(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_remove_disease_valid)
    ui = TUI_UI()
    ui._add_disease()
    diseases_table = str(ui._show_diseases())
    assert "Covid-19" in diseases_table
    assert "20:00:0" in diseases_table
    assert ui._remove_disease() == "Disease removed."
    diseases_table = str(ui._show_diseases())
    assert "Covid-19" not in diseases_table
    assert "20:00:0" not in diseases_table


def fake_input_remove_disease_invalid_index(input):
    return_value = {
        "Disease's name: ": "Covid-19",
        "Disease's infectious period in minutes: ": "123",
        "Disease to remove (index): ": "2"
    }
    return return_value[input]


def test_remove_disease_invalid_index(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_remove_disease_invalid_index)
    ui = TUI_UI()
    ui._add_disease()
    assert ui._remove_disease() == "Wrong index"


def test_import_meetings():
    data = "Name_1,Surname_1,Name_2,Surname_2,Date,Duration\n"
    data += "Sofia,Baker,Marcus,Moore,2021-12-01 12:48,165"
    file_handle = StringIO(data)
    ui = TUI_UI()
    ui._people = read_meetings_csv_handled(file_handle)

    meetings_table = str(ui._show_meetings())
    assert "Sofia Baker" in meetings_table
    assert "Marcus Moore" in meetings_table
    assert "2021-12-01 12:48" in meetings_table
    assert "2:45:00" in meetings_table


def fake_input_remove_meeting_invalid_index(input):
    return_value = {
        "Meeting's UUID: ": "abc",
    }
    return return_value[input]


def test_remove_meeting_invalid_index(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_remove_meeting_invalid_index)
    ui = TUI_UI()
    assert ui._remove_meeting() == "Meeting abc removed."
