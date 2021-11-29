#!/usr/bin/env python3

# Standard library.
from __future__ import annotations
import collections.abc
import typing


def hello(
    name: str, *, echo: collections.abc.Callable[[str], typing.Any]
) -> None:
    if name:
        echo(f"Hello, {name}!")


def hello_all(
    *names: str, echo: collections.abc.Callable[[str], typing.Any]
) -> None:
    for name in names:
        hello(name, echo=echo)
