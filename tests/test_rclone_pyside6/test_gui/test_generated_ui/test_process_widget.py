#!/usr/bin/env python3

# External dependencies.
import PySide6.QtWidgets

# Internal modules.
import rclone_pyside6.gui.generated_ui.process_widget


class Widget(PySide6.QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = rclone_pyside6.gui.generated_ui.process_widget.Ui_Form()
        self.ui.setupUi(self)  # type: ignore[no-untyped-call]


class TestUi_Form:  # pylint: disable=invalid-name
    def test_setup_from_owner(
        self, q_application: PySide6.QtWidgets.QApplication
    ) -> None:
        del q_application
        Widget()

    def test_setup_outside_owner_with_object_name(
        self, q_application: PySide6.QtWidgets.QApplication
    ) -> None:
        del q_application
        widget = PySide6.QtWidgets.QWidget()
        widget.setObjectName("MainWindow2")
        ui = rclone_pyside6.gui.generated_ui.process_widget.Ui_Form()
        ui.setupUi(widget)  # type: ignore[no-untyped-call]
