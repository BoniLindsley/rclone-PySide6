#!/usr/bin/env python3

# Standard library.
from __future__ import annotations
import sys

# External dependencies.
import click

# Internal packages.
from . import greet  # pylint: disable=relative-beyond-top-level


@click.command()
@click.argument("names", nargs=-1)
def main(names: list[str]) -> int:  # pragma: no cover
    greet.hello_all(*names, stdout=sys.stdout)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
