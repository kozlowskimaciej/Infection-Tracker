from datetime import datetime
from infection_tracker.disease import Disease
from infection_tracker.meeting import Meeting
from infection_tracker.exceptions import (InvalidDateError,
                                          InvalidDiseaseError,
                                          InvalidPersonError)


class Person:
    '''
    Class Person. Conatins attributes:
    :param name: Person's name
    :type name: str

    :param surname: Person's surname
    :type surname: str

    :param meeting_list: Person's meeting list
    :type meeting_list: list
    '''
    def __init__(self, name: str, surname: str) -> None:
        '''
        Initializes Person object
        '''
        self._name = str(name)
        self._surname = str(surname)
        self._meeting_list = []

    def add_meeting(self, person, date: str, duration: int) -> None:
        '''
        Adds new meeting to person's meeting list.
        '''
        if not isinstance(person, Person):
            raise InvalidPersonError(person)

        meeting = Meeting(self, person, date, duration)

        # Add the meeting to both people's meeting list
        self._meeting_list.append(meeting)
        person._meeting_list.append(meeting)

    def remove_meeting(self, uuid: str) -> bool:
        '''
        Removes a meeting based on it's UUID from meeting list.
        '''
        uuid = str(uuid)

        # Find matching meeting in meeting_list and remove it
        # Returns True if removed and False if not found
        for index, meeting in enumerate(self._meeting_list):
            if str(meeting.uuid()) == uuid:
                self._meeting_list.pop(index)
                return True

        return False

    def meetings(self) -> list:
        '''
        Returns person's meeting list
        '''
        return self._meeting_list

    def who_is_infected(self,
                        disease: Disease,
                        when_diagnosed: str,
                        last_meeting: Meeting = None,
                        checked_meetings: list = None,
                        infected_people: list = None) -> set:
        '''
        Returns a list of possibly infected people.
        '''

        # Try to get disease's infectious period
        try:
            infectious_period = disease.get_infectious_period()
        except Exception:
            raise InvalidDiseaseError(disease)

        # If diagnosis date is not a datetime object then try to make it one
        if not isinstance(when_diagnosed, datetime):
            try:
                when_diagnosed = datetime.fromisoformat(when_diagnosed)
            except ValueError:
                raise InvalidDateError(when_diagnosed)

        if checked_meetings is None:
            checked_meetings = []

        if infected_people is None:
            infected_people = {self.__str__()}

        if last_meeting is not None:
            last_meet_date = last_meeting.date()
            last_meet_duration = last_meeting.duration()
            total_infection = (last_meet_date + last_meet_duration)
            total_infection += infectious_period
        else:
            last_meet_date = None
            last_meet_duration = None

        # Search for all meetings which happend after the diagnosis date
        # minus infectious period of the disease
        # (only for the main infected person)
        # or the meetings that took place between
        # last meeting and last meeting plus
        # it's duration plus infectious period of the disease.

        for meeting in self._meeting_list:

            # Set second person as other_person
            people = meeting.people()
            if people[0].__str__() == self.__str__():
                other_person = people[1]
            else:
                other_person = people[0]

            if meeting.uuid() not in checked_meetings:

                meet_date = meeting.date()

                if (last_meet_date is None and
                    meet_date >= when_diagnosed - infectious_period) or (
                        last_meet_date is not None and
                        meet_date >= last_meet_date and
                        meet_date <= total_infection):
                    checked_meetings.append(meeting.uuid())
                    infected_people.add(other_person.__str__())

                    # Recursively search in other potentially infected person's
                    # meeting list for another people

                    other_person.who_is_infected(disease,
                                                 when_diagnosed,
                                                 meeting,
                                                 checked_meetings,
                                                 infected_people)

        return infected_people

    def __str__(self) -> str:
        '''
        Returns a string "name surname"
        '''
        return f"{self._name} {self._surname}"
