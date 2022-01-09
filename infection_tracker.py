import sys
from infection_tracker.console_ui import ConsoleUI


def main(arguments):
    # if arguments are present, use console interface
    if len(arguments) > 1:
        ConsoleUI(arguments)
    else:
        print("INFECTION TRACKER")


if __name__ == "__main__":
    main(sys.argv)
