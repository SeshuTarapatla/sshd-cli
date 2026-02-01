from subprocess import check_output
from sshd_cli.models.exceptions import CodeNotFound
from sshd_cli.vars import CODE, SSH_EXTENSION


class Code:
    def __init__(self) -> None:
        self.check_code()

    def check_code(self):
        if not CODE:
            CodeNotFound.err_msg(log=True)

    def ensure_setup(self):
        self.ensure_remote_ssh_extension()
        self.ensure_github_copilot_access()

    def ensure_remote_ssh_extension(self):
        if SSH_EXTENSION not in check_output([CODE, "--list-extensions"], encoding="utf-8"):
            self.install_remote_ssh_extension()
    
    def install_remote_ssh_extension(self):
        ...

    def ensure_github_copilot_access(self): ...
