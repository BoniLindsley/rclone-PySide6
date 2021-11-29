#!/usr/bin/env python3

# Internal modules.
import rclone_pyside6.greet


class TestHello:
    def test_prints_hello(self) -> None:
        stdout_buffer: list[str] = []
        rclone_pyside6.greet.hello("Alice", echo=stdout_buffer.append)
        assert stdout_buffer == ["Hello, Alice!"]

    def test_prints_nothing_if_name_is_blank(self) -> None:
        stdout_buffer: list[str] = []
        rclone_pyside6.greet.hello("", echo=stdout_buffer.append)
        assert stdout_buffer == []


class TestHelloAll:
    def test_prints_hello_for_each_non_empty_name(self) -> None:
        stdout_buffer: list[str] = []
        rclone_pyside6.greet.hello_all(
            "Alice", "Bell", "", "Delta", echo=stdout_buffer.append
        )
        assert stdout_buffer == [
            "Hello, Alice!",
            "Hello, Bell!",
            "Hello, Delta!",
        ]

    def test_prints_nothing_if_no_name_given(self) -> None:
        stdout_buffer: list[str] = []
        rclone_pyside6.greet.hello_all(echo=stdout_buffer.append)
        assert stdout_buffer == []
