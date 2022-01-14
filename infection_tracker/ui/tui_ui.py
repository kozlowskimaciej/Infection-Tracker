from infection_tracker.exceptions import (InvalidChoiceError,
                                          PersonNotExistsError)
from infection_tracker.disease import Disease
from infection_tracker.files import read_meetings_csv
from prettytable import PrettyTable


class TUI_UI:
    '''
    Text-based user interface
    '''
    def __init__(self):
        self._diseases = []
        self._meetings = set()
        self._people = []
        choices = {
            "1": {
                "message": "Add a meeting",
                "function": self.hello
            },
            "2": {
                "message": "Remove a meeting",
                "function": self.hello
            },
            "3": {
                "message": "Show meetings",
                "function": self._show_meetings
            },
            "4": {
                "message": "Add a disease",
                "function": self._add_disease
            },
            "5": {
                "message": "Remove a disease",
                "function": self._remove_disease
            },
            "6": {
                "message": "Show diseases",
                "function": self._show_diseases
            },
            "7": {
                "message": "Get infected people list",
                "function": self._get_infected_people_list
            },
            "8": {
                "message": "Import meetings from csv file",
                "function": self._import_meetings
            },
            "9": {
                "message": "Export meetings to csv file",
                "function": self.hello
            }
        }

        print('INFECTION TRACKER')

        while True:
            print("\n")
            for choice in choices:
                print(choice+". ", choices[choice]["message"], sep=" ")
            choice_num = input("What's your choice?\n")
            try:
                print(choices[choice_num]["function"]())
            except Exception:
                raise InvalidChoiceError(choice_num)
            print("\n")

    def _show_meetings(self):
        self._set_meetings()
        table = PrettyTable()
        table.field_names = (
            ["UUID", "Person 1", "Person 2", "Date", "Duration"]
        )
        for mt in self._meetings:
            table.add_row(
                [mt.uuid(),
                 mt.person1(),
                 mt.person2(),
                 mt.date(),
                 mt.duration()]
                )
        return table

    def _add_disease(self):
        name = input("What's the disease's name?\n")
        period = input(
            "What's the disease's infectious period (in minutes)?\n"
            )
        disease = Disease(name, period)
        self._diseases.append(disease)
        return "Disease added."

    def _remove_disease(self):
        self._show_diseases()
        choice_num = input(
            "Which disease do you want to remove?\n"
            )

        try:
            self._diseases.pop(int(choice_num)-1)
        except IndexError:
            raise InvalidChoiceError(choice_num)

        return "Disease removed."

    def _show_diseases(self):
        table = PrettyTable()
        table.field_names = (
            ["Index", "Name", "Infectious period"]
        )

        for index, disease in enumerate(self._diseases):
            table.add_row([str(index+1)+".",
                           disease.__str__(),
                           disease.get_infectious_period()])

        return table

    def _get_infected_people_list(self):
        infected = input("Full name of infected person: ")
        date = input(
            "When was the patient diagnosed (ISO 8601, e.g. 2021-12-04 21:02):"
            )
        print(self._show_diseases())
        disease = input(
            "Which disease was the patient diagnosed with (index):"
            )

        try:
            infected_list = self._people[infected].who_is_infected(
                                                self._diseases[int(disease)-1],
                                                date)
        except KeyError:
            raise PersonNotExistsError(infected)

        infected_list = ", ".join(infected_list)

        return infected_list

    def _import_meetings(self):
        path = input("What's the csv file's path?\n")
        self._people = read_meetings_csv(path)
        return "Imported."

    def _set_meetings(self):
        meetings = []
        for person in self._people:
            meetinglist = self._people[person].meetings()
            for meeting in meetinglist:
                meetings.append(meeting)
        self._meetings = set(meetings)

    def hello(self):
        print('hello')
