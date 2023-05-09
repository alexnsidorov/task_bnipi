# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\window\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from pyqtgraph import GraphicsView
from window.widgets import TBTableView 


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.table = TBTableView(self.splitter)
        self.table.setObjectName("table")
        self.graph = GraphicsView(self.splitter)
        self.graph.setObjectName("graph")
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setObjectName("save")
        self.horizontalLayout.addWidget(self.save)
        self.open = QtWidgets.QPushButton(self.centralwidget)
        self.open.setObjectName("open")
        self.horizontalLayout.addWidget(self.open)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Testing bnipi"))
        self.save.setText(_translate("MainWindow", "Save in file"))
        self.open.setText(_translate("MainWindow", "Open file"))
