from infection_tracker.disease import Disease
from infection_tracker.person import Person
from infection_tracker.exceptions import (InvalidInfectiousPeriodError)
from datetime import datetime
from infection_tracker.files import read_meetings_csv
from prettytable import PrettyTable


class TUI_UI:
    '''
    Text-based user interface

    Class TUI_UI. Conatins attributes:
    :param diseases: Stores diseases objects
    :type diseases: list

    :param meetings: Stores meetings objects
    :type meetings: set

    :param people: Stores people objects
    :type people: dict
    '''
    def __init__(self) -> None:
        '''
        Initalizes text-based user interface
        '''
        self._diseases = []
        self._meetings = set()
        self._people = dict()

    def show(self) -> None:
        '''
        Shows UI
        '''

        # Define all possible choices
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
            },
            "9": {
                "message": "Exit.",
                "function": exit
            }
        }

        print('INFECTION TRACKER')

        # Main loop for displaying UI
        while True:
            # Print choices with description
            for choice in choices:
                print(choice+". ", choices[choice]["message"], sep=" ")
            choice_num = input("What's your choice: ")

            # Try running the function from the dictionary
            try:
                print(choices[choice_num]["function"]())
            except Exception:
                print("Invalid choice.")

            print("\n")

    def _add_meeting(self) -> str:
        '''
        Adds a meeting to the database
        '''
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

        # If a person doesn't exist, create a new Person object
        # and add to database
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

        # Adds meeting to both people's meeting list
        person1.add_meeting(person2, date, duration)

        return "Meeting added."

    def _remove_meeting(self) -> str:
        '''
        Removes a meeting from the database
        '''
        print(self._show_meetings())

        uuid = input("Meeting's UUID: ")

        # Browse through all meetings to find the ones
        # that need to be removed.
        for person in self._people:
            self._people[person].remove_meeting(uuid)

        # Rebuild meetings database after removing a meeting
        self._set_meetings()
        return f"Meeting {uuid} removed."

    def _show_meetings(self) -> PrettyTable:
        '''
        Builds a table that contains all meetings from meetings database
        '''

        # Rebuild meetings database to make sure it's up-to-date
        self._set_meetings()

        table = PrettyTable()

        # Add field names and rows to the table
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

    def _add_disease(self) -> str:
        '''
        Adds the disease to the database
        '''
        name = input("Disease's name: ")
        period = input(
            "Disease's infectious period in minutes: "
            )

        # Try to create disease object
        try:
            disease = Disease(name, period)
        except InvalidInfectiousPeriodError:
            return "Invalid period."

        # Add the disease to database
        self._diseases.append(disease)
        return "Disease added."

    def _remove_disease(self) -> str:
        '''
        Removes the disease from the database
        '''

        # Show a table with the diseases
        print(self._show_diseases())
        choice_num = input(
            "Disease to remove (index): "
            )

        # Try to remove the disease from given index
        try:
            self._diseases.pop(int(choice_num)-1)
        except IndexError:
            return "Wrong index"

        return "Disease removed."

    def _show_diseases(self) -> PrettyTable:
        '''
        Builds a table that contains all diseases from diseases database
        '''
        table = PrettyTable()
        table.field_names = (
            ["Index", "Name", "Infectious period"]
        )

        # Get indexes (which starts from 0 to n but we want to display them
        # from 1 to n+1, that's why there is str(index+1)), disease's name,
        # infectious period and make a row.
        for index, disease in enumerate(self._diseases):
            table.add_row([str(index+1)+".",
                           disease.__str__(),
                           disease.get_infectious_period()])

        return table

    def _get_infected_people_list(self) -> str:
        '''
        Returns a list with infected people.
        '''
        infected = input("Full name of infected person: ")

        # Check if person exists in people database
        try:
            infected = self._people[infected]
        except KeyError:
            return "This person does not exist."

        date = input(
            "Patient diagnosed (ISO 8601, e.g. 2021-12-04 01:02): "
            )

        # Check if the date is in correct format
        try:
            datetime.fromisoformat(date)
        except Exception:
            return "Wrong date."

        # Show available diseases
        print(self._show_diseases())
        disease = input(
            "Choose disease (index): "
            )

        # Check if the index is correct
        try:
            disease = self._diseases[int(disease)-1]
        except Exception:
            return "Wrong index."

        # Get a list with infected people
        infected_list = infected.who_is_infected(disease, date)

        # Make a string from list
        infected_list = ", ".join(infected_list)

        return infected_list

    def _import_meetings(self) -> str:
        '''
        Imports meetings from CSV file.
        '''
        path = input("CSV file's path: ")

        # Try to import meetings
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

    def _set_meetings(self) -> None:
        '''
        Builds meetings database from people's meetings
        '''
        meetings = []

        # Add all meetings from people database
        for person in self._people:
            meetinglist = self._people[person].meetings()
            for meeting in meetinglist:
                meetings.append(meeting)

        # Convert list to set to get rid of duplicates and
        # make it a meetings database
        self._meetings = set(meetings)
