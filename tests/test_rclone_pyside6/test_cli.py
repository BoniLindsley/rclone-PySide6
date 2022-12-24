#!/usr/bin/env python3

# Standard libraries.
import collections.abc
import subprocess
import sys
import typing

# External dependencies.
import click
import click.testing

# Internal modules
import rclone_pyside6.cli
from rclone_pyside6.cli import RcdServer

_F = typing.TypeVar("_F", bound=collections.abc.Callable[..., typing.Any])


@click.command()
def click_command() -> None:
    pass


class TestRcdServer:
    def test_default_constructor(self) -> None:
        RcdServer()

    def test_context_manager_default_enter_and_exit(self) -> None:
        with RcdServer() as rcd_server:
            assert isinstance(rcd_server, RcdServer)

    def test_context_manager_exit_kills_subprocess(self) -> None:
        with RcdServer() as rcd_server:
            process = subprocess.Popen(  # pylint: disable=consider-using-with
                [sys.executable]
            )
            rcd_server.rcd_subprocess = process
            assert process.returncode is None
        assert process.returncode is not None

    def test_pass_to_command_forwards_server_instance(self) -> None:
        @click.command()
        @RcdServer.pass_to_command
        def command(rcd_server: RcdServer) -> None:
            assert isinstance(rcd_server, RcdServer)
            click.echo("test_pass_to_command_forwards_server_instance")

        runner = click.testing.CliRunner(mix_stderr=False)
        result = runner.invoke(command)
        assert result.stderr == ""
        assert result.stdout == "test_pass_to_command_forwards_server_instance\n"
        assert result.exception is None
        assert result.exit_code == 0

    def test_from_context_creates_server_if_missing(self) -> None:
        with click.Context(click_command) as ctx:
            rcd_server = RcdServer.from_context(ctx)
            assert isinstance(rcd_server, RcdServer)

    def test_from_context_ensures_server_cleanup(self) -> None:
        rcd_server_dict: list[RcdServer] = []
        rcd_subprocess_dict: list[subprocess.Popen[bytes]] = []

        @click.command()
        def command() -> None:
            ctx = click.get_current_context()
            rcd_server_dict.append(RcdServer.from_context(ctx))
            assert rcd_server_dict[0].rcd_subprocess is None

            rcd_server_dict[0].start()
            rcd_subprocess = rcd_server_dict[0].rcd_subprocess
            assert rcd_subprocess is not None
            rcd_subprocess_dict.append(rcd_subprocess)
            assert rcd_subprocess.returncode is None

        runner = click.testing.CliRunner(mix_stderr=False)
        result = runner.invoke(command, input="\n")
        assert result.stderr == ""
        assert result.stdout == ""
        assert result.exception is None
        assert result.exit_code == 0

        assert rcd_server_dict[0].rcd_subprocess is None
        assert rcd_subprocess_dict[0].returncode is not None

    def test_from_context_attaches_resource_to_root_context(self) -> None:
        rcd_server_dict: list[RcdServer] = []
        rcd_subprocess_dict: list[subprocess.Popen[bytes]] = []

        @click.command()
        def command() -> None:
            root = click.get_current_context()
            with click.Context(click_command, parent=root) as ctx:
                rcd_server_dict.append(RcdServer.from_context(ctx))
                assert rcd_server_dict[0].rcd_subprocess is None

                rcd_server_dict[0].start()
                rcd_subprocess = rcd_server_dict[0].rcd_subprocess
                assert rcd_subprocess is not None
                rcd_subprocess_dict.append(rcd_subprocess)
                assert rcd_subprocess.returncode is None
            assert rcd_subprocess_dict[0].returncode is None

        runner = click.testing.CliRunner(mix_stderr=False)
        result = runner.invoke(command, input="\n")
        assert result.stderr == ""
        assert result.stdout == ""
        assert result.exception is None
        assert result.exit_code == 0

        assert rcd_server_dict[0].rcd_subprocess is None
        assert rcd_subprocess_dict[0].returncode is not None

    def test_from_context_reuses_server_if_exists(self) -> None:
        with click.Context(click_command) as ctx:
            rcd_server = RcdServer.from_context(ctx)
            rcd_server_2 = RcdServer.from_context(ctx)
            assert rcd_server is rcd_server_2

    def test_from_context_overwrites_metakey_if_not_server(self) -> None:
        with click.Context(click_command) as ctx:
            ctx.meta[RcdServer.meta_key] = 1
            rcd_server = RcdServer.from_context(ctx)
            assert isinstance(rcd_server, RcdServer)

    def test_start_and_stop(self) -> None:
        rcd_server = RcdServer()
        assert rcd_server.rcd_subprocess is None

        rcd_server.start()
        rcd_subprocess = rcd_server.rcd_subprocess
        assert isinstance(rcd_subprocess, subprocess.Popen)
        try:
            assert rcd_subprocess.returncode is None

            rcd_server.stop()
            assert rcd_server.rcd_subprocess is None
            assert rcd_subprocess.returncode is not None
        finally:
            rclone_pyside6.cli.kill_subprocesses(rcd_subprocess)
            rcd_subprocess.communicate()

    def test_start_ignores_restart(self) -> None:
        rcd_server = RcdServer()
        assert rcd_server.rcd_subprocess is None

        rcd_server.start()
        rcd_subprocess = rcd_server.rcd_subprocess
        assert isinstance(rcd_subprocess, subprocess.Popen)
        try:
            assert rcd_subprocess.returncode is None

            rcd_server.start()
            rcd_subprocess_2 = rcd_server.rcd_subprocess
            assert rcd_subprocess is rcd_subprocess_2
        finally:
            rclone_pyside6.cli.kill_subprocesses(rcd_subprocess)
            rcd_subprocess.communicate()

    def test_stop_is_okay_if_not_started(self) -> None:
        rcd_server = RcdServer()
        assert rcd_server.rcd_subprocess is None
        rcd_server.stop()
        assert rcd_server.rcd_subprocess is None

    def test_stop_is_okay_if_subprocess_stops_unexpectedly(self) -> None:
        rcd_server = RcdServer()
        assert rcd_server.rcd_subprocess is None

        rcd_server.start()
        rcd_subprocess = rcd_server.rcd_subprocess
        assert isinstance(rcd_subprocess, subprocess.Popen)
        try:
            assert rcd_subprocess.returncode is None
            rclone_pyside6.cli.kill_subprocesses(rcd_subprocess)
            rcd_subprocess.communicate()
            assert rcd_subprocess.returncode is not None

            assert rcd_server.rcd_subprocess is not None
            rcd_server.stop()
            assert rcd_server.rcd_subprocess is None
        finally:
            rclone_pyside6.cli.kill_subprocesses(rcd_subprocess)
            rcd_subprocess.communicate()

    def test_create_rcd_command_gives_rclone_command(self) -> None:
        rcd_server = RcdServer()
        rcd_server.address = "address"
        rcd_server.password = "password"
        rcd_server.port = 1234
        rcd_server.realm = "realm"
        rcd_server.user = "user"
        command = rcd_server.create_rcd_command()
        assert len(command) == 6
        assert command[0] == "rclone"
        assert command[1] == "rcd"
        assert "--rc-realm=realm" in command
        assert "--rc-user=user" in command
        assert "--rc-pass=password" in command
        assert "--rc-addr=address:1234" in command


def test_cli_default_is_help() -> None:
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(rclone_pyside6.cli.cli)
    assert result.stderr == ""
    assert result.stdout != ""
    assert result.exception is None
    assert result.exit_code == 0


def test_cli_has_stop_subcommand() -> None:
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(rclone_pyside6.cli.cli, ["stop"])
    assert result.stderr == ""
    assert result.stdout == ""
    assert result.exception is None
    assert result.exit_code == 0


def test_start_callable() -> None:
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(rclone_pyside6.cli.start)
    assert result.stderr == ""
    assert result.stdout == ""
    assert result.exception is None
    assert result.exit_code == 0


def test_stop_callable() -> None:
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(rclone_pyside6.cli.stop)
    assert result.stderr == ""
    assert result.stdout == ""
    assert result.exception is None
    assert result.exit_code == 0
