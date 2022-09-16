#!/usr/bin/env python3

# Standard libraries.
import ast
import collections.abc
import gettext
import itertools
import logging
import pathlib
import subprocess
import typing

# External dependencies.
import click

_T = typing.TypeVar("_T")
UnaryOperator = typing.Callable[[_T], _T]
AnyCallable = collections.abc.Callable[..., typing.Any]

_logger = logging.getLogger(__name__)


def get_project_root(file_path: pathlib.Path) -> pathlib.Path:
    root_files = [
        "pyproject.toml",
        "setup.cfg",
        "setup.py",
    ]
    _logger.debug("Searching in parents for %s", root_files)
    for directory in file_path.parents:
        for filename in root_files:
            if (directory / filename).exists():
                return directory
    raise FileNotFoundError("No project root files found in parents.")


def get_src_directory(file_path: pathlib.Path) -> pathlib.Path:
    try:
        project_root = get_project_root(file_path)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            str(error) + f" Started from {file_path}"
        ) from error
    src_directory = project_root / "src"
    _logger.debug("Using project root %s", project_root)
    if not src_directory.exists():
        raise FileNotFoundError(
            "Source directory not found in project root: {src_directory}"
        )
    return src_directory


def ui_paths(
    file_path: pathlib.Path,
) -> collections.abc.Iterator[pathlib.Path]:
    try:
        src_directory = get_src_directory(file_path)
    except FileNotFoundError as error:
        _logger.error("Cannot find src directory: %s", error)
        click.get_current_context().exit(1)
    _logger.debug(
        "Searching for .ui files to compile in %s", src_directory
    )
    yield from src_directory.glob("**/*.ui")


def compile_file(
    ui_path: pathlib.Path, *, compiler: str = "pyside6-uic"
) -> bytes:
    try:
        return subprocess.check_output([compiler, ui_path])
    except subprocess.CalledProcessError as error:
        _logger.error("Failed to compile.\n%s", error.stdout.decode())
        click.get_current_context().exit(1)
    assert False, "Unreachable"


def compiler_option(
    *args: str, **kwargs: typing.Any
) -> UnaryOperator[AnyCallable]:
    if not args:
        args = ("--compiler",)
    kwargs.setdefault("default", "pyside6-uic")
    kwargs.setdefault(
        "help", gettext.gettext("program to compile .ui to .py")
    )
    kwargs.setdefault("show_default", True)
    return click.option(*args, **kwargs)


@click.group()
def group() -> None:
    _logger.addHandler(logging.StreamHandler())
    _logger.setLevel(logging.WARNING)


@group.command()
@compiler_option()
def update(compiler: str) -> None:
    for ui_path in ui_paths(pathlib.Path(__file__)):
        _logger.info("Compiling %s", ui_path)
        ui_code = compile_file(ui_path, compiler=compiler)
        ui_module_path = ui_path.with_suffix(".py")
        ui_module_path.write_bytes(ui_code)


def compare_ast(node: ast.AST, other: ast.AST) -> bool:
    ignored_fields = {
        "lineno",
        "col_offset",
        "end_lineno",
        "end_col_offset",
    }
    for child, other_child in itertools.zip_longest(
        ast.walk(node), ast.walk(other)
    ):
        if type(child) != type(  # pylint: disable=unidiomatic-typecheck
            other_child
        ):
            return False
        available_field_names = set(child._fields)
        if available_field_names != set(other_child._fields):
            return False
        available_field_names.difference_update(ignored_fields)
        for field_name in available_field_names:
            child_field = getattr(child, field_name)
            other_child_field = getattr(other_child, field_name)
            if type(child_field) != type(  # pylint: disable=unidiomatic-typecheck
                other_child_field
            ):
                return False
            if isinstance(child_field, ast.AST):
                continue
            if isinstance(child_field, list):
                continue
            if child_field != other_child_field:
                return False
    return True


@group.command()
@compiler_option()
def check(compiler: str) -> None:
    for ui_path in ui_paths(pathlib.Path(__file__)):
        _logger.debug("Checking %s", ui_path)
        ui_code = compile_file(ui_path, compiler=compiler)
        ui_module_path = ui_path.with_suffix(".py")
        try:
            ui_module_code = ui_module_path.read_bytes()
        except FileNotFoundError:
            ui_module_code = b""
        if ui_module_code == ui_code:
            continue
        ui_ast = ast.parse(ui_code)
        ui_module_ast = ast.parse(ui_module_code)
        if not compare_ast(ui_module_ast, ui_ast):
            _logger.error("Outdated %s", ui_module_path)
            click.get_current_context().exit(1)


if __name__ == "__main__":
    group()
