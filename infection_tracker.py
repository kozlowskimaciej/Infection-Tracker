import sys
from infection_tracker.ui.cli_ui import CLI_UI
from infection_tracker.ui.tui_ui import TUI_UI


def main(arguments):
    # If arguments are present, use command-line interface,
    # else use text-based user interface
    if len(arguments) > 1:
        CLI_UI(arguments)
    else:
        TUI_UI().show()


if __name__ == "__main__":
    main(sys.argv)
