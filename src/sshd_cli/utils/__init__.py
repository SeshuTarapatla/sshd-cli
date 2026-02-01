from pathlib import Path
from subprocess import run
from sys import base_prefix, prefix

from validators import domain, ip_address

from sshd_cli.vars import ASSETS


def valid_host(value: str) -> bool:
    return value == "localhost" or bool(domain(value) or ip_address.ipv4(value))


def is_virtual_env() -> bool:
    return prefix != base_prefix


def update_path(path: Path) -> int:
    path.mkdir(parents=True, exist_ok=True)
    update_path_script = ASSETS / "update_path.ps1"
    return run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            update_path_script,
            str(path),
        ]
    ).returncode


if __name__ == "__main__":
    update_path(Path("~/.ssh2").expanduser())
