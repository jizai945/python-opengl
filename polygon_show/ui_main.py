# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainLcGixI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from myglwidget import MyGLWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 600)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.openGLWidget = MyGLWidget(Form)
        self.openGLWidget.setObjectName(u"openGLWidget")

        self.verticalLayout.addWidget(self.openGLWidget)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.le_file = QLineEdit(self.widget)
        self.le_file.setObjectName(u"le_file")
        self.le_file.setEnabled(False)

        self.horizontalLayout.addWidget(self.le_file)

        self.btn_file = QPushButton(self.widget)
        self.btn_file.setObjectName(u"btn_file")

        self.horizontalLayout.addWidget(self.btn_file)


        self.verticalLayout.addWidget(self.widget)

        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_file.setText(QCoreApplication.translate("Form", u"\u9009\u62e9", None))
    # retranslateUi

