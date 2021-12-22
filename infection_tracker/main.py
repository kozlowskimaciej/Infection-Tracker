from disease import Disease
from files import read_meetings_csv, write_file_infected
import csv
import sys
import argparse


def main(arguments):
    parser = argparse.ArgumentParser(description='wip')
    parser.add_argument('meetings_csv', help='CSV file that contains informations about meetings. The order of columns is as follows: Name_1, Surname_1, Name_2, Surname_2, Date (dd.mm.Y h:mm format), Duration (in minutes).')
    parser.add_argument('infected_person', help='Name and surname of an infected person, e.g. "Mark Howling".')
    parser.add_argument('infectious_period', type=int, help='Infectious period of a disease (in minutes).')
    parser.add_argument('--name', help='Name of disease.')
    parser.add_argument('--output', nargs = '?', const = 'output', help='Save output in file.')
    args = parser.parse_args(arguments[1:])

    if not args.name:
        name = None
    
    disease = Disease(name, int(args.period))
    people = read_meetings_csv(args.people)

    infected_list = people[args.infected].who_is_infected(disease)

    infected = ", ".join(infected_list)

    print(infected)

    if args.output:
        write_file_infected(args.output, infected)



if __name__ == "__main__":
    main(sys.argv)