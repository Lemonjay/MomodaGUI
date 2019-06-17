# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gisDialog01.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

import time
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import xlsDialog
from GISMmdOperation import gis_model_insert


class Ui_Dialog(QMainWindow):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(791, 732)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(80, 30))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cb1lineEdit = QtWidgets.QLineEdit(Dialog)
        self.cb1lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.cb1lineEdit.setObjectName("cb1lineEdit")
        self.horizontalLayout.addWidget(self.cb1lineEdit)
        self.cb1Btn = QtWidgets.QPushButton(Dialog)
        self.cb1Btn.setMinimumSize(QtCore.QSize(0, 30))
        self.cb1Btn.setObjectName("cb1Btn")
        self.horizontalLayout.addWidget(self.cb1Btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.modellineEdit = QtWidgets.QLineEdit(Dialog)
        self.modellineEdit.setMinimumSize(QtCore.QSize(600, 30))
        self.modellineEdit.setObjectName("modellineEdit")
        self.horizontalLayout_2.addWidget(self.modellineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(80, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.gislineEdit = QtWidgets.QLineEdit(Dialog)
        self.gislineEdit.setMinimumSize(QtCore.QSize(600, 30))
        self.gislineEdit.setObjectName("gislineEdit")
        self.horizontalLayout_3.addWidget(self.gislineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setMinimumSize(QtCore.QSize(80, 0))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_7.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.xlsBtn = QtWidgets.QPushButton(Dialog)
        self.xlsBtn.setMinimumSize(QtCore.QSize(0, 110))
        self.xlsBtn.setObjectName("xlsBtn")
        self.horizontalLayout_4.addWidget(self.xlsBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.liblineEdit = QtWidgets.QLineEdit(Dialog)
        self.liblineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.liblineEdit.setObjectName("liblineEdit")
        self.horizontalLayout_5.addWidget(self.liblineEdit)
        self.libBtn = QtWidgets.QPushButton(Dialog)
        self.libBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.libBtn.setObjectName("libBtn")
        self.horizontalLayout_5.addWidget(self.libBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.folderlineEdit = QtWidgets.QLineEdit(Dialog)
        self.folderlineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.folderlineEdit.setObjectName("folderlineEdit")
        self.horizontalLayout_6.addWidget(self.folderlineEdit)
        self.folderBtn = QtWidgets.QPushButton(Dialog)
        self.folderBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.folderBtn.setObjectName("folderBtn")
        self.horizontalLayout_6.addWidget(self.folderBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.insertModelBtn = QtWidgets.QPushButton(Dialog)
        self.insertModelBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.insertModelBtn.setObjectName("insertModelBtn")
        self.verticalLayout_2.addWidget(self.insertModelBtn)
        self.logText = QtWidgets.QTextBrowser(Dialog)
        self.logText.setObjectName("logText")
        self.logText.setStyleSheet("background-color: rgb(67, 67, 67);\n"
                                   "color: rgb(255, 255, 255);")
        self.verticalLayout_2.addWidget(self.logText)

        self.cb1Btn.clicked.connect(self.cb1_open_btn)
        self.xlsBtn.clicked.connect(self.jump_dialog_btn)
        self.libBtn.clicked.connect(self.lib_btn)
        self.folderBtn.clicked.connect(self.folder_open_btn)
        self.insertModelBtn.clicked.connect(self.insert_model_btn)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_6.setText(_translate("Dialog", "GIS Model Insert Tools"))
        self.label_2.setText(_translate("Dialog", "Cb1 Files"))
        self.cb1Btn.setText(_translate("Dialog", "Open"))
        self.label.setText(_translate("Dialog", "Model ID"))
        self.label_3.setText(_translate("Dialog", "GIS Model Xls"))
        self.label_7.setText(_translate("Dialog", "Field Lists"))
        self.xlsBtn.setText(_translate("Dialog", "Open"))
        self.label_4.setText(_translate("Dialog", "Lib Xls"))
        self.libBtn.setText(_translate("Dialog", "Open"))
        self.label_5.setText(_translate("Dialog", "Result Folder"))
        self.folderBtn.setText(_translate("Dialog", "Open"))
        self.insertModelBtn.setText(_translate("Dialog", "Run"))

    def cb1_open_btn(self):
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1lineEdit.setText(str(file_name[0]))

    def folder_open_btn(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.folderlineEdit.setText(directory)

    def jump_dialog_btn(self):
        # self.hide()
        _temp_dialog = QtWidgets.QDialog()
        _ui = xlsDialog.XlsDialog()
        _ui.setupUi(_temp_dialog)
        _temp_dialog.show()
        _ui.modelTextSignal.connect(self.get_dialog_signal)
        _ui.fieldTitleSignal.connect(self.get_field_title_signal)
        self.xlsBtn.setEnabled(False)  # 锁定按钮
        _temp_dialog.exec_()
        self.xlsBtn.setEnabled(True)  # 释放按钮
        # self.show()

    def get_dialog_signal(self, _connect):
        if '.xls' in _connect or '.xlsx' in _connect:
            self.gislineEdit.setText(_connect)
        else:
            self.modellineEdit.setText(_connect.replace("'", ""))

    def get_field_title_signal(self, _connect):
        self.lineEdit.setText(_connect)

    def lib_btn(self):
        self.liblineEdit.setText(self.xls_open())

    def xls_open(self):
        file_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'excel files(*.xls , *.xlsx)')
        return file_name[0]

    def insert_model_btn(self):
        try:
            self.logText.append('Running:\n')
            _model_id = self.modellineEdit.text()
            _cb1_files = eval(self.cb1lineEdit.text())
            _gis_xls = self.gislineEdit.text()
            _lib_xls = self.liblineEdit.text()
            _folder = self.folderlineEdit.text()
            _field_lists = [] if len(self.lineEdit.text()) == 0 else eval(self.lineEdit.text())
            self.logText.append(
                '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n'.format(_model_id, _cb1_files, _gis_xls, _lib_xls, _folder,
                                                        _field_lists))
            time.sleep(2)
            gis_model_insert(_model_id, _cb1_files, _gis_xls, _lib_xls, _field_lists, _folder)
            self.logText.append('Success: '"<font color = green>{}</font> \n".format('GIS Model Insert'))
        except:
            self.logText.append('Error: '"<font color = red>{}</font> \n".format(traceback.format_exc()))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
