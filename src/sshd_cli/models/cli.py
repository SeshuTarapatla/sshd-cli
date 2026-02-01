from enum import StrEnum
from sys import stdout
from typing import TypedDict


class HelpOpts(TypedDict):
    help: str
    short_help: str


class Panels(StrEnum):
    SERVER = "Server Management"
    SESSION = "Session Management"
    SHELL = "Shell Integration"


class Ansi(StrEnum):
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

    # most used combos
    BOLD_RED = f"{BOLD}{RED}"
    BOLD_CYAN = f"{BOLD}{CYAN}"


    @staticmethod
    def reset():
        stdout.write(Ansi.RESET)
        stdout.flush()
