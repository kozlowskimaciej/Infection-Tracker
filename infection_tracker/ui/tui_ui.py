from infection_tracker.disease import Disease
from infection_tracker.person import Person
from infection_tracker.exceptions import (InvalidInfectiousPeriodError)
from datetime import datetime
from infection_tracker.files import read_meetings_csv
from prettytable import PrettyTable


class TUI_UI:
    '''
    Text-based user interface
    '''
    def __init__(self):
        self._diseases = []
        self._meetings = set()
        self._people = dict()
        choices = {
            "1": {
                "message": "Add a meeting",
                "function": self._add_meeting
            },
            "2": {
                "message": "Remove a meeting",
                "function": self._remove_meeting
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
            }
        }

        print('INFECTION TRACKER')

        while True:
            print("\n")
            for choice in choices:
                print(choice+". ", choices[choice]["message"], sep=" ")
            choice_num = input("What's your choice: ")
            try:
                print(choices[choice_num]["function"]())
            except Exception:
                print("Invalid choice.")
            print("\n")

    def _add_meeting(self):
        person1name = input("First name of first person: ")
        person1sur = input("Last name of first person: ")
        person1full = f"{person1name} {person1sur}"

        person2name = input("First name of second person: ")
        person2sur = input("Last name of second person: ")
        person2full = f"{person2name} {person2sur}"

        date = input("Date of meeting (ISO 8601, e.g. 2021-12-04 21:02): ")
        try:
            datetime.fromisoformat(date)
        except Exception:
            return "Wrong date."

        duration = input("Meeting duration in minutes: ")
        try:
            duration = int(duration)
        except Exception:
            return "Wrong duration."

        if self._people.get(person1full) is None:
            person1 = Person(person1name, person1sur)
            self._people[person1full] = person1
        else:
            person1 = self._people.get(person1full)

        if self._people.get(person2full) is None:
            person2 = Person(person2name, person2sur)
            self._people[person2full] = person2
        else:
            person2 = self._people.get(person2full)

        person1.add_meeting(person2, date, duration)

        return "Meeting added."

    def _remove_meeting(self):
        uuid = input("Meeting's UUID: ")
        for person in self._people:
            self._people[person].remove_meeting(uuid)
        self._set_meetings()
        return f"Meeting {uuid} removed."

    def _show_meetings(self):
        self._set_meetings()
        table = PrettyTable()
        table.field_names = (
            ["UUID", "Person 1", "Person 2", "Date", "Duration"]
        )
        for meeting in self._meetings:
            table.add_row(
                [meeting.uuid(),
                 meeting.person1(),
                 meeting.person2(),
                 meeting.date(),
                 meeting.duration()]
                )
        return table

    def _add_disease(self):
        name = input("Disease's name: ")
        period = input(
            "Disease's infectious period in minutes: "
            )
        try:
            disease = Disease(name, period)
        except InvalidInfectiousPeriodError:
            return "Invalid period."
        self._diseases.append(disease)
        return "Disease added."

    def _remove_disease(self):
        self._show_diseases()
        choice_num = input(
            "Disease to remove (index): "
            )

        try:
            self._diseases.pop(int(choice_num)-1)
        except IndexError:
            return "Wrong index"

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
        try:
            infected = self._people[infected]
        except KeyError:
            return "This person does not exist."

        date = input(
            "Patient diagnosed (ISO 8601, e.g. 2021-12-04 21:02): "
            )
        try:
            datetime.fromisoformat(date)
        except Exception:
            return "Wrong date."

        print(self._show_diseases())
        disease = input(
            "Choose disease (index): "
            )
        try:
            disease = self._diseases[int(disease)-1]
        except Exception:
            return "Wrong index."

        infected_list = infected.who_is_infected(disease, date)

        infected_list = ", ".join(infected_list)

        return infected_list

    def _import_meetings(self):
        path = input("CSV file's path: ")
        try:
            self._people = read_meetings_csv(path)
            return "Imported."
        except FileNotFoundError:
            return f"No file was found in {path}."
        except IsADirectoryError:
            return f"{path} is not CSV file's path."
        except PermissionError:
            return f"You do not have permission to access {path}."
        except Exception:
            return "Invalid data."

    def _set_meetings(self):
        meetings = []
        for person in self._people:
            meetinglist = self._people[person].meetings()
            for meeting in meetinglist:
                meetings.append(meeting)
        self._meetings = set(meetings)
