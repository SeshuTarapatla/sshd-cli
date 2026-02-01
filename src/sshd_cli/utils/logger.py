from logging import INFO, basicConfig, getLogger

from rich.console import Console
from rich.logging import RichHandler

__all__ = ["console", "log", "info", "error"]

console = Console()


basicConfig(
    level=INFO,
    format="| %(message)s",
    handlers=[RichHandler(console=console, omit_repeated_times=False)],
)


log = getLogger("app")


def info(msg):
    console.print(f"[bold blue] INFO    [/]- {msg}")


def error(msg):
    console.print(f"[bold red] ERROR   [/]- {msg}")


def warn(msg):
    console.print(f"[bold yellow] WARNING [/]- {msg}")


if __name__ == "__main__":
    log.info("INFO MESSAGE")
    log.warning("WARNING MESSAGE")
    log.error("ERROR MESSAGE")
    log.fatal("FATAL MESSAGE")
