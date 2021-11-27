#!/usr/bin/env python3

# Standard library.
from __future__ import annotations
import typing


def hello(name: str, *, stdout: typing.TextIO) -> None:
    if name:
        print(f"Hello, {name}!", file=stdout)


def hello_all(*names: str, stdout: typing.TextIO) -> None:
    for name in names:
        hello(name, stdout=stdout)
