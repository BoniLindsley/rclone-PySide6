# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QToolBar, QToolBox, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(783, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.remoteControlToolBox = QToolBox(self.centralwidget)
        self.remoteControlToolBox.setObjectName(u"remoteControlToolBox")
        self.serverPage = QWidget()
        self.serverPage.setObjectName(u"serverPage")
        self.serverPage.setGeometry(QRect(0, 0, 751, 544))
        self.verticalLayout = QVBoxLayout(self.serverPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.connectionGroupBox = QGroupBox(self.serverPage)
        self.connectionGroupBox.setObjectName(u"connectionGroupBox")
        self.connectionGroupBox.setCheckable(True)
        self.formLayout = QFormLayout(self.connectionGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.addressLabel = QLabel(self.connectionGroupBox)
        self.addressLabel.setObjectName(u"addressLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.addressLabel)

        self.addressLineEdit = QLineEdit(self.connectionGroupBox)
        self.addressLineEdit.setObjectName(u"addressLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.addressLineEdit)

        self.portLabel = QLabel(self.connectionGroupBox)
        self.portLabel.setObjectName(u"portLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.portLabel)

        self.portSpinBox = QSpinBox(self.connectionGroupBox)
        self.portSpinBox.setObjectName(u"portSpinBox")
        self.portSpinBox.setMaximum(65535)
        self.portSpinBox.setValue(5572)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.portSpinBox)


        self.verticalLayout.addWidget(self.connectionGroupBox)

        self.authenticationGroupBox = QGroupBox(self.serverPage)
        self.authenticationGroupBox.setObjectName(u"authenticationGroupBox")
        self.authenticationGroupBox.setCheckable(True)
        self.formLayout_2 = QFormLayout(self.authenticationGroupBox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.realmLabel = QLabel(self.authenticationGroupBox)
        self.realmLabel.setObjectName(u"realmLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.realmLabel)

        self.realmLineEdit = QLineEdit(self.authenticationGroupBox)
        self.realmLineEdit.setObjectName(u"realmLineEdit")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.realmLineEdit)

        self.userLabel = QLabel(self.authenticationGroupBox)
        self.userLabel.setObjectName(u"userLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.userLabel)

        self.userLineEdit = QLineEdit(self.authenticationGroupBox)
        self.userLineEdit.setObjectName(u"userLineEdit")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.userLineEdit)

        self.passwordLabel = QLabel(self.authenticationGroupBox)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(self.authenticationGroupBox)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.passwordLineEdit)


        self.verticalLayout.addWidget(self.authenticationGroupBox)

        self.hostGroupBox = QGroupBox(self.serverPage)
        self.hostGroupBox.setObjectName(u"hostGroupBox")
        self.hostGroupBox.setCheckable(True)
        self.verticalLayout_3 = QVBoxLayout(self.hostGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.hostActionWidget = QWidget(self.hostGroupBox)
        self.hostActionWidget.setObjectName(u"hostActionWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.hostActionWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.hostActionPushButton = QPushButton(self.hostActionWidget)
        self.hostActionPushButton.setObjectName(u"hostActionPushButton")

        self.horizontalLayout_3.addWidget(self.hostActionPushButton)

        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.hostActionWidget)

        self.hostLogPlainTextEdit = QPlainTextEdit(self.hostGroupBox)
        self.hostLogPlainTextEdit.setObjectName(u"hostLogPlainTextEdit")
        self.hostLogPlainTextEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.hostLogPlainTextEdit)


        self.verticalLayout.addWidget(self.hostGroupBox)

        self.serverStatusWidget = QWidget(self.serverPage)
        self.serverStatusWidget.setObjectName(u"serverStatusWidget")
        self.verticalLayout_6 = QVBoxLayout(self.serverStatusWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.serverStatusWidget_2 = QWidget(self.serverStatusWidget)
        self.serverStatusWidget_2.setObjectName(u"serverStatusWidget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.serverStatusWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.serverStatusPushButton = QPushButton(self.serverStatusWidget_2)
        self.serverStatusPushButton.setObjectName(u"serverStatusPushButton")

        self.horizontalLayout_2.addWidget(self.serverStatusPushButton)

        self.serverStatusSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.serverStatusSpacer)


        self.verticalLayout_6.addWidget(self.serverStatusWidget_2)

        self.serverLogPlainTextEdit = QPlainTextEdit(self.serverStatusWidget)
        self.serverLogPlainTextEdit.setObjectName(u"serverLogPlainTextEdit")
        self.serverLogPlainTextEdit.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.serverLogPlainTextEdit)


        self.verticalLayout.addWidget(self.serverStatusWidget)

        self.serverSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.serverSpacer)

        self.remoteControlToolBox.addItem(self.serverPage, u"Server")
        self.remotesPage = QWidget()
        self.remotesPage.setObjectName(u"remotesPage")
        self.remotesPage.setGeometry(QRect(0, 0, 765, 440))
        self.verticalLayout_2 = QVBoxLayout(self.remotesPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.remotesActionWidget = QWidget(self.remotesPage)
        self.remotesActionWidget.setObjectName(u"remotesActionWidget")
        self.horizontalLayout = QHBoxLayout(self.remotesActionWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.remotesConnectionPushButton = QPushButton(self.remotesActionWidget)
        self.remotesConnectionPushButton.setObjectName(u"remotesConnectionPushButton")

        self.horizontalLayout.addWidget(self.remotesConnectionPushButton)

        self.remotesAddPushButton = QPushButton(self.remotesActionWidget)
        self.remotesAddPushButton.setObjectName(u"remotesAddPushButton")
        self.remotesAddPushButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.remotesAddPushButton)

        self.remotesRemovePushButton = QPushButton(self.remotesActionWidget)
        self.remotesRemovePushButton.setObjectName(u"remotesRemovePushButton")
        self.remotesRemovePushButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.remotesRemovePushButton)

        self.remotesBrowsePushButton = QPushButton(self.remotesActionWidget)
        self.remotesBrowsePushButton.setObjectName(u"remotesBrowsePushButton")
        self.remotesBrowsePushButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.remotesBrowsePushButton)

        self.remotesSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.remotesSpacer)


        self.verticalLayout_2.addWidget(self.remotesActionWidget)

        self.remoteListWidget = QListWidget(self.remotesPage)
        self.remoteListWidget.setObjectName(u"remoteListWidget")

        self.verticalLayout_2.addWidget(self.remoteListWidget)

        self.remoteControlToolBox.addItem(self.remotesPage, u"Remotes")
        self.browsePage = QWidget()
        self.browsePage.setObjectName(u"browsePage")
        self.browsePage.setGeometry(QRect(0, 0, 139, 162))
        self.verticalLayout_5 = QVBoxLayout(self.browsePage)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.commandWidget = QWidget(self.browsePage)
        self.commandWidget.setObjectName(u"commandWidget")
        self.formLayout_3 = QFormLayout(self.commandWidget)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.sourceLabel = QLabel(self.commandWidget)
        self.sourceLabel.setObjectName(u"sourceLabel")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.sourceLabel)

        self.sourceLineEdit = QLineEdit(self.commandWidget)
        self.sourceLineEdit.setObjectName(u"sourceLineEdit")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.sourceLineEdit)

        self.destinationLabel = QLabel(self.commandWidget)
        self.destinationLabel.setObjectName(u"destinationLabel")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.destinationLabel)

        self.destinationLineEdit = QLineEdit(self.commandWidget)
        self.destinationLineEdit.setObjectName(u"destinationLineEdit")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.destinationLineEdit)


        self.verticalLayout_5.addWidget(self.commandWidget)

        self.browseTreeWidget = QTreeWidget(self.browsePage)
        self.browseTreeWidget.setObjectName(u"browseTreeWidget")

        self.verticalLayout_5.addWidget(self.browseTreeWidget)

        self.remoteControlToolBox.addItem(self.browsePage, u"Browse")

        self.verticalLayout_4.addWidget(self.remoteControlToolBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 783, 19))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
#if QT_CONFIG(shortcut)
        self.addressLabel.setBuddy(self.addressLineEdit)
        self.portLabel.setBuddy(self.portSpinBox)
        self.realmLabel.setBuddy(self.realmLineEdit)
        self.userLabel.setBuddy(self.userLineEdit)
        self.passwordLabel.setBuddy(self.passwordLineEdit)
        self.sourceLabel.setBuddy(self.sourceLineEdit)
        self.destinationLabel.setBuddy(self.destinationLineEdit)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.connectionGroupBox, self.addressLineEdit)
        QWidget.setTabOrder(self.addressLineEdit, self.portSpinBox)
        QWidget.setTabOrder(self.portSpinBox, self.authenticationGroupBox)
        QWidget.setTabOrder(self.authenticationGroupBox, self.realmLineEdit)
        QWidget.setTabOrder(self.realmLineEdit, self.userLineEdit)
        QWidget.setTabOrder(self.userLineEdit, self.passwordLineEdit)
        QWidget.setTabOrder(self.passwordLineEdit, self.hostGroupBox)
        QWidget.setTabOrder(self.hostGroupBox, self.remotesAddPushButton)
        QWidget.setTabOrder(self.remotesAddPushButton, self.remotesRemovePushButton)
        QWidget.setTabOrder(self.remotesRemovePushButton, self.remoteListWidget)
        QWidget.setTabOrder(self.remoteListWidget, self.sourceLineEdit)
        QWidget.setTabOrder(self.sourceLineEdit, self.destinationLineEdit)
        QWidget.setTabOrder(self.destinationLineEdit, self.browseTreeWidget)

        self.retranslateUi(MainWindow)

        self.remoteControlToolBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.connectionGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.addressLabel.setText(QCoreApplication.translate("MainWindow", u"Address", None))
        self.addressLineEdit.setText(QCoreApplication.translate("MainWindow", u"localhost", None))
        self.portLabel.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.authenticationGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Authentication", None))
        self.realmLabel.setText(QCoreApplication.translate("MainWindow", u"Realm", None))
        self.realmLineEdit.setText(QCoreApplication.translate("MainWindow", u"rclone", None))
        self.userLabel.setText(QCoreApplication.translate("MainWindow", u"User", None))
        self.passwordLabel.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.hostGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Host", None))
        self.hostActionPushButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.serverStatusPushButton.setText(QCoreApplication.translate("MainWindow", u"Check", None))
        self.remoteControlToolBox.setItemText(self.remoteControlToolBox.indexOf(self.serverPage), QCoreApplication.translate("MainWindow", u"Server", None))
        self.remotesConnectionPushButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.remotesAddPushButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.remotesRemovePushButton.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.remotesBrowsePushButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.remoteControlToolBox.setItemText(self.remoteControlToolBox.indexOf(self.remotesPage), QCoreApplication.translate("MainWindow", u"Remotes", None))
        self.sourceLabel.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.destinationLabel.setText(QCoreApplication.translate("MainWindow", u"Destination", None))
        ___qtreewidgetitem = self.browseTreeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Action", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Destination", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Source", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Path", None));
        self.remoteControlToolBox.setItemText(self.remoteControlToolBox.indexOf(self.browsePage), QCoreApplication.translate("MainWindow", u"Browse", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

