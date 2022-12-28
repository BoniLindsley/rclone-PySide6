#!/usr/bin/env python3

# Standard libraries.
import enum
import re
import typing
import warnings


class Operation(enum.IntEnum):
    COPY = enum.auto()
    DELETE = enum.auto()
    SYNC = enum.auto()


def parse_operation(word: str) -> Operation | str:
    upper = word.upper()
    try:
        return Operation[upper]
    except KeyError:
        return word
    assert False  # pragma: no cover


class Target(enum.IntEnum):
    SOURCE = enum.auto()
    DESTINATION = enum.auto()


class SyncLine(typing.NamedTuple):
    path: str
    operation: Operation | str
    target: Target


def parse_rclone_sync_line(line: str) -> SyncLine | None:
    pattern = re.compile(
        # "abcdefg NOTICE: directory/filename.txt:"
        #  " Skipped copy as --dry-run is set (size 123.456 Ki)"
        r"^.*?"  # Non-greedy search for any leading string up to "NOTICE".
        r"NOTICE: (.*)"  # Capture path.
        r": Skipped (\w+)"  # Capture skipped operation.
        r" as --dry-run is set \(size "  # Filler literal.
        r"\d+(\.\d*)?"  # Match integer or decimal. E.g. 123 or 123.456
        r"(?:[KMGTP]i)?"  # Match filesize units: Ki, Mi, etc
        r"\)$"  # Closing paranthesis at the end.
    )
    match = pattern.match(line)
    if match is None:
        return None
    groups = match.groups()
    return SyncLine(
        path=groups[0],
        operation=parse_operation(groups[1]),
        target=Target.DESTINATION,
    )


def to_choice_line_from_sync_line(sync_line: SyncLine) -> str:
    operation = sync_line.operation
    # Right-pad with spaces for alignment of paths.
    if isinstance(operation, Operation):
        prefix = operation.name.lower().ljust(6)
    # Prepend with has if operation is unknown.
    # Acts as comment to be ignored, while letting user edit if useful.
    else:
        prefix = "# " + operation
    return f"{prefix} {sync_line.path}"


def parse_choice_line(line: str) -> SyncLine | None:
    line = line.strip()
    if not line:
        return None
    if line[0] == "#":
        return None
    prefix, _, path = line.partition(" ")
    operation = parse_operation(prefix.strip())
    if not isinstance(operation, Operation):
        warnings.warn("Unable to parse prefix: f{prefix}")
        return None
    path = path.strip()
    return SyncLine(path=path, operation=operation, target=Target.DESTINATION)
