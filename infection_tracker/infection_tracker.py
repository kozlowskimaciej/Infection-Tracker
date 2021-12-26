from disease import Disease
from files import read_meetings_csv, write_file_infected
import sys
import json
import argparse


def parser(arguments):
    # loads text from help_messages.json file
    with open('help_messages.json') as f:
        help_msg = json.load(f)

    parser = argparse.ArgumentParser(description=help_msg['description'])

    parser.add_argument('meetings',
                        help=help_msg['meetings'])

    parser.add_argument('infected',
                        help=help_msg['infected'])

    parser.add_argument('period',
                        type=int,
                        help=help_msg['period'])

    parser.add_argument('date',
                        type=str,
                        help=help_msg['date'])

    parser.add_argument('--name',
                        help=help_msg['--name'])

    parser.add_argument('--output',
                        nargs='?',
                        const='output',
                        help=help_msg['--output'])

    args = parser.parse_args(arguments[1:])

    if not args.name:
        name = None

    disease = Disease(name, int(args.period))
    people = read_meetings_csv(args.meetings)

    infected_list = people.get(args.infected).who_is_infected(disease)

    infected = ", ".join(infected_list)

    print(infected)

    if args.output:
        write_file_infected(args.output, infected)


def main(arguments):
    if len(arguments) > 1:
        parser(arguments)


if __name__ == "__main__":
    main(sys.argv)
