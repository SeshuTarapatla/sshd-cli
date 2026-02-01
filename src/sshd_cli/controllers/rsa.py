from shutil import which
from subprocess import DEVNULL, run

from sshd_cli.models.exceptions import KeyPairGenerateError, SSHKeyGenMissing
from sshd_cli.vars import SSH_COMMENT, SSH_KEY


def generate_rsa_key_pair():
    SSH_KEYGEN = which("ssh-keygen.exe")
    if not SSH_KEYGEN:
        SSHKeyGenMissing.err_msg(log=True)
    resp = run(
        args=[
            SSH_KEYGEN,
            "-t",
            "rsa",
            "-b",
            "2048",
            "-N",
            "",
            "-C",
            SSH_COMMENT,
            "-f",
            SSH_KEY,
        ],
        stdout=DEVNULL,
    ).returncode
    if resp != 0:
        KeyPairGenerateError.err_msg(log=True)
