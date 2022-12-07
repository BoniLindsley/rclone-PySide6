#!/usr/bin/env python3

# Standard libraries.
from __future__ import annotations  # For delayed type expansion < 3.10.
import enum
import sys
import typing

# External dependencies.
import PySide6.QtCore
import PySide6.QtStateMachine
import PySide6.QtWidgets

# Internal modules.
from .generated_ui.process_widget import Ui_Form as ProcessWidget

_T_co = typing.TypeVar("_T_co")


class ChildNotFound(Exception):
    pass


def find_child(
    parent: PySide6.QtCore.QObject, type_: type[_T_co], name: str
) -> _T_co:  # pragma: no cover
    child = typing.cast(_T_co, parent.findChild(type_, name))
    if child is None:
        raise ChildNotFound(f"Unable to find {type_} named {name}.")
    return child


class Process(PySide6.QtWidgets.QWidget):
    class States(enum.IntEnum):
        UNINITIALISED = enum.auto()
        STARTING = enum.auto()
        STARTED = enum.auto()
        STOPPING = enum.auto()
        STOPPED = enum.auto()

    class StateMachine(PySide6.QtStateMachine.QStateMachine):
        def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
            super().__init__(*args, **kwargs)
            self.states: dict[Process.States, PySide6.QtStateMachine.QAbstractState] = {
                Process.States.UNINITIALISED: PySide6.QtStateMachine.QState(),
                Process.States.STARTING: PySide6.QtStateMachine.QState(),
                Process.States.STARTED: PySide6.QtStateMachine.QState(),
                Process.States.STOPPING: PySide6.QtStateMachine.QState(),
                Process.States.STOPPED: PySide6.QtStateMachine.QFinalState(),
            }
            for state in self.states.values():
                self.addState(state)
            self.setInitialState(self.states[Process.States.UNINITIALISED])

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)
        ProcessWidget().setupUi(self)  # type: ignore[no-untyped-call]
        self._process = PySide6.QtCore.QProcess()
        self.state_machine = self.StateMachine(self)

    def set_process(self, process: PySide6.QtCore.QProcess) -> None:  # pragma: no cover
        self._process = process
        signal = process.readyReadStandardError  # type: ignore[attr-defined]
        signal.connect(self._read_process_stderr)
        signal = process.readyReadStandardOutput  # type: ignore[attr-defined]
        signal.connect(self._read_process_stdout)

    def _read_process_stderr(self) -> None:  # pragma: no cover
        process = self._process
        if process is None:
            return
        text = process.readAllStandardError().data().decode()
        self._append_log(text)

    def _read_process_stdout(self) -> None:  # pragma: no cover
        process = self._process
        if process is None:
            return
        text = process.readAllStandardOutput().data().decode()
        self._append_log(text)

    def _append_log(self, text: str) -> None:  # pragma: no cover
        output_widget = find_child(
            self,
            PySide6.QtWidgets.QPlainTextEdit,
            "output",
        )
        output_widget.appendPlainText(text)


def main() -> int:  # pragma: no cover
    qt_app = PySide6.QtWidgets.QApplication()
    process_widget = Process()
    main_window = PySide6.QtWidgets.QMainWindow()
    main_window.setCentralWidget(process_widget)
    main_window.show()
    return qt_app.exec()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
