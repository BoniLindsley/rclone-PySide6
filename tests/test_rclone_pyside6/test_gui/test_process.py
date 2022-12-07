#!/usr/bin/env python3

# External dependencies.
import PySide6.QtWidgets

# Internal modules
import rclone_pyside6.gui.process


def test_process_default_constructor(
    q_application: PySide6.QtWidgets.QApplication,
) -> None:
    del q_application
    process = rclone_pyside6.gui.process.Process()
    assert process is not None
