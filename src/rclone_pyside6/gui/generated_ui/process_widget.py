# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'process_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(274, 270)
        self.actionStart = QAction(Form)
        self.actionStart.setObjectName(u"actionStart")
        self.actionStop = QAction(Form)
        self.actionStop.setObjectName(u"actionStop")
        self.actionKill = QAction(Form)
        self.actionKill.setObjectName(u"actionKill")
        self.processLayout = QVBoxLayout(Form)
        self.processLayout.setObjectName(u"processLayout")
        self.command = QLineEdit(Form)
        self.command.setObjectName(u"command")

        self.processLayout.addWidget(self.command)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.start = QPushButton(Form)
        self.start.setObjectName(u"start")

        self.hboxLayout.addWidget(self.start)

        self.stop = QPushButton(Form)
        self.stop.setObjectName(u"stop")

        self.hboxLayout.addWidget(self.stop)

        self.kill = QPushButton(Form)
        self.kill.setObjectName(u"kill")

        self.hboxLayout.addWidget(self.kill)


        self.processLayout.addLayout(self.hboxLayout)

        self.output = QPlainTextEdit(Form)
        self.output.setObjectName(u"output")

        self.processLayout.addWidget(self.output)


        self.retranslateUi(Form)
        self.start.clicked.connect(self.output.clear)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        self.actionStart.setText(QCoreApplication.translate("Form", u"Start", None))
        self.actionStop.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.actionKill.setText(QCoreApplication.translate("Form", u"Kill", None))
        self.start.setText(QCoreApplication.translate("Form", u"Start", None))
        self.stop.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.kill.setText(QCoreApplication.translate("Form", u"Kill", None))
        pass
    # retranslateUi

