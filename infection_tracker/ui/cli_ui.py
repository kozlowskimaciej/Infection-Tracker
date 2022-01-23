from infection_tracker.disease import Disease
from infection_tracker.files import read_meetings_csv, write_file_infected
from infection_tracker.exceptions import PersonNotExistsError
import json
import argparse

HELP_MSG_PATH = 'infection_tracker/ui/help_messages.json'


class CLI_UI:
    '''
    Command-line interface
    Class CLI_UI
    '''
    def __init__(self, arguments):
        '''
        Initalizes text-based user interface
        '''
        args = self._parse_args(arguments)

        # if disease's name is not provided, set it to None
        if not args.name:
            name = None

        disease = Disease(name, int(args.period))
        people = read_meetings_csv(args.meetings)

        # make a list with infected people
        infected_person = people.get(args.infected)

        # try to make a list of infected people
        try:
            infected_list = infected_person.who_is_infected(disease, args.date)
        except AttributeError:
            raise PersonNotExistsError(args.infected)

        # make a string from list
        infected_list = ", ".join(infected_list)

        print(infected_list)

        if args.output:
            write_file_infected(args.output, infected_list)

    def _parse_args(self, arguments):
        '''
        Parses arguments from command line
        '''
        # create a parser with arguments
        parser = self._add_args()

        # skip first argument which is script's name
        args = parser.parse_args(arguments[1:])
        return args

    def _add_args(self):
        '''
        Creates parser and adds arguments
        '''
        # loads dictionary with messages from help_messages.json file
        with open(HELP_MSG_PATH) as f:
            help_msg = json.load(f)

        # create parser with description
        parser = argparse.ArgumentParser(description=help_msg['description'])

        # load arguments based on help_messages.json file
        for argument in help_msg:
            if argument not in {'description', '--output'}:
                parser.add_argument(argument, help=help_msg[argument])

        # optional argument for saving program's output in file
        # default name is 'output'
        parser.add_argument('--output',
                            nargs='?',
                            const='output',
                            help=help_msg['--output'])

        return parser
