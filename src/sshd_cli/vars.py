from importlib.resources import files
from pathlib import Path
from shutil import which
from typing import cast

ASSETS          = cast(Path, files("sshd_cli").joinpath("assets"))
BANNER          = (ASSETS / "banner").read_text()
BIN             = Path("~/bin").expanduser()
CODE            = str(which("code"))
CLI_PREFIX      = "sshd_cli"

SSH_DIR         = Path("~/.ssh").expanduser()
SSH_CONFIG      = SSH_DIR / "config"
SSH_KEY         = SSH_DIR / f"{CLI_PREFIX}_rsa"
SSH_PUB         = SSH_DIR / f"{CLI_PREFIX}_rsa.pub"
SSH_COMMENT     = "### Auto generated key by sshd-cli ###"
SSH_EXTENSION   = "ms-vscode-remote.remote-ssh"