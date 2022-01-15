import csv
from infection_tracker.person import Person


def read_meetings_csv(file):
    with open(file, newline='') as csvfile:
        people = read_meetings(csvfile)
    return people


def read_meetings(file_handle):
    reader = csv.DictReader(file_handle)
    people = dict()
    for row in reader:
        person1 = str(row['Name_1'] + ' ' + row['Surname_1'])
        if person1 not in people:
            people[person1] = Person(row['Name_1'], row['Surname_1'])

        person2 = str(row['Name_2'] + ' ' + row['Surname_2'])
        if person2 not in people:
            people[person2] = Person(row['Name_2'], row['Surname_2'])

        people[person1].add_meeting(people[person2],
                                    row['Date'],
                                    row['Duration'])
    return people


def write_file_infected(file, infected):
    with open(file, 'w') as f:
        f.write(infected)
