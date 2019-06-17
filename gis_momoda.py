# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gis_momoda.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

import gisMomoda_rc
from PyQt5 import QtCore, QtGui, QtWidgets
import gisDialogTool2
import gisDialogTool3


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(537, 515)
        MainWindow.setStyleSheet("background-color: rgb(10, 69, 107);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("background-image: url(:/background_image/gisImage.png);\n"
                                      "background-repeat: no-repeat;\n"
                                      "background-attachment: fixed;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "")
        self.titleLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.titleLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.titleLabel.setTextFormat(QtCore.Qt.AutoText)
        self.titleLabel.setScaledContents(False)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(False)
        self.titleLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(19, 103, 109);\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(23, 127, 134);\n"
                                        "color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(25, 124, 112);")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-color: rgb(35, 156, 138);")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("background-color: rgb(37, 181, 157);")
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.jump_dialog_btn1)
        self.pushButton_2.clicked.connect(self.jump_dialog_btn2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GIS&Momoda Tools"))
        self.titleLabel.setText(_translate("MainWindow", "GIS Momoda Model Insert Tools"))
        self.pushButton.setText(_translate("MainWindow", "Pose Information extract"))
        self.pushButton_2.setText(_translate("MainWindow", "GIS Model Insert"))

    def jump_dialog_btn1(self):
        # self.hide()
        _temp_dialog = QtWidgets.QDialog()
        _ui = gisDialogTool2.Ui_Dialog()
        _ui.setupUi(_temp_dialog)
        _temp_dialog.show()
        self.pushButton.setEnabled(False)  # 锁定按钮
        _temp_dialog.exec_()
        self.pushButton.setEnabled(True)  # 释放按钮
        # self.show()

    def jump_dialog_btn2(self):
        # self.hide()
        _temp_dialog = QtWidgets.QDialog()
        _ui = gisDialogTool3.Ui_Dialog()
        _ui.setupUi(_temp_dialog)
        _temp_dialog.show()
        self.pushButton_2.setEnabled(False)  # 锁定按钮
        _temp_dialog.exec_()
        self.pushButton_2.setEnabled(True)  # 释放按钮
        # self.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
