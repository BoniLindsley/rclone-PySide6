#!/usr/bin/env python3

# External dependencies.
import pytest

# Internal modules.
from rclone_pyside6.parse import (
    Operation,
    SyncLine,
    Target,
    parse_operation,
    parse_rclone_sync_line,
    to_choice_line_from_sync_line,
    parse_choice_line,
)


class TestOperation:
    def test_has_expected_members(self) -> None:
        _ = Operation.COPY
        _ = Operation.DELETE
        _ = Operation.SYNC


class TestParseAsOperation:
    def test_returns_operation_for_known_operations(self) -> None:
        result = parse_operation("SYNC")
        assert result == Operation.SYNC

    def test_accepts_non_upper_case(self) -> None:
        result = parse_operation("cOpY")
        assert result == Operation.COPY

    def test_returns_given_string_if_unknown(self) -> None:
        bad_operation = "????"
        result = parse_operation(bad_operation)
        assert result is bad_operation


class TestTarget:
    def test_has_expected_members(self) -> None:
        _ = Target.SOURCE
        _ = Target.DESTINATION


class TestSyncLine:
    def test_has_expected_members(self) -> None:
        _ = SyncLine(path="dir", operation=Operation.DELETE, target=Target.SOURCE)


class TestParseRcloneSyncLine:
    def test_returns_path_and_operation(self) -> None:
        line = "<5>NOTICE: x: Skipped copy as --dry-run is set (size 0)"
        result = parse_rclone_sync_line(line)
        assert result is not None
        assert result.path == "x"
        assert result.operation == Operation.COPY

    def test_ignores_empty_notice(self) -> None:
        line = "<5>NOTICE:"
        result = parse_rclone_sync_line(line)
        assert result is None

    def test_ignores_non_notice_lines(self) -> None:
        line = "Transferred:              0 B / 0 B, -, 0 B/s, ETA -"
        result = parse_rclone_sync_line(line)
        assert result is None

    def test_ignores_empty_line(self) -> None:
        line = ""
        result = parse_rclone_sync_line(line)
        assert result is None


class TestToChoiceLineFromSyncLine:
    def test_returns_copy_and_path(self) -> None:
        sync_line = SyncLine(
            path="dir_path", operation=Operation.COPY, target=Target.DESTINATION
        )
        result = to_choice_line_from_sync_line(sync_line)
        assert result == "copy   dir_path"

    def test_prepends_hash_to_unknown_operation(self) -> None:
        sync_line = SyncLine(path="world", operation="hello", target=Target.DESTINATION)
        result = to_choice_line_from_sync_line(sync_line)
        assert result == "# hello world"


class TestParseChoiceLine:
    def test_returns_copy_and_path(self) -> None:
        choice_line = "copy dir_path"
        result = parse_choice_line(choice_line)
        assert result == SyncLine(
            path="dir_path", operation=Operation.COPY, target=Target.DESTINATION
        )

    def test_ignores_empty_lines(self) -> None:
        choice_line = ""
        result = parse_choice_line(choice_line)
        assert result is None

    def test_ignores_hash_comment_line(self) -> None:
        choice_line = "# copy dir_path"
        result = parse_choice_line(choice_line)
        assert result is None

    def test_ignores_leading_and_trailing_spaces(self) -> None:
        choice_line = "   delete file_path   "
        result = parse_choice_line(choice_line)
        assert result == SyncLine(
            path="file_path", operation=Operation.DELETE, target=Target.DESTINATION
        )

    def test_ignores_spaces_after_operation(self) -> None:
        choice_line = "copy   file_path"
        result = parse_choice_line(choice_line)
        assert result == SyncLine(
            path="file_path", operation=Operation.COPY, target=Target.DESTINATION
        )

    def test_ignores_and_warns_for_unknown_operation(self) -> None:
        choice_line = "??? file_path"
        with pytest.warns():
            result = parse_choice_line(choice_line)
        assert result is None
