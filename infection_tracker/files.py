import csv
from infection_tracker.person import Person


def read_meetings_csv(file) -> dict:
    with open(file, newline='') as csvfile:
        people = read_meetings_csv_handled(csvfile)
    return people


def read_meetings_csv_handled(file_handle) -> dict:
    reader = csv.DictReader(file_handle)
    people = dict()
    for row in reader:
        # Check if a person already exists. If not, make a new Person object
        person1 = str(row['Name_1'] + ' ' + row['Surname_1'])
        if person1 not in people:
            people[person1] = Person(row['Name_1'], row['Surname_1'])

        person2 = str(row['Name_2'] + ' ' + row['Surname_2'])
        if person2 not in people:
            people[person2] = Person(row['Name_2'], row['Surname_2'])

        # Add meeting to both people's meeting list
        people[person1].add_meeting(people[person2],
                                    row['Date'],
                                    row['Duration'])
    return people


def write_file_infected(file, infected: str) -> None:
    with open(file, 'w') as f:
        write_file_infected_handled(f, infected)


def write_file_infected_handled(file_handle, infected: str) -> None:
    # Write infected people to file
    file_handle.write(infected)
