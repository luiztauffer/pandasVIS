# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filter_variables.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(551, 408)
        self.textEdit_2 = QTextEdit(Dialog)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(20, 280, 511, 61))
        self.groupBox_1 = QGroupBox(Dialog)
        self.groupBox_1.setObjectName(u"groupBox_1")
        self.groupBox_1.setGeometry(QRect(10, 70, 531, 191))
        self.comboBox_1 = QComboBox(self.groupBox_1)
        self.comboBox_1.setObjectName(u"comboBox_1")
        self.comboBox_1.setGeometry(QRect(10, 30, 131, 22))
        self.comboBox_2 = QComboBox(self.groupBox_1)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(170, 30, 161, 22))
        self.lineEdit_1 = QLineEdit(self.groupBox_1)
        self.lineEdit_1.setObjectName(u"lineEdit_1")
        self.lineEdit_1.setGeometry(QRect(390, 70, 131, 22))
        self.comboBox_3 = QComboBox(self.groupBox_1)
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(390, 30, 131, 22))
        self.radioButton_2 = QRadioButton(self.groupBox_1)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(360, 70, 21, 20))
        self.radioButton_2.setChecked(False)
        self.radioButton_1 = QRadioButton(self.groupBox_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setGeometry(QRect(360, 30, 21, 20))
        self.radioButton_1.setChecked(True)
        self.textEdit_1 = QTextEdit(self.groupBox_1)
        self.textEdit_1.setObjectName(u"textEdit_1")
        self.textEdit_1.setGeometry(QRect(10, 110, 511, 31))
        self.pushButton_2 = QPushButton(self.groupBox_1)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(120, 150, 93, 28))
        self.pushButton_1 = QPushButton(self.groupBox_1)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.pushButton_1.setGeometry(QRect(10, 150, 93, 28))
        self.pushButton_accept = QPushButton(Dialog)
        self.pushButton_accept.setObjectName(u"pushButton_accept")
        self.pushButton_accept.setGeometry(QRect(160, 360, 93, 28))
        self.pushButton_cancel = QPushButton(Dialog)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setGeometry(QRect(290, 360, 93, 28))
        self.comboBox_0 = QComboBox(Dialog)
        self.comboBox_0.setObjectName(u"comboBox_0")
        self.comboBox_0.setGeometry(QRect(90, 30, 131, 22))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 55, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.textEdit_2.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.groupBox_1.setTitle(QCoreApplication.translate("Dialog", u"Operation", None))
        self.radioButton_2.setText("")
        self.radioButton_1.setText("")
        self.textEdit_1.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Clear", None))
        self.pushButton_1.setText(QCoreApplication.translate("Dialog", u"Add condition", None))
        self.pushButton_accept.setText(QCoreApplication.translate("Dialog", u"Accept", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Group by:", None))
    # retranslateUi

