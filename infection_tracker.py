import sys
from infection_tracker.ui.cli_ui import CLI_UI
from infection_tracker.ui.tui_ui import TUI_UI


def main(arguments):
    # if arguments are present, use console interface
    if len(arguments) > 1:
        CLI_UI(arguments)
    else:
        TUI_UI()


if __name__ == "__main__":
    main(sys.argv)
