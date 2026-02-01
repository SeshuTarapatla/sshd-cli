from send2trash import send2trash
from sshconf import read_ssh_config

from sshd_cli.controllers.code import Code
from sshd_cli.controllers.rsa import generate_rsa_key_pair
from sshd_cli.models.exceptions import AliasAlreadyExists, CodeNotFound, InvalidAlias
from sshd_cli.utils.logger import log
from sshd_cli.vars import CLI_PREFIX, CODE, SSH_CONFIG, SSH_DIR, SSH_KEY, SSH_PUB


class SSH:
    # dunder methods
    def __init__(self) -> None:
        self._ssh_init()

    def __enter__(self) -> "SSH":
        return self

    def __exit__(self, *args): ...

    # public functions
    def list(self):
        return [
            (host, {"hostname": self._conf.host(host).get("hostname", "")})
            for host in self._conf.hosts()
            if not str(host).startswith(CLI_PREFIX) and host != "*"
        ]

    def add(self, hostname: str, alias: str, overwrite: bool = False):
        if self.exists(alias):
            if overwrite:
                self._conf.remove(alias)
            else:
                AliasAlreadyExists.err_msg(alias=alias)
        self._conf.add(alias, HostName=hostname)
        self._write()

    def remove(self, alias: str):
        if self.exists(alias):
            self._conf.remove(alias)
            self._write()
        else:
            InvalidAlias.err_msg(alias=alias)

    def exists(self, alias: str) -> bool:
        return alias in self._conf.hosts()

    def connect(self, alias: str = ""):
        self.alias = alias
        self._client_setup()
        self._remote_setup()

    # private functions
    def _ssh_init(self):
        self._conf = read_ssh_config(SSH_CONFIG)
        SSH_DIR.mkdir(exist_ok=True, parents=True)
        SSH_CONFIG.touch()
        self._add_sshd_cli_config()
        self._add_gss_api_config()
        self._write()

    def _add_gss_api_config(self):
        host = "*"
        self._remove_host(host)
        self._conf.add(
            host=host,
            before_host=self._first_host(),
            GSSAPIAuthentication="yes",
            GSSAPIDelegateCredentials="yes",
        )

    def _add_sshd_cli_config(self):
        host = f"{CLI_PREFIX}*"
        self._remove_host(host)
        self._conf.add(
            host=host,
            before_host=self._first_host(),
            IdentityFile=SSH_KEY,
            IdentitiesOnly="yes",
            StrictHostKeyChecking="accept-new",
            UserKnownHostsFile="/dev/null",
        )

    def _first_host(self) -> str | None:
        if hosts := self._conf.hosts():
            return hosts[0]

    def _remove_host(self, alias: str):
        if alias in self._conf.hosts():
            self._conf.remove(alias)

    def _write(self):
        self._conf.write(SSH_CONFIG)
        self._format_config()

    def _format_config(self):
        delimiter = "\n\n"
        data = SSH_CONFIG.read_text()
        formatted_data = delimiter.join(
            map(
                lambda line: line.strip(),
                filter(lambda line: line, data.split(delimiter)),
            )
        )
        SSH_CONFIG.write_text(formatted_data)

    def _check_host(self):
        if not self.exists(self.alias):
            InvalidAlias.err_msg(alias=self.alias, log=True)
    
    def _check_code(self):
        Code().ensure_setup()

    def _check_rsa_keypair(self):
        if not any((SSH_KEY.exists(), SSH_PUB.exists())):
            log.error("RSA key pair missing. Generating a new pair...")
            [send2trash(file) for file in (SSH_KEY, SSH_PUB) if file.exists()]
            generate_rsa_key_pair()
            log.info(
                f"New RSA key pair generated at: [bright_blue]{SSH_KEY}[/] and [bright_blue]{SSH_PUB}[/]."
            )
        else:
            log.info(
                f"RSA key pair found at: [bright_blue]{SSH_KEY}[/] and [bright_blue]{SSH_PUB}[/]."
            )

    def _client_setup(self):
        self._check_host()
        self._check_code()
        self._check_rsa_keypair()

    def _remote_setup(self): ...


class RemoteSession: ...
