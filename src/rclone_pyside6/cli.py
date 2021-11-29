#!/usr/bin/env python3

# External dependencies.
import click

# Internal packages.
from . import greet


@click.command()
@click.argument("names", nargs=-1)
def group(names: list[str]) -> None:
    greet.hello_all(*names, echo=click.echo)
