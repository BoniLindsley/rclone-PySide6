#!/usr/bin/env python3

# Standard libraries.
import collections.abc
import re
import sys
import subprocess
import typing


def parse_rclone_sync_line(line: str) -> tuple[str, str] | None:
    pattern = re.compile(
        r"^<5>NOTICE: (.*): Skipped (\w+) as --dry-run is set \(size \d+\)$"
    )
    match = pattern.match(line)
    if match is None:
        return None
    groups = match.groups()
    filename = groups[0]
    operation = groups[1]
    return (filename, operation)


def parse_rclone_sync_stderr(
    stderr: typing.IO[str],
) -> collections.abc.Generator[tuple[str, str], None, None]:
    for line in stderr:
        line_result = parse_rclone_sync_line(line)
        if line_result is not None:
            yield line_result


def parse_stdout() -> collections.abc.Generator[tuple[str, str], None, None]:
    with subprocess.Popen(
        [
            "rclone",
            "sync",
            "--dry-run",
            "tests/test_rclone_pyside6",
            "/home/boni/base/tmp",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        stderr = process.stderr
        assert stderr is not None
        try:
            yield from parse_rclone_sync_stderr(stderr)
        finally:
            process.kill()
            process.communicate()


def main() -> int:  # pragma: no cover
    for line_result in parse_stdout():
        print(line_result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
