from typing import NoReturn

from sshd_cli.utils.logger import error, warn


class ExitCode:
    INVALID_HOST = 1
    HOST_EXISTS = 2
    INSTALL_ERROR = 3
    VIRTUAL_ENV = 4
    CLI_NOT_FOUND = 5
    SITE_NOT_FOUND = 6
    PATH_ISSUE = 7
    INVALID_RESPONSE = 8


class CliException(Exception):
    @staticmethod
    def err_msg(msg: str, code: int) -> NoReturn:
        error(msg)
        exit(code)


class InvalidHostAddress(CliException, ValueError):
    @staticmethod
    def err_msg(
        msg: str = "Not a valid host address.",
        code: int = ExitCode.INVALID_HOST,
        *,
        host: str | None = None,
    ) -> NoReturn:
        msg = f"'{host}' is {msg.lower()}" if host is not None else msg
        return CliException.err_msg(msg, code)


class AliasAlreadyExists(CliException, ValueError):
    @staticmethod
    def err_msg(
        msg: str = "Alias already exists. Use [bright_yellow]-o/--overwrite[/] flag to replace.",
        code: int = ExitCode.HOST_EXISTS,
        *,
        alias: str | None = None,
    ) -> NoReturn:
        msg = f"'{alias}' {msg.lower()}" if alias is not None else msg
        return CliException.err_msg(msg, code)


class InstallationError(CliException, RuntimeError):
    @staticmethod
    def err_msg(
        msg: str = "Failed to installed sshd-cli utility.",
        code: int = ExitCode.INSTALL_ERROR,
    ) -> NoReturn:
        return CliException.err_msg(msg, code)


class VirtualEnvError(InstallationError, EnvironmentError):
    @staticmethod
    def err_msg(
        msg: str = "Shell integration is not supported. Please prefer base python (or) use [cyan]python -m sshd_cli[/].",
        code: int = ExitCode.VIRTUAL_ENV,
    ) -> NoReturn:
        warn("Virtual environment detected.")
        return CliException.err_msg(msg, code)


class CliNotFound(InstallationError, LookupError):
    @staticmethod
    def err_msg(
        msg: str = "sshd-cli.exe is not found in USER SITE. Make sure you use [bold magenta]--user[/] flag while pip installing.",
        code: int = ExitCode.CLI_NOT_FOUND,
    ) -> NoReturn:
        return CliException.err_msg(msg, code)


class UserSiteNotFound(InstallationError, FileNotFoundError):
    @staticmethod
    def err_msg(
        msg: str = "Failed to resolve USER SITE directory. Cannot proceed with installation.",
        code: int = ExitCode.SITE_NOT_FOUND,
    ) -> NoReturn:
        return CliException.err_msg(msg, code)


class PathUpdateFailure(InstallationError, RuntimeError):
    @staticmethod
    def err_msg(
        msg: str = "Failed to update the USER PATH variable.",
        code: int = ExitCode.PATH_ISSUE,
    ) -> NoReturn:
        return CliException.err_msg(msg, code)


class InvalidResponse(CliException, ValueError):
    @staticmethod
    def err_msg(
        msg: str = "Not a valid response.",
        code: int = ExitCode.INVALID_RESPONSE,
        *,
        response: str = "",
    ) -> NoReturn:
        msg = f"[bold red]{response}[/] is {msg.lower()}" if response else msg
        return CliException.err_msg(msg, code)
