import atexit
import json
from pathlib import Path
from shutil import copy2, move
from site import USER_SITE
from subprocess import run
from sys import argv
from typing import Literal

import yaml
from icecream import ic
from rich.syntax import Syntax
from typer import Argument, Option, Typer

from sshd_cli.controllers.ssh import SSH
from sshd_cli.models.cli import Ansi, HelpOpts, Panels
from sshd_cli.models.exceptions import (
    CliNotFound,
    InvalidHostAddress,
    InvalidResponse,
    PathUpdateFailure,
    UserSiteNotFound,
    VirtualEnvError,
)
from sshd_cli.utils import is_virtual_env, update_path, valid_host
from sshd_cli.utils.logger import console, info
from sshd_cli.vars import BANNER, BIN

# MAIN ------------------------------------------------------------------------------------------------

console.print(BANNER)
app = Typer(
    name="sshd-cli",
    no_args_is_help=True,
    add_completion=False,
    help="A cli tool to connect to servers and manage remote development sessions.",
)


class Help:
    @staticmethod
    def generate_help_opts(
        help: str,
        *,
        alias: str | tuple[str, ...] | None = None,
        indent: int = 0,
    ) -> HelpOpts:
        alias = (alias,) if isinstance(alias, str) else alias
        return {
            "help": help,
            "short_help": f"{help} {'\t' * indent}Alias: [bold cyan]{', '.join(sorted(alias))}[/]."
            if alias
            else help,
        }

    add_command = generate_help_opts("Add a new server.", alias="new", indent=3)
    remove_command = generate_help_opts(
        "Remove an existing server.", alias="delete", indent=2
    )
    list_command = generate_help_opts(
        "List all saved servers.",
        alias=("ls", "status", "show"),
        indent=2,
    )
    connect_command = generate_help_opts(
        "Start remote session on a server.", alias="start", indent=1
    )
    kill_command = generate_help_opts(
        "Kill running session on a server.", alias="stop", indent=1
    )
    install_command = generate_help_opts(
        "Install [bright_yellow]sshd-cli[/] as a command line utility."
    )

    @staticmethod
    def interactive_mode():
        atexit.register(Ansi.reset)
        console.print(" [bold bright_black]*** Interactive Mode ***[/]\n")


# SERVERS ---------------------------------------------------------------------------------------------


@app.command(name="add", rich_help_panel=Panels.SERVER, **Help.add_command)
@app.command(name="new", hidden=True, **Help.add_command)
def add(
    hostname: str = Argument("", help="Address of the host to add."),
    alias: str = Option(
        "",
        "-a",
        "--alias",
        help="Short alias for the host. (defaults to [bold]hostname prefix[/]).",
    ),
    overwrite: bool = Option(
        False, "-o", "--overwrite", help="Overwrite if the alias exists."
    ),
):
    ssh = SSH()
    if not hostname:
        Help.interactive_mode()
        hostname = input(f" Enter the host address: {Ansi.BOLD_CYAN}").strip()
        InvalidHostAddress.err_msg(host=hostname) if not valid_host(hostname) else None
        alias = hostname.split(".")[0].lower()
        alias = input(
            f"{Ansi.RESET} Enter a short alias for the host (defaults to {Ansi.BOLD_CYAN}{alias}{Ansi.RESET}): {Ansi.BOLD_CYAN}"
        ).strip()
        if ssh.exists(alias):
            resp = (
                input(
                    f"{Ansi.RESET} {Ansi.BOLD_CYAN}{alias}{Ansi.RESET} already exists. Do you want to overwrite it? (y/n): {Ansi.BOLD_RED}"
                )
                .lower()
                .strip()
            )
            if resp not in ("y", "n"):
                InvalidResponse(resp)
            if resp == "y":
                overwrite = True
            elif resp == "n":
                overwrite = False
    if not alias:
        alias = hostname.split(".")[0].lower()
        info(f"Alias not passed, defaulting to: [bold cyan]{alias}[/]")
    ssh.add(hostname, alias, overwrite)
    info(f"New host with alias '{alias}' added successfully.")


@app.command(name="remove", rich_help_panel=Panels.SERVER, **Help.remove_command)
@app.command(name="delete", hidden=True, **Help.remove_command)
def remove(alias: str = Argument("", help="Alias of the host to remove.")):
    if not alias:
        Help.interactive_mode()
        list_(output="table")
        alias = input(f"Please enter the alias of the host to remove: {Ansi.BOLD_RED}").strip()
    with SSH() as ssh:
        ssh.remove(alias)
    info(f"Host with alias '{alias}' removed successfully.")


@app.command(name="list", rich_help_panel=Panels.SERVER, **Help.list_command)
@app.command(name="ls", hidden=True, **Help.list_command)
@app.command(name="show", hidden=True, **Help.list_command)
@app.command(name="status", hidden=True, **Help.list_command)
def list_(
    output: Literal["table", "json", "yaml"] = Option(
        "table", "-o", "--output", help="Output format."
    ),
    status: bool = Option(True, help="Status of host session.", is_flag=True),
):
    ssh = SSH()
    hosts, configs = zip(*ssh.list())
    console.print(f"Total Hosts: {len(hosts)}.")
    if output == "table":
        from rich.align import Align
        from rich.table import Table

        table = Table()
        table.add_column(
            Align("Alias", align="center"), style="bold cyan", no_wrap=True
        )
        table.add_column(
            Align("Configuration", align="center"),
            style="bright_magenta",
        )

        [
            table.add_row(host, json.dumps(config))
            for host, config in zip(hosts, configs)
        ]
        console.print(table)
    else:
        entries = [
            {"host": host, "config": config} for host, config in zip(hosts, configs)
        ]
        if output == "json":
            console.print("\n" + json.dumps(entries, indent=2))
        elif output == "yaml":
            console.print(
                "",
                Syntax(
                    yaml.safe_dump({"hosts": entries}, sort_keys=False),
                    "yaml",
                    theme="ansi_dark",
                    background_color=None,
                ),
            )


# SESSIONS --------------------------------------------------------------------------------------------


@app.command(name="connect", rich_help_panel=Panels.SESSION, **Help.connect_command)
@app.command(name="start", hidden=True, **Help.connect_command)
def connect(
    alias: str = Argument("", help="Alias of the host to connect."),
    ssh: bool = Option(False, "-s", "--ssh", help="Connect in terminal ssh mode."),
):
    if not alias:
        Help.interactive_mode()
        list_(output="table")
        alias = input(f"Please enter an host alias to start remote session: {Ansi.BOLD_BLUE}").strip()
    if ssh:
        run(["ssh", alias])
    else:
        with SSH() as ssh_:
            ssh_.connect(alias)


@app.command(name="kill", rich_help_panel=Panels.SESSION, **Help.kill_command)
@app.command(name="stop", hidden=True, **Help.kill_command)
def kill(alias: str = Argument("", help="Alias of the host to kill session.")):
    ic(alias)


# SHELL -----------------------------------------------------------------------------------------------


if argv[0].endswith(".py"):

    @app.command(name="install", rich_help_panel=Panels.SHELL, **Help.install_command)
    def install():
        console.print()
        if is_virtual_env():
            VirtualEnvError.err_msg()
        if USER_SITE:
            scripts_dir = Path(USER_SITE).parent / "Scripts"
            cli = "sshd-cli.exe"
            src = scripts_dir / cli
            src_bkp = scripts_dir / f"{cli}.bkp"
            dst = BIN / cli

            if not src.exists() and src_bkp.exists():
                src = src_bkp

            if src.exists():
                BIN.mkdir(parents=True, exist_ok=True)
                copy2(src, dst)
                move(src, src_bkp)
                resp = update_path(BIN)
                if resp in (0, 1):
                    info(
                        "sshd-cli.exe installation complete. Start using the tool by running [yellow]sshd-cli[/]."
                    )
                    if resp == 0:
                        info(
                            "Path updated. Please restart the terminal for new changes to take affect."
                        )
                elif resp == 2:
                    PathUpdateFailure.err_msg()
            else:
                CliNotFound.err_msg()
        else:
            UserSiteNotFound.err_msg()
