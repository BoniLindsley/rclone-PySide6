#!/usr/bin/env python3

# Standard libraries.
import collections.abc
import functools
import logging
import platform
import secrets
import subprocess
import sys
import types
import typing


# External dependencies.
import click
import click_repl  # type: ignore[import]

_F = typing.TypeVar("_F", bound=collections.abc.Callable[..., typing.Any])
_T = typing.TypeVar("_T")

_logger = logging.getLogger(__name__)

repl_meta_key = f"{__package__}.repl_layer_count"


def kill_subprocesses(process: subprocess.Popen[bytes]) -> None:  # pragma: no cover
    if platform.system() == "Windows":
        # A way to kill all child subprocess in Windows.
        subprocess.call(["taskkill", "/F", "/PID", str(process.pid), "/T"])
    else:
        # Not sure how to do this on other platforms.
        process.kill()


class RcdServer:
    __Self = typing.TypeVar("__Self", bound="RcdServer")
    meta_key = f"{__package__}.rcd_server"

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.realm = "rclone"
        self.user = secrets.token_urlsafe()
        self.password = secrets.token_urlsafe()
        self.address = "localhost"
        self.port = 5572
        self.rcd_subprocess: subprocess.Popen[bytes] | None = None

    def __enter__(self: __Self) -> __Self:
        _logger.debug("Context object opening.")
        return self

    def __exit__(  # pylint: disable=useless-return
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> bool | None:
        del exc_type
        del exc_value
        del traceback
        _logger.debug("Context object closing.")
        self.stop()
        return None

    @classmethod
    def pass_to_command(cls, command: _F) -> _F:
        def decorated(*args: object, **kwargs: object) -> object:
            context = click.get_current_context()
            rcd_server = cls.from_context(context)
            return command(rcd_server, *args, **kwargs)

        return functools.update_wrapper(typing.cast(_F, decorated), command)

    @classmethod
    def from_context(cls: type[__Self], ctx: click.Context) -> __Self:
        obj = ctx.meta.get(cls.meta_key)
        if isinstance(obj, cls):
            return obj

        if obj is not None:
            _logger.warning(
                "Overwriting existing click context object of type %s", type(obj)
            )
        del obj

        # Create and store the actual server object.
        new_obj = ctx.meta[cls.meta_key] = cls()

        # Assign cleanup responsibility to the out-most Click context.
        # This is because the Click meta map is used by all contexts in the hierarchy.
        root_ctx = ctx
        parent_ctx: click.Context | None = ctx
        while parent_ctx is not None:
            root_ctx = parent_ctx
            parent_ctx = parent_ctx.parent
        root_ctx.with_resource(new_obj)
        return new_obj

    def start(self) -> None:
        if self.rcd_subprocess is not None:
            _logger.warning("Existing rclone rcd subprocess not properly stopped.")
            return
        arguments = self.create_rcd_command()
        _logger.debug("Starting rclone rcd with: %s", arguments)
        rcd_subprocess = subprocess.Popen(  # pylint: disable=consider-using-with
            arguments
        )
        self.rcd_subprocess = rcd_subprocess

    def stop(self) -> None:
        _logger.debug("Requested to stop existing rclone rcd subprocess.")
        rcd_subprocess = self.rcd_subprocess
        if rcd_subprocess is None:
            _logger.debug("No existing rclone rcd subprocess to stop.")
            return
        if rcd_subprocess.returncode is None:
            _logger.info("Terminating existing rclone rcd subprocess.")
            kill_subprocesses(rcd_subprocess)
        rcd_subprocess.communicate()
        _logger.debug(
            "Return code of rclone rcd subprocess: %s", rcd_subprocess.returncode
        )
        self.rcd_subprocess = None

    def create_rcd_command(self) -> list[str]:
        return [
            "rclone",
            "rcd",
            f"--rc-realm={self.realm}",
            f"--rc-user={self.user}",
            f"--rc-pass={self.password}",
            f"--rc-addr={self.address}:{self.port}",
        ]


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.pass_context
def repl(ctx: click.Context) -> None:
    ctx.meta.setdefault(repl_meta_key, 0)
    ctx.meta[repl_meta_key] += 1
    click_repl.repl(ctx)
    ctx.meta[repl_meta_key] -= 1


@cli.command()
@RcdServer.pass_to_command
@click.pass_context
def start(ctx: click.Context, rcd_server: RcdServer) -> None:
    rcd_server.start()
    if ctx.meta.get(repl_meta_key, 0) <= 0:
        click.pause("Press any key to stop...\n")
        rcd_server.stop()


@cli.command()
@RcdServer.pass_to_command
def stop(rcd_server: RcdServer) -> None:
    rcd_server.stop()


def main() -> int:  # pragma: no cover
    cli()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
