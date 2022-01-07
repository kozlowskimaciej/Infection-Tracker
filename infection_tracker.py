from infection_tracker.disease import Disease
from infection_tracker.files import read_meetings_csv, write_file_infected
import sys
import json
import argparse


def console_ui(arguments):
    # loads dictionary with messages from help_messages.json file
    with open('infection_tracker/help_messages.json') as f:
        help_msg = json.load(f)

    parser = argparse.ArgumentParser(description=help_msg['description'])

    # loads arguments based on help_messages.json file
    for argument in help_msg:
        if argument not in {'description', '--output'}:
            parser.add_argument(argument, help=help_msg[argument])

    # optional argument for saving program's output in file
    # default name is 'output'
    parser.add_argument('--output',
                        nargs='?',
                        const='output',
                        help=help_msg['--output'])

    args = parser.parse_args(arguments[1:])

    # if disease's name is not provided, set it to None
    if not args.name:
        name = None

    disease = Disease(name, int(args.period))
    people = read_meetings_csv(args.meetings)

    # make a list with infected people
    infected_list = people.get(args.infected).who_is_infected(disease, args.date)
    infected = ", ".join(infected_list)

    print(infected)

    if args.output:
        write_file_infected(args.output, infected)


def main(arguments):
    # if arguments are present, use console interface
    if arguments:
        console_ui(arguments)


if __name__ == "__main__":
    main(sys.argv)
