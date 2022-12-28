#!/usr/bin/env python3

# Standard libraries.
import io
import platform
import subprocess
import sys


# External dependencies.
import click

# Internal modules.
import rclone_pyside6.parse


def kill_rclone(process: subprocess.Popen[str]) -> None:  # pragma: no cover
    """On Windows, chocolatey has a wrapper that starts rclone as a subprocess."""
    if platform.system() == "Windows":
        # A way to kill all child subprocess in Windows.
        subprocess.call(["taskkill", "/F", "/PID", str(process.pid), "/T"])
    else:
        # Not sure how to do this on other platforms.
        process.kill()


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("source")
@click.argument("destination")
def sync(source: str, destination: str) -> None:
    choice_buffer = io.StringIO()
    with subprocess.Popen(
        ["rclone", "sync", "--dry-run", source, destination],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        stderr = process.stderr
        assert stderr is not None
        try:
            for line in stderr:
                sync_line = rclone_pyside6.parse.parse_rclone_sync_line(line)
                if sync_line is None:
                    continue
                line = rclone_pyside6.parse.to_choice_line_from_sync_line(sync_line)
                choice_buffer.write(line)
                choice_buffer.write("\n")
                del line
                del sync_line
        finally:
            kill_rclone(process)
            del stderr
        process.communicate()
    del process
    choice_lines = click.edit(choice_buffer.getvalue())
    del choice_buffer

    for line in io.StringIO(choice_lines):
        sync_line = rclone_pyside6.parse.parse_choice_line(line)
        if sync_line is None:
            continue
        print(sync_line)


def main() -> int:  # pragma: no cover
    cli()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
