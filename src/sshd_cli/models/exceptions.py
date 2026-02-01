from typing import NoReturn

from sshd_cli.utils.logger import error, warn
from sshd_cli.utils.logger import log as log_


class ExitCode:
    INVALID_HOST = 1
    ALIAS_EXISTS = 2
    ALIAS_MISSING = 3
    INSTALL_ERROR = 4
    VIRTUAL_ENV = 5
    CLI_NOT_FOUND = 6
    SITE_NOT_FOUND = 7
    PATH_ISSUE = 8
    INVALID_RESPONSE = 9
    SSH_KEYGEN_MISSING = 10
    SSH_KEYGEN_ERROR = 11
    CODE_NOT_FOUND = 12


class CliException(Exception):
    @staticmethod
    def err_msg(msg: str, code: int, log: bool = False) -> NoReturn:
        log_.error(msg) if log else error(msg)
        exit(code)


class InvalidHostAddress(CliException, ValueError):
    @staticmethod
    def err_msg(
        msg: str = "Not a valid host address.",
        code: int = ExitCode.INVALID_HOST,
        log: bool = False,
        *,
        host: str | None = None,
    ) -> NoReturn:
        msg = f"'{host}' is {msg.lower()}" if host is not None else msg
        return CliException.err_msg(msg, code, log)


class AliasAlreadyExists(CliException, ValueError):
    @staticmethod
    def err_msg(
        msg: str = "Alias already exists. Use [bright_yellow]-o/--overwrite[/] flag to replace.",
        code: int = ExitCode.ALIAS_EXISTS,
        log: bool = False,
        *,
        alias: str | None = None,
    ) -> NoReturn:
        msg = f"'{alias}' {msg.lower()}" if alias is not None else msg
        return CliException.err_msg(msg, code, log)


class InvalidAlias(CliException, LookupError):
    @staticmethod
    def err_msg(
        msg: str = "Not a valid alias.",
        code: int = ExitCode.ALIAS_MISSING,
        log: bool = False,
        *,
        alias: str = "",
    ) -> NoReturn:
        msg = f"[bold red]{alias}[/] is {msg.lower()}"
        return CliException.err_msg(msg, code, log)


class InstallationError(CliException, RuntimeError):
    @staticmethod
    def err_msg(
        msg: str = "Failed to installed sshd-cli utility.",
        code: int = ExitCode.INSTALL_ERROR,
        log: bool = False,
    ) -> NoReturn:
        return CliException.err_msg(msg, code, log)


class VirtualEnvError(InstallationError, EnvironmentError):
    @staticmethod
    def err_msg(
        msg: str = "Shell integration is not supported. Please prefer base python (or) use [cyan]python -m sshd_cli[/].",
        code: int = ExitCode.VIRTUAL_ENV,
        log: bool = False,
    ) -> NoReturn:
        warn("Virtual environment detected.")
        return CliException.err_msg(msg, code, log)


class CliNotFound(InstallationError, LookupError):
    @staticmethod
    def err_msg(
        msg: str = "sshd-cli.exe is not found in USER SITE. Make sure you use [bold magenta]--user[/] flag while pip installing.",
        code: int = ExitCode.CLI_NOT_FOUND,
        log: bool = False,
    ) -> NoReturn:
        return CliException.err_msg(msg, code, log)


class UserSiteNotFound(InstallationError, FileNotFoundError):
    @staticmethod
    def err_msg(
        msg: str = "Failed to resolve USER SITE directory. Cannot proceed with installation.",
        code: int = ExitCode.SITE_NOT_FOUND,
        log: bool = False,
    ) -> NoReturn:
        return CliException.err_msg(msg, code, log)


class PathUpdateFailure(InstallationError, RuntimeError):
    @staticmethod
    def err_msg(
        msg: str = "Failed to update the USER PATH variable.",
        code: int = ExitCode.PATH_ISSUE,
        log: bool = False,
    ) -> NoReturn:
        return CliException.err_msg(msg, code, log)


class InvalidResponse(CliException, ValueError):
    @staticmethod
    def err_msg(
        msg: str = "Not a valid response.",
        code: int = ExitCode.INVALID_RESPONSE,
        log: bool = False,
        *,
        response: str = "",
    ) -> NoReturn:
        msg = f"[bold red]{response}[/] is {msg.lower()}" if response else msg
        return CliException.err_msg(msg, code, log)


class SSHKeyGenMissing(CliException, FileNotFoundError):
    @staticmethod
    def err_msg(
        msg: str = "[bold red]ssh-keygen.exe[/] is not found in the PATH. Cannot generate rsa keypair.",
        code: int = ExitCode.SSH_KEYGEN_MISSING,
        log: bool = False,
    ) -> NoReturn:
        return CliException.err_msg(msg, code, log)


class KeyPairGenerateError(CliException, RuntimeError):
    @staticmethod
    def err_msg(
        msg: str = "Failed to generate a rsa keypair. Cannot proceed further.",
        code: int = ExitCode.SSH_KEYGEN_ERROR,
        log: bool = False,
    ) -> NoReturn:
        return CliException.err_msg(msg, code, log)


class CodeNotFound(CliException, FileNotFoundError):
    @staticmethod
    def err_msg(
        msg: str = "Visual Studio Code not found in the PATH.",
        code: int = ExitCode.CODE_NOT_FOUND,
        log: bool = False,
    ) -> NoReturn:
        return CliException.err_msg(msg, code, log)
