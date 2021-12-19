from datetime import datetime, timedelta
from disease import Disease
import uuid


class InvalidMeetingDateError(Exception):
    def __init__(self, date, duration):
        super().__init__(f"{date} {duration} is not a valid date.") 

class InvalidPersonError(Exception):
    def __init__(self, person):
        super().__init__(f"{person} is not a valid person.")  

class InvalidDiseaseError(Exception):
    def __init__(self, disease):
        super().__init__(f"{disease} is not a valid disease.")  


class Person:
    def __init__(self, name: str, surname: str) -> None:
        self._name = str(name)
        self._surname = str(surname)
        self._meeting_list = []

    def add_meeting(self, person, date: str, duration: int) -> None:
        if not isinstance(person, Person):
            raise InvalidPersonError(person)

        try:
            date = datetime.strptime(date, "%d.%m.%Y %H:%M")
            duration = timedelta(minutes=duration)
        except ValueError:
            raise InvalidMeetingDateError(date, duration)

        meeting_uuid = uuid.uuid4()

        self._meeting_list.append(
            {
                "uuid": meeting_uuid,
                "person": person,
                "date": date,
                "duration": duration
            }
        )

        person._meeting_list.append(
            {
                "uuid": meeting_uuid,
                "person": self,
                "date": date,
                "duration": duration
            }
        )

    def meetings(self) -> list:
        return self._meeting_list

    def who_is_infected(self, disease: Disease, last_meeting_date: datetime = None, last_meeting_duration: timedelta = None, checked_meetings: list = None, infected_people: list = None) -> set:
        if not isinstance(disease, Disease):
            raise InvalidDiseaseError(disease)
        
        if checked_meetings is None:
            checked_meetings = []
        
        if infected_people is None:
            infected_people = {self.__str__()}

        for meeting in self._meeting_list:
            if meeting["uuid"] not in checked_meetings:
                if last_meeting_date is None or (
                    meeting["date"] >= last_meeting_date and (
                        meeting["date"] <= last_meeting_date + last_meeting_duration + disease.get_infectious_period())):
                    checked_meetings.append(meeting["uuid"])
                    infected_people.add(meeting["person"].__str__())
                    meeting["person"].who_is_infected(disease, meeting["date"], meeting["duration"], checked_meetings, infected_people)
        
        return infected_people

    def __str__(self) -> str:
        return f"{self._name} {self._surname}"