#!/usr/bin/env python3

# Standard libraries.
import sys

# External dependencies.
import PySide6.QtCore
import PySide6.QtWidgets

# Internal modules.
from .generated_ui.main_window import Ui_MainWindow


class MainWindow(PySide6.QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore[no-untyped-call]


def add_data(tree_widget: PySide6.QtWidgets.QTreeWidget) -> None:
    items = []
    data: dict[str, list[str]] = {
        "Project A": ["file_a.py", "file_a.txt", "something.xls"],
        "Project B": ["file_b.csv", "photo.jpg"],
        "Project C": [],
    }
    for key, values in data.items():
        item = PySide6.QtWidgets.QTreeWidgetItem([key])
        for value in values:
            ext = value.split(".")[-1].upper()
            child = PySide6.QtWidgets.QTreeWidgetItem([value, ext])
            item.addChild(child)
        items.append(item)
    tree_widget.insertTopLevelItems(0, items)


def main() -> int:
    qt_app = PySide6.QtWidgets.QApplication()
    main_window = MainWindow()
    tree_widget = main_window.ui.centralwidget
    tree_widget.setHeaderLabels(["Name", "Type"])
    add_data(tree_widget)
    main_window.show()
    return qt_app.exec()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
