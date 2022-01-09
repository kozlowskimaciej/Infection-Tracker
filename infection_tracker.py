import sys
from infection_tracker.ui.cli_ui import CLI_UI


def main(arguments):
    # if arguments are present, use console interface
    if len(arguments) > 1:
        CLI_UI(arguments)
    else:
        print("INFECTION TRACKER")


if __name__ == "__main__":
    main(sys.argv)
