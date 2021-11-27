#!/usr/bin/env python3

# Standard libraries.
import io

# Internal modules.
from rclone_pyside6 import greet


class TestHello:
    def test_prints_hello(self) -> None:
        stdout = io.StringIO()
        greet.hello("Alice", stdout=stdout)
        stdout_output = stdout.getvalue()
        assert stdout_output == "Hello, Alice!\n"

    def test_prints_nothing_if_name_is_blank(self) -> None:
        stdout = io.StringIO()
        greet.hello("", stdout=stdout)
        stdout_output = stdout.getvalue()
        assert not stdout_output


class TestHelloAll:
    def test_prints_hello_for_each_non_empty_name(self) -> None:
        stdout = io.StringIO()
        greet.hello_all("Alice", "Bell", "", "Delta", stdout=stdout)
        stdout_output = stdout.getvalue()
        expected_output = ""
        expected_output += "Hello, Alice!\n"
        expected_output += "Hello, Bell!\n"
        expected_output += "Hello, Delta!\n"
        assert stdout_output == expected_output

    def test_prints_nothing_if_no_name_given(self) -> None:
        stdout = io.StringIO()
        greet.hello_all(stdout=stdout)
        stdout_output = stdout.getvalue()
        assert not stdout_output
