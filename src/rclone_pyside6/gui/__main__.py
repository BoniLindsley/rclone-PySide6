#!/usr/bin/env python3

# mypy notes:
# -   ignore[arg-type]: QState.assignProperty argument 2
#     wants bytes at runtime but wants str when type checking.
# -   ignore[attr-defined]: PySide6 signals are not always defined.

# Standard libraries.
from __future__ import annotations  # For delayed type expansion < 3.10.
import collections.abc
import datetime
import json
import logging
import secrets
import sys
import typing

# External dependencies.
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtNetwork
import PySide6.QtWidgets
import PySide6.QtStateMachine

# Internal modules.
from .generated_ui.main_window import Ui_MainWindow
from .process import find_child

_T_co = typing.TypeVar("_T_co")

_logger = logging.getLogger(__name__)


class NetworkCommunication(PySide6.QtCore.QObject):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)
        self._address_port_enabled = False
        self._address = ""
        self._port = 5572
        self._authentication_enabled = False
        self._realm = "rclone"
        self._user = ""
        self._password = ""
        self._host_process = host_process = PySide6.QtCore.QProcess()
        host_process.setProgram("rclone")
        host_process.finished.connect(  # type: ignore[attr-defined]
            self._emit_host_finished
        )
        signal = host_process.readyReadStandardError  # type: ignore[attr-defined]
        signal.connect(self._emit_host_stderr_ready)
        signal = host_process.readyReadStandardOutput  # type: ignore[attr-defined]
        signal.connect(self._emit_host_stdout_ready)
        self._client = client = PySide6.QtNetwork.QNetworkAccessManager()
        signal = client.authenticationRequired  # type: ignore[attr-defined]
        signal.connect(self._on_authentication_required)
        signal = client.finished  # type: ignore[attr-defined]
        signal.connect(self._emit_client_reply_ready)

    def post_operations_list(
        self, remote: str, path: str
    ) -> PySide6.QtNetwork.QNetworkReply:
        data: dict[str, typing.Any] = {
            "fs": remote,
            "remote": path,
        }
        reply = self.post_command("operations/list", data)
        signal = reply.finished  # type: ignore[attr-defined]
        signal.connect(self._on_receive_operations_list_reply)
        return reply

    def _on_receive_operations_list_reply(self) -> None:
        reply = typing.cast(PySide6.QtNetwork.QNetworkReply, self.sender())
        try:
            json_data = json.loads(reply.readAll().data())
        except json.JSONDecodeError:
            json_data = {}
        dir_list = json_data.get("list", [])
        self.received_operations_list_reply.emit(dir_list)

    received_operations_list_reply = PySide6.QtCore.Signal(list)

    def post_config_listremotes(self) -> None:
        reply = self.post_command("config/listremotes")
        signal = reply.finished  # type: ignore[attr-defined]
        signal.connect(self._on_receive_config_listremotes_reply)

    def _on_receive_config_listremotes_reply(self) -> None:
        reply = typing.cast(PySide6.QtNetwork.QNetworkReply, self.sender())
        try:
            json_data = json.loads(reply.readAll().data())
        except json.JSONDecodeError:
            json_data = {}
        remotes = json_data.get("remotes", [])
        self.received_config_listremotes_reply.emit(remotes)

    received_config_listremotes_reply = PySide6.QtCore.Signal(list)

    def post_rc_noop(self) -> None:
        self.post_command("rc/noop", self._noop_data)

    _noop_data = {"noop": 1}

    def post_command(
        self, command: str, data: dict[str, typing.Any] | None = None
    ) -> PySide6.QtNetwork.QNetworkReply:
        request = PySide6.QtNetwork.QNetworkRequest()
        address = self._address or "localhost"
        url = PySide6.QtCore.QUrl(f"http://{address}:{self._port}/{command}")
        request.setUrl(url)
        encoded_data = b""
        if data is not None:
            encoded_data = json.dumps(data).encode()
            request.setHeader(
                PySide6.QtNetwork.QNetworkRequest.KnownHeaders.ContentTypeHeader,
                "application/json",
            )
        reply = self._client.post(request, encoded_data)
        self.client_request_sent.emit(reply)
        return reply

    client_request_sent = PySide6.QtCore.Signal(PySide6.QtNetwork.QNetworkReply)

    @PySide6.QtCore.Slot(PySide6.QtNetwork.QNetworkReply)
    def _emit_client_reply_ready(self, reply: PySide6.QtNetwork.QNetworkReply) -> None:
        self.client_reply_ready.emit(reply)

    client_reply_ready = PySide6.QtCore.Signal(PySide6.QtNetwork.QNetworkReply)

    def _on_authentication_required(
        self,
        reply: PySide6.QtNetwork.QNetworkReply,
        authenticator: PySide6.QtNetwork.QAuthenticator,
    ) -> None:
        del reply
        authenticator.setRealm(self._realm)
        authenticator.setUser(self._user)
        authenticator.setPassword(self._password)

    @PySide6.QtCore.Slot()
    def kill_host(self) -> None:
        self._host_process.kill()

    @PySide6.QtCore.Slot()
    def start_host(self) -> None:
        if self.is_host_running():
            return
        host_process = self._host_process
        signal = host_process.readyReadStandardError  # type: ignore[attr-defined]
        signal.connect(
            self._on_host_first_standard_error_ready,
            type=PySide6.QtCore.Qt.ConnectionType.SingleShotConnection,
        )
        host_process.start()

    def refresh_host_arguments(self) -> None:
        host_process = self._host_process
        arguments = ["rcd"]
        if self._authentication_enabled:
            arguments.extend(self._authentication_rc_arguments())
        if self._address_port_enabled:
            arguments.extend(self._address_port_rc_arguments())
        host_process.setArguments(arguments)

    def is_host_running(self) -> bool:
        return (
            self._host_process.state()
            != PySide6.QtCore.QProcess.ProcessState.NotRunning
        )

    def _address_port_rc_arguments(self) -> tuple[str]:
        return (f"--rc-addr={self._address}:{self._port}",)

    def _authentication_rc_arguments(self) -> tuple[str, str, str]:
        return (
            f"--rc-realm={self._realm}",
            f"--rc-user={self._user}",
            f"--rc-pass={self._password}",
        )

    @PySide6.QtCore.Slot()
    def _emit_host_finished(self) -> None:
        self.host_finished.emit()

    host_finished = PySide6.QtCore.Signal()

    @PySide6.QtCore.Slot()
    def _on_host_first_standard_error_ready(self) -> None:
        self.host_ready.emit()
        self.post_config_listremotes()

    host_ready = PySide6.QtCore.Signal()

    @PySide6.QtCore.Slot()
    def _emit_host_stderr_ready(self) -> None:
        self.host_stderr_ready.emit(
            self._host_process.readAllStandardError().data().decode()
        )

    host_stderr_ready = PySide6.QtCore.Signal(str)

    @PySide6.QtCore.Slot()
    def _emit_host_stdout_ready(self) -> None:
        self.host_stdout_ready.emit(
            self._host_process.readAllStandardOutput().data().decode()
        )

    host_stdout_ready = PySide6.QtCore.Signal(str)

    @PySide6.QtCore.Slot()
    def set_address_port_enabled(self, enabled: bool) -> None:
        self._address_port_enabled = enabled
        self.refresh_host_arguments()

    @PySide6.QtCore.Slot()
    def set_address(self, address: str) -> None:
        self._address = address
        self.refresh_host_arguments()

    @PySide6.QtCore.Slot()
    def set_port(self, port: int) -> None:
        self._port = port
        self.refresh_host_arguments()

    @PySide6.QtCore.Slot()
    def set_authentication_enabled(self, enabled: bool) -> None:
        self._authentication_enabled = enabled
        self.refresh_host_arguments()

    @PySide6.QtCore.Slot()
    def set_password(self, password: str) -> None:
        self._password = password
        self.refresh_host_arguments()

    @PySide6.QtCore.Slot()
    def set_realm(self, realm: str) -> None:
        self._realm = realm
        self.refresh_host_arguments()

    @PySide6.QtCore.Slot()
    def set_user(self, user: str) -> None:
        self._user = user
        self.refresh_host_arguments()


class MainWindowStateMachine(PySide6.QtStateMachine.QStateMachine):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)
        self.host_disabled = PySide6.QtStateMachine.QState()
        self.host_stopped = PySide6.QtStateMachine.QState()
        self.host_starting = PySide6.QtStateMachine.QState()
        self.host_started = PySide6.QtStateMachine.QState()
        self.host_stopping = PySide6.QtStateMachine.QState()

    def set_up(self) -> None:
        if self.initialState():
            pass
        states = (
            self.host_disabled,
            self.host_stopped,
            self.host_starting,
            self.host_started,
            self.host_stopping,
        )
        for state in states:
            self.addState(state)
        self.setInitialState(self.host_stopped)


class MainWindow(PySide6.QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        Ui_MainWindow().setupUi(self)  # type: ignore[no-untyped-call]
        self._remote_widget_items: dict[str, PySide6.QtWidgets.QListWidgetItem] = {}
        self.state_machine = state_machine = MainWindowStateMachine(self)
        self.network_communication = NetworkCommunication(self)
        self._set_up_states()
        state_machine.set_up()
        state_machine.start()

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        communication = self.network_communication
        if not communication.is_host_running():
            super().closeEvent(event)
            return
        communication = self.network_communication
        connection_type = PySide6.QtCore.Qt.ConnectionType.SingleShotConnection
        communication.host_finished.connect(
            self.close,
            connection_type,  # type: ignore [arg-type]
        )
        communication.kill_host()
        event.ignore()

    def _set_up_states(self) -> None:
        self._set_up_network_communication()
        self._set_up_connection_group_box()
        self._set_up_authentication_group_box()
        self._set_up_host_group_box()
        self._set_up_server_status_push_button()
        self._set_up_server_log_plain_text_edit()
        self._set_up_remotes_connection_push_button()
        self._set_up_remote_list_widget()
        self._set_up_browse_tree_widget()

    def _set_up_network_communication(self) -> None:
        communication = self.network_communication
        state_machine = self.state_machine
        signal = state_machine.host_disabled.entered  # type: ignore[attr-defined]
        signal.connect(communication.kill_host)
        signal = state_machine.host_starting.entered  # type: ignore[attr-defined]
        signal.connect(communication.start_host)
        state_machine.host_starting.addTransition(
            communication.host_ready,
            state_machine.host_started,
        )
        state_machine.host_starting.addTransition(
            communication.host_finished,
            state_machine.host_stopped,
        )
        signal = state_machine.host_stopping.entered  # type: ignore[attr-defined]
        signal.connect(communication.kill_host)
        state_machine.host_stopping.addTransition(
            communication.host_finished,
            state_machine.host_stopped,
        )
        signal = state_machine.host_disabled.entered  # type: ignore[attr-defined]
        signal.connect(communication.kill_host)

    def _set_up_connection_group_box(self) -> None:
        communication = self.network_communication
        group = find_child(self, PySide6.QtWidgets.QGroupBox, "connectionGroupBox")
        signal = group.toggled  # type: ignore[attr-defined]
        signal.connect(communication.set_address_port_enabled)
        communication.set_address_port_enabled(group.isChecked())
        state_machine = self.state_machine
        state_machine.host_stopped.assignProperty(
            group, "enabled", True  # type: ignore[arg-type]
        )
        state_machine.host_starting.assignProperty(
            group, "enabled", False  # type: ignore[arg-type]
        )
        self._set_up_address_line_edit()
        self._set_up_port_spin_box()

    def _set_up_address_line_edit(self) -> None:
        line_edit = find_child(self, PySide6.QtWidgets.QLineEdit, "addressLineEdit")
        slot = self.network_communication.set_address
        line_edit.textChanged.connect(slot)  # type: ignore[attr-defined]
        slot(line_edit.text())

    def _set_up_port_spin_box(self) -> None:
        slot = self.network_communication.set_port
        spin_box = find_child(self, PySide6.QtWidgets.QSpinBox, "portSpinBox")
        spin_box.textChanged.connect(slot)  # type: ignore[attr-defined]
        slot(spin_box.value())

    def _set_up_authentication_group_box(self) -> None:
        slot = self.network_communication.set_authentication_enabled
        group = find_child(self, PySide6.QtWidgets.QGroupBox, "authenticationGroupBox")
        group.toggled.connect(slot)  # type: ignore[attr-defined]
        slot(group.isChecked())
        state_machine = self.state_machine
        state_machine.host_stopped.assignProperty(
            group, "enabled", True  # type: ignore[arg-type]
        )
        state_machine.host_starting.assignProperty(
            group, "enabled", False  # type: ignore[arg-type]
        )
        self._set_up_realm_line_edit()
        self._set_up_user_line_edit()
        self._set_up_password_line_edit()

    def _set_up_realm_line_edit(self) -> None:
        slot = self.network_communication.set_realm
        line_edit = find_child(self, PySide6.QtWidgets.QLineEdit, "realmLineEdit")
        line_edit.textChanged.connect(slot)  # type: ignore[attr-defined]
        slot(line_edit.text())

    def _set_up_user_line_edit(self) -> None:
        line_edit = find_child(self, PySide6.QtWidgets.QLineEdit, "userLineEdit")
        line_edit.textChanged.connect(  # type: ignore[attr-defined]
            self.network_communication.set_user
        )
        line_edit.setText(secrets.token_urlsafe())

    def _set_up_password_line_edit(self) -> None:
        line_edit = find_child(self, PySide6.QtWidgets.QLineEdit, "passwordLineEdit")
        line_edit.textChanged.connect(  # type: ignore[attr-defined]
            self.network_communication.set_password
        )
        line_edit.setText(secrets.token_urlsafe())

    def _set_up_host_group_box(self) -> None:
        group = find_child(self, PySide6.QtWidgets.QGroupBox, "hostGroupBox")
        state_machine = self.state_machine
        state_machine.host_disabled.assignProperty(
            group, "checked", False  # type: ignore[arg-type]
        )
        state_machine.host_disabled.addTransition(
            group.clicked, state_machine.host_stopped  # type: ignore[attr-defined]
        )
        state_machine.host_stopped.addTransition(
            group.clicked, state_machine.host_disabled  # type: ignore[attr-defined]
        )
        state_machine.host_stopped.assignProperty(
            group, "checked", True  # type: ignore[arg-type]
        )
        state_machine.host_stopped.assignProperty(
            group, "checkable", True  # type: ignore[arg-type]
        )
        state_machine.host_starting.assignProperty(
            group, "checkable", False  # type: ignore[arg-type]
        )
        state_machine.host_started.assignProperty(
            group, "checked", True  # type: ignore[arg-type]
        )
        self._set_up_host_action_button()
        self._set_up_host_log_plain_text_edit()

    def _set_up_host_action_button(self) -> None:
        button = find_child(
            self,
            PySide6.QtWidgets.QPushButton,
            "hostActionPushButton",
        )
        state_machine = self.state_machine
        state_machine.host_stopped.assignProperty(
            button, "text", "Start"  # type: ignore[arg-type]
        )
        state_machine.host_stopped.addTransition(
            button.clicked, state_machine.host_starting  # type: ignore[attr-defined]
        )
        state_machine.host_starting.assignProperty(
            button, "text", "Stop"  # type: ignore[arg-type]
        )
        state_machine.host_starting.addTransition(
            button.clicked, state_machine.host_stopping  # type: ignore[attr-defined]
        )
        state_machine.host_started.addTransition(
            button.clicked, state_machine.host_stopping  # type: ignore[attr-defined]
        )
        state_machine.host_stopping.assignProperty(
            button, "text", "Force stop"  # type: ignore[arg-type]
        )
        state_machine.host_stopping.addTransition(
            button.clicked, state_machine.host_stopped  # type: ignore[attr-defined]
        )

    def _set_up_host_log_plain_text_edit(self) -> None:
        communication = self.network_communication
        log_text_edit = find_child(
            self,
            PySide6.QtWidgets.QPlainTextEdit,
            "hostLogPlainTextEdit",
        )
        communication.host_stderr_ready.connect(log_text_edit.appendPlainText)
        communication.host_stdout_ready.connect(log_text_edit.appendPlainText)

    def _set_up_server_status_push_button(self) -> None:
        button = find_child(
            self,
            PySide6.QtWidgets.QPushButton,
            "serverStatusPushButton",
        )
        signal = button.pressed  # type: ignore[attr-defined]
        signal.connect(self.network_communication.post_rc_noop)
        state_machine = self.state_machine
        state_machine.host_disabled.assignProperty(
            button, "enabled", True  # type: ignore[arg-type]
        )
        state_machine.host_stopped.assignProperty(
            button, "enabled", False  # type: ignore[arg-type]
        )
        state_machine.host_started.assignProperty(
            button, "enabled", True  # type: ignore[arg-type]
        )

    def _set_up_server_log_plain_text_edit(self) -> None:
        communication = self.network_communication
        communication.client_request_sent.connect(self._log_client_request)
        communication.client_reply_ready.connect(self._log_client_received_reply)

    @PySide6.QtCore.Slot(PySide6.QtNetwork.QNetworkReply)
    def _log_client_request(self, reply: PySide6.QtNetwork.QNetworkReply) -> None:
        request = reply.request()
        url = request.url().toString()
        now = datetime.datetime.now()
        log_text_edit = find_child(
            self,
            PySide6.QtWidgets.QPlainTextEdit,
            "serverLogPlainTextEdit",
        )
        write = log_text_edit.appendPlainText
        write(f"{now}: Sent to {url}")

    @PySide6.QtCore.Slot(PySide6.QtNetwork.QNetworkReply)
    def _log_client_received_reply(
        self, reply: PySide6.QtNetwork.QNetworkReply
    ) -> None:
        now = datetime.datetime.now()
        error = reply.error()
        if error is PySide6.QtNetwork.QNetworkReply.NetworkError.NoError:
            QNetworkRequest = PySide6.QtNetwork.QNetworkRequest
            status = str(
                reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
            )
        else:
            status = typing.cast(bytes, error.name).decode()
        url = reply.url().toString()
        log_text_edit = find_child(
            self,
            PySide6.QtWidgets.QPlainTextEdit,
            "serverLogPlainTextEdit",
        )
        write = log_text_edit.appendPlainText
        write(f"{now}: Received {status} from {url}")

    def _set_up_remotes_connection_push_button(self) -> None:
        button = find_child(
            self,
            PySide6.QtWidgets.QPushButton,
            "remotesConnectionPushButton",
        )
        button.pressed.connect(  # type: ignore[attr-defined]
            self._on_remotes_connection_push_button_pressed
        )
        state_machine = self.state_machine
        state_machine.host_disabled.assignProperty(
            button, "text", "Refresh"  # type: ignore[arg-type]
        )
        state_machine.host_stopped.assignProperty(
            button, "text", "Start"  # type: ignore[arg-type]
        )
        state_machine.host_stopped.addTransition(
            button.clicked, state_machine.host_starting  # type: ignore[attr-defined]
        )
        state_machine.host_starting.assignProperty(
            button, "text", "Refresh"  # type: ignore[arg-type]
        )

    def _on_remotes_connection_push_button_pressed(self) -> None:
        communication = self.network_communication
        if self.state_machine.host_disabled.active() or communication.is_host_running():
            communication.post_config_listremotes()

    def _set_up_remote_list_widget(self) -> None:
        signal = self.network_communication.received_config_listremotes_reply
        signal.connect(self._update_remote_list_widget_list)
        list_widget = find_child(
            self, PySide6.QtWidgets.QListWidget, "remoteListWidget"
        )
        list_widget.itemActivated.connect(  # type: ignore[attr-defined]
            self._on_remote_list_widget_item_activated
        )

    def _update_remote_list_widget_list(
        self, remotes: collections.abc.Iterable[str]
    ) -> None:
        updated_remotes = set(remotes)

        widget_items = self._remote_widget_items
        remotes_to_remove = set(widget_items.keys())
        remotes_to_remove.difference_update(updated_remotes)
        items_to_remove = filter(
            None,
            (widget_items.get(remote) for remote in remotes_to_remove),
        )
        for item in items_to_remove:
            item.deleteLater()  # type: ignore[attr-defined]

        remotes_to_add = updated_remotes.difference(widget_items.keys())
        list_widget = find_child(
            self, PySide6.QtWidgets.QListWidget, "remoteListWidget"
        )
        for remote in remotes_to_add:
            widget_items[remote] = PySide6.QtWidgets.QListWidgetItem(
                remote, list_widget
            )

    def _on_remote_list_widget_item_activated(self) -> None:
        list_widget = find_child(
            self, PySide6.QtWidgets.QListWidget, "remoteListWidget"
        )
        selected_remote_name = list_widget.currentItem().text()
        reply = self.network_communication.post_operations_list(
            f"{selected_remote_name}:", ""
        )
        signal = reply.finished  # type: ignore[attr-defined]
        signal.connect(self._on_reply_finished_to_remote_item_activated)

    def _on_reply_finished_to_remote_item_activated(self) -> None:
        reply = typing.cast(PySide6.QtNetwork.QNetworkReply, self.sender())
        if reply.error() == PySide6.QtNetwork.QNetworkReply.NetworkError.NoError:
            remote_control_tool_box = find_child(
                self,
                PySide6.QtWidgets.QToolBox,
                "remoteControlToolBox",
            )
            browse_page = find_child(
                self,
                PySide6.QtWidgets.QWidget,
                "browsePage",
            )
            remote_control_tool_box.setCurrentWidget(browse_page)
        else:
            self.statusBar().showMessage(
                "Failed to list remote.",
                int(datetime.timedelta(seconds=2) / datetime.timedelta(milliseconds=1)),
            )

    def _set_up_browse_tree_widget(self) -> None:
        signal = self.network_communication.received_operations_list_reply
        signal.connect(self._update_browse_tree_widget_list)

    def _update_browse_tree_widget_list(
        self, files: collections.abc.Iterable[dict[str, typing.Any]]
    ) -> None:
        tree_widget = find_child(
            self,
            PySide6.QtWidgets.QTreeWidget,
            "browseTreeWidget",
        )
        tree_widget.clear()
        for file in files:
            name = file.get("Name")
            if name is not None:
                PySide6.QtWidgets.QTreeWidgetItem(tree_widget, [name])


def main() -> int:
    qt_app = PySide6.QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.show()
    return qt_app.exec()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
