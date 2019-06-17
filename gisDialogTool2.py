# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gisDialogTool2.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

import time
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import xlsDialog
from GISMmdOperation import mmd_gis_pose_extract, mmd_model_dict_extract


class Ui_Dialog(QMainWindow):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(791, 732)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.verticalLayout.addWidget(self.label_6)
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
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.modellineEdit = QtWidgets.QLineEdit(Dialog)
        self.modellineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.modellineEdit.setReadOnly(True)
        self.modellineEdit.setObjectName("modellineEdit")
        self.horizontalLayout_2.addWidget(self.modellineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.poselineEdit = QtWidgets.QLineEdit(Dialog)
        self.poselineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.poselineEdit.setObjectName("poselineEdit")
        self.horizontalLayout_5.addWidget(self.poselineEdit)
        self.poseBtn = QtWidgets.QPushButton(Dialog)
        self.poseBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.poseBtn.setObjectName("poseBtn")
        self.horizontalLayout_5.addWidget(self.poseBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.dictlineEdit = QtWidgets.QLineEdit(Dialog)
        self.dictlineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.dictlineEdit.setObjectName("dictlineEdit")
        self.horizontalLayout_6.addWidget(self.dictlineEdit)
        self.dictBtn = QtWidgets.QPushButton(Dialog)
        self.dictBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.dictBtn.setObjectName("dictBtn")
        self.horizontalLayout_6.addWidget(self.dictBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.poseRunBtn = QtWidgets.QPushButton(Dialog)
        self.poseRunBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.poseRunBtn.setObjectName("poseRunBtn")
        self.horizontalLayout_3.addWidget(self.poseRunBtn)
        self.dictRunBtn = QtWidgets.QPushButton(Dialog)
        self.dictRunBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.dictRunBtn.setObjectName("dictRunBtn")
        self.horizontalLayout_3.addWidget(self.dictRunBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.logText = QtWidgets.QTextBrowser(Dialog)
        self.logText.setObjectName("logText")
        self.logText.setStyleSheet("background-color: rgb(67, 67, 67);\n"
                                   "color: rgb(255, 255, 255);")
        self.verticalLayout.addWidget(self.logText)

        self.cb1Btn.clicked.connect(self.cb1_open_btn)
        self.poseBtn.clicked.connect(lambda: self.xls_save_btn(self.poseBtn))
        self.dictBtn.clicked.connect(lambda: self.xls_save_btn(self.dictBtn))
        self.poseRunBtn.clicked.connect(self.pose_info_extract)
        self.dictRunBtn.clicked.connect(self.dict_info_extract)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_6.setText(_translate("Dialog", "Momoda&GIS Points Pose Information Extract "))
        self.label_2.setText(_translate("Dialog", "Cb1 File"))
        self.cb1Btn.setText(_translate("Dialog", "Open"))
        self.label.setText(_translate("Dialog", "Model ID"))
        self.modellineEdit.setText(_translate("Dialog", "A9B2E15D940045119D68052BB4900E8A"))
        self.label_4.setText(_translate("Dialog", "Model Pose Xls"))
        self.poselineEdit.setToolTip(_translate("Dialog", "<html><head/><body><p>xlslineEdit</p></body></html>"))
        self.poseBtn.setText(_translate("Dialog", "Save"))
        self.label_5.setText(_translate("Dialog", "Model Dict Xls"))
        self.dictBtn.setText(_translate("Dialog", "Save"))
        self.poseRunBtn.setText(_translate("Dialog", "Model Pose Extract"))
        self.dictRunBtn.setText(_translate("Dialog", "Model Dict Info Extract "))

    def cb1_open_btn(self):
        file_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1lineEdit.setText(str(file_name[0]))

    def xls_save_btn(self, btn):
        file_name, file_type = QFileDialog.getSaveFileName(self, "文件保存", '',
                                                           "All Files (*);;Excel Files (*.xls)")
        if btn == self.poseBtn:
            self.poselineEdit.setText(file_name)
        elif btn == self.dictBtn:
            self.dictlineEdit.setText(file_name)

    def pose_info_extract(self):
        try:
            self.logText.append('Running:\n')
            _model_id = self.modellineEdit.text()
            _cb1_file = self.cb1lineEdit.text()
            _pose_xls = self.poselineEdit.text()
            self.logText.append(
                '{0}\n{1}\n{2}\n'.format(_model_id, _cb1_file, _pose_xls))
            time.sleep(2)
            mmd_gis_pose_extract(_cb1_file, _model_id, _pose_xls)
            self.logText.append('Success: '"<font color = green>{}</font> \n".format('Pose info extract'))
        except:
            self.logText.append('Error: '"<font color = red>{}</font> \n".format(traceback.format_exc()))

    def dict_info_extract(self):
        try:
            self.logText.append('Running:\n')
            # _model_id = self.modellineEdit.text()
            _cb1_file = self.cb1lineEdit.text()
            _dict_xls = self.dictlineEdit.text()
            self.logText.append(
                '{0}\n{1}\n'.format(_cb1_file, _dict_xls))
            time.sleep(2)
            mmd_model_dict_extract(_cb1_file, _dict_xls)
            self.logText.append('Success: '"<font color = green>{}</font> \n".format('plcs model dict info extract'))
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
