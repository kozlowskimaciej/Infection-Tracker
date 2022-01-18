from infection_tracker.ui.tui_ui import TUI_UI


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
    pass


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
    pass


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
    pass


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
    pass


def fake_input_remove_disease_valid(input):
    return_value = {
        "Disease's name: ": "Covid-19",
        "Disease's infectious period in minutes: ": "123",
        "Disease to remove (index): ": "1"
    }
    return return_value[input]


def test_show_remove_disease_valid(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_remove_disease_valid)
    ui = TUI_UI()
    ui._add_disease()
    assert ui._remove_disease() == "Disease removed."
    pass


def fake_input_remove_disease_invalid_index(input):
    return_value = {
        "Disease's name: ": "Covid-19",
        "Disease's infectious period in minutes: ": "123",
        "Disease to remove (index): ": "2"
    }
    return return_value[input]


def test_show_remove_disease_invalid_index(monkeypatch):
    monkeypatch.setattr('builtins.input',
                        fake_input_remove_disease_invalid_index)
    ui = TUI_UI()
    ui._add_disease()
    assert ui._remove_disease() == "Wrong index"
    pass
