# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xls_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QMainWindow, QTableWidget, QFileDialog, QTableWidgetItem
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import numpy as np


class XlsDialog(QMainWindow):
    modelTextSignal = pyqtSignal(str)
    fieldTitleSignal = pyqtSignal(str)
    __text = []

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(930, 784)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(750, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.pushButton.clicked.connect(self.creat_table_show)
        self.tableWidget.itemClicked.connect(self.field_value)
        self.pushButton_2.clicked.connect(self.data_search_btn1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Xls File Open"))
        self.pushButton_2.setText(_translate("Dialog", "Search"))

    def openfile(self):

        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        self.modelTextSignal.emit(openfile_name[0])
        return openfile_name[0]

    def creat_table_show(self):
        self.__text = []
        xls_path = self.openfile()
        if len(xls_path) > 0:
            input_table = pd.read_excel(xls_path)
            # print(input_table)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            print(input_table_rows)
            print(input_table_colunms)
            input_table_header = input_table.columns.values.tolist()
            # print(input_table_header)

            self.tableWidget.setColumnCount(input_table_colunms)
            self.tableWidget.setRowCount(input_table_rows)
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)

            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                # print(input_table_rows_values)
                input_table_rows_values_array = np.array(input_table_rows_values)
                # print(input_table_rows_values_array)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                # print(input_table_rows_values_list)
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
                    # print(input_table_items_list)
                    # print(type(input_table_items_list))
                    input_table_items = str(input_table_items_list)
                    if input_table_items != 'nan':
                        new_item = QTableWidgetItem(input_table_items)
                        new_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.tableWidget.setItem(i, j, new_item)
            # else:
            #     self.centralWidget.show()

    def data_search_btn1(self):
        items = self.tableWidget.findItems(self.lineEdit.text(), QtCore.Qt.MatchContains)
        for item in items:
            item.setSelected(True)
            # 设置单元格的背脊颜色为红
            item.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            self.tableWidget.verticalScrollBar().setSliderPosition(item.row())
            # self.pushButton_2.autoRepeat()

    def field_value(self):
        _title = self.tableWidget.horizontalHeaderItem(self.tableWidget.currentColumn()).text()
        if _title == 'model_id':
            _content = self.tableWidget.currentItem().text()
            print(_content)
            self.modelTextSignal.emit(_content)
        elif _title not in self.__text:
            self.__text.append(_title)
            print(self.__text)
            self.fieldTitleSignal.emit(str(self.__text))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = XlsDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
