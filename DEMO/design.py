# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("Stegano"))
        MainWindow.resize(290, 271)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 291, 271))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.pushButton_2 = QtGui.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 210, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(10, 60, 161, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.btnBrowse = QtGui.QPushButton(self.tab)
        self.btnBrowse.setGeometry(QtCore.QRect(10, 20, 161, 31))
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.radioButton = QtGui.QRadioButton(self.tab)
        self.radioButton.setGeometry(QtCore.QRect(10, 110, 111, 17))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        # self.radioButton_2 = QtGui.QRadioButton(self.tab)
        # self.radioButton_2.setGeometry(QtCore.QRect(10, 130, 131, 17))
        # self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        # self.radioButton_4 = QtGui.QRadioButton(self.tab)
        # self.radioButton_4.setGeometry(QtCore.QRect(10, 150, 211, 17))
        # self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        # self.lineEdit = QtGui.QLineEdit(self.tab)
        # self.lineEdit.setGeometry(QtCore.QRect(200, 150, 41, 20))
        # self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        # self.tab_2 = QtGui.QWidget()
        # # self.tab_2.setObjectName(_fromUtf8("tab_2"))
        # self.pushButton_3 = QtGui.QPushButton(self.tab_2)
        # self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 161, 31))
        # self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        # self.pushButton_4 = QtGui.QPushButton(self.tab_2)
        # self.pushButton_4.setGeometry(QtCore.QRect(200, 210, 75, 23))
        # self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        # self.radioButton_5 = QtGui.QRadioButton(self.tab_2)
        # self.radioButton_5.setGeometry(QtCore.QRect(10, 70, 121, 17))
        # self.radioButton_5.setObjectName(_fromUtf8("radioButton_5"))
        # self.radioButton_6 = QtGui.QRadioButton(self.tab_2)
        # self.radioButton_6.setGeometry(QtCore.QRect(10, 90, 131, 17))
        # self.radioButton_6.setObjectName(_fromUtf8("radioButton_6"))
        # self.radioButton_8 = QtGui.QRadioButton(self.tab_2)
        # self.radioButton_8.setGeometry(QtCore.QRect(10, 110, 201, 17))
        # self.radioButton_8.setObjectName(_fromUtf8("radioButton_8"))
        # self.lineEdit_2 = QtGui.QLineEdit(self.tab_2)
        # self.lineEdit_2.setGeometry(QtCore.QRect(200, 110, 41, 20))
        # self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        # self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Stegano", "Stegano", None))
        self.pushButton_2.setText(_translate("Stegano", "Koduj", None))
        self.pushButton.setText(_translate("Stegano", "Wybierz plik tekstowy", None))
        self.btnBrowse.setText(_translate("Stegano", "Wybierz plik multimedialny", None))
        self.radioButton.setText(_translate("Stegano", "Tryb standardowy", None))
        # self.radioButton_2.setText(_translate("Stegano", "Tryb deterministyczny", None))
        # self.radioButton_4.setText(_translate("Stegano", "Tryb niedeterministyczny z ziarnem:", None))
        # self.lineEdit.setText(_translate("Stegano", "15", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Koder", None))
        # self.pushButton_3.setText(_translate("Stegano", "Wybierz plik multimedialny", None))
        # self.pushButton_4.setText(_translate("Stegano", "Dekoduj", None))
        # self.radioButton_5.setText(_translate("Stegano", "Tryb standardowy", None))
        # self.radioButton_6.setText(_translate("Stegano", "Tryb deterministyczny", None))
        # self.radioButton_8.setText(_translate("Stegano", "Tryb niedeterministyczny z ziarnem:", None))
        # self.lineEdit_2.setText(_translate("Stegano", "15", None))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Stegano", "Dekoder", None))

