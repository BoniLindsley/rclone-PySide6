#!/usr/bin/env python3

# External dependencies.
import click
import click.testing

# Internal modules
import rclone_pyside6.cli


def test_group_echoes_greetings() -> None:
    group = rclone_pyside6.cli.group
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(
        group, ("Alpha", "Beta", "", "Gamma", "Delta")
    )
    assert result.stderr == ""
    assert result.stdout.splitlines() == [
        "Hello, Alpha!",
        "Hello, Beta!",
        "Hello, Gamma!",
        "Hello, Delta!",
    ]
    assert result.exception is None
    assert result.exit_code == 0
