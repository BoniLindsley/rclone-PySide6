#!/usr/bin/env python3

# External dependencies.
import PySide6.QtWidgets

# Internal modules.
import rclone_pyside6.gui.generated_ui.main_window


class MainWindow(PySide6.QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = rclone_pyside6.gui.generated_ui.main_window.Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore[no-untyped-call]


class TestUi_MainWindow:  # pylint: disable=invalid-name
    def test_setup_from_owner(
        self, q_application: PySide6.QtWidgets.QApplication
    ) -> None:
        del q_application
        MainWindow()

    def test_setup_outside_owner_with_object_name(
        self, q_application: PySide6.QtWidgets.QApplication
    ) -> None:
        del q_application
        main_window = PySide6.QtWidgets.QMainWindow()
        main_window.setObjectName("MainWindow2")
        ui = rclone_pyside6.gui.generated_ui.main_window.Ui_MainWindow()
        ui.setupUi(main_window)
