from datetime import datetime, timedelta
from infection_tracker.disease import Disease
import uuid


class InvalidDateError(Exception):
    def __init__(self, date):
        super().__init__(f"{date} is not a valid date.")


class InvalidPersonError(Exception):
    def __init__(self, person):
        super().__init__(f"{person} is not a valid person.")


class InvalidDiseaseError(Exception):
    def __init__(self, disease):
        super().__init__(f"{disease} is not a valid disease.")


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
        self._name = str(name)
        self._surname = str(surname)
        self._meeting_list = []

    def _add_to_meeting_list(self,
                             uuid: int,
                             person: str,
                             date: datetime,
                             duration: timedelta) -> None:

        self._meeting_list.append(
            {
                "uuid": uuid,
                "person": person,
                "date": date,
                "duration": duration
            }
        )

    def add_meeting(self, person, date: str, duration: int) -> None:
        '''
        Adds new meeting to person's meeting list.
        '''
        if not isinstance(person, Person):
            raise InvalidPersonError(person)

        try:
            date = datetime.fromisoformat(date)
            duration = timedelta(minutes=duration)
        except ValueError:
            raise InvalidDateError(date)

        # Creating an universally unique identifier for a meeting
        meeting_uuid = uuid.uuid4()

        self._add_to_meeting_list(meeting_uuid, person, date, duration)
        person._add_to_meeting_list(meeting_uuid, self, date, duration)

    def meetings(self) -> list:
        '''
        Returns person's meeting list
        '''
        return self._meeting_list

    def who_is_infected(self,
                        disease: Disease,
                        when_diagnosed: str,
                        last_meeting_date: datetime = None,
                        last_meeting_duration: timedelta = None,
                        checked_meetings: list = None,
                        infected_people: list = None) -> set:
        '''
        Returns a list of possibly infected people.
        '''
        try:
            infection_period = disease.get_infectious_period()
        except Exception:
            raise InvalidDiseaseError(disease)

        if not isinstance(when_diagnosed, datetime):
            try:
                when_diagnosed = datetime.fromisoformat(when_diagnosed)
            except ValueError:
                raise InvalidDateError(when_diagnosed)

        if checked_meetings is None:
            checked_meetings = []

        if infected_people is None:
            infected_people = {self.__str__()}

        for meeting in self._meeting_list:
            if meeting["uuid"] not in checked_meetings:
                if (last_meeting_date is None and
                    meeting["date"] >= when_diagnosed - infection_period) or (
                        last_meeting_date is not None and
                        meeting["date"] >= last_meeting_date and
                        meeting["date"] <=
                        ((last_meeting_date + last_meeting_duration)
                            + infection_period)):
                    checked_meetings.append(meeting["uuid"])
                    infected_people.add(meeting["person"].__str__())
                    meeting["person"].who_is_infected(disease,
                                                      when_diagnosed,
                                                      meeting["date"],
                                                      meeting["duration"],
                                                      checked_meetings,
                                                      infected_people)

        return infected_people

    def __str__(self) -> str:
        '''
        Returns a string "name surname"
        '''
        return f"{self._name} {self._surname}"
