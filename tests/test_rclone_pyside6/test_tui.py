#!/usr/bin/env python3

# Standard libraries.
import io

# Internal modules
from rclone_pyside6.tui import parse_rclone_sync_stderr, parse_rclone_sync_line


class TestParseRcloneSyncLine:
    def test_returns_filename_and_operation(self) -> None:
        line = "<5>NOTICE: x: Skipped copy as --dry-run is set (size 0)"
        result = parse_rclone_sync_line(line)
        assert result is not None
        assert result[0] == "x"
        assert result[1] == "copy"
        assert len(result) == 2

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


class TestParseRcloneSyncStderr:
    def test_returns_files_to_change(self) -> None:
        stream = io.StringIO(
            "<5>NOTICE: x: Skipped copy as --dry-run is set (size 0)\n"
            "<5>NOTICE: y: Skipped delete as --dry-run is set (size 0)\n"
            "<5>NOTICE: \n"
            "Transferred:              0 B / 0 B, -, 0 B/s, ETA -\n"
            "Checks:                 1 / 1, 100%\n"
            "Deleted:                1 (files), 0 (dirs)\n"
            "Transferred:            1 / 1, 100%\n"
            "Elapsed time:         0.0s\n"
        )
        result = list(parse_rclone_sync_stderr(stream))
        assert result[0] == ("x", "copy")
        assert result[1] == ("y", "delete")
        assert len(result) == 2

    def test_okay_if_no_operations(self) -> None:
        stream = io.StringIO(
            "<6>INFO  : There was nothing to transfer\n"
            "<5>NOTICE: \n"
            "Transferred:              0 B / 0 B, -, 0 B/s, ETA -\n"
            "Elapsed time:         0.0s\n"
        )
        result = list(parse_rclone_sync_stderr(stream))
        assert len(result) == 0
