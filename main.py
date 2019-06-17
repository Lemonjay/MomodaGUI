import sys
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from qtUi import Ui_MainWindow
from BasemapOperation import base_map_add
from AttributeOperation import attribute_statistic, attribute_add_indoor, attribute_add_outdoor, \
    model_attribute_extract, model_attribute_add
from PackageOperation import cb1_version_publish
from SceneOperation import building_floor_merge, model_id_recoding
from ModelOperation import cb1_model_replace, cb1_model_height_modify
import xlsDialog


class Main(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.resize(897, 743)
        self.resize(500, 600)
        self.setupUi(self)
        # self.retranslateUi(self)

    def setup_ui(self):
        pass

    # <editor-fold desc="Tool 1 Button Function">
    def cb1_open(self):
        # file_name = QFileDialog.getOpenFileName(self, '选择文件', '', '{0} files(*.{0})'.format(_file_extension))
        file_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1lineEdit.setText(file_name[0])
        # self.cb1lineEdit_2.setText(file_name[0])

    def pic_open(self):
        # file_name = QFileDialog.getOpenFileName(self, '选择文件', '', '{0} files(*.{0})'.format(_file_extension))
        file_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'BaseMap files(*.jpg , *.png)')
        print(file_name[0])
        self.bmlineEdit.setText(file_name[0])

    def folder_open(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.umlineEdit.setText(directory)

    def exe_run(self):
        self.logtextEdit.append('Log writing......')
        try:
            cb1_path = self.cb1lineEdit.text()
            floor = self.floorlineEdit.text()
            bm_path = self.bmlineEdit.text()
            user_path = self.umlineEdit.text()
            indoor_delete = self.checkBox.isChecked()
            print(indoor_delete)
            self.logtextEdit.append(
                '{0}\n{1}\n{2}\n{3}\nIndoor Features Delete: {4}\n'.format(cb1_path, bm_path, floor, user_path,
                                                                           indoor_delete))
            base_map_add(cb1_path, floor, bm_path, user_path, indoor_delete)
            self.logtextEdit.append('Running successed')
        except:
            self.logtextEdit.append('Error: '
                                    "<font color = red>{}</font> \n".format(traceback.format_exc()))

    # </editor-fold>

    # <editor-fold desc="Tool 2 Button Function">

    def cb1_open_method2(self):
        # file_name = QFileDialog.getOpenFileName(self, '选择文件', '', '{0} files(*.{0})'.format(_file_extension))
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1lineEdit_2.setText(str(file_name[0]))

    def xls_open(self):
        file_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xls , *.xlsx)')
        return file_name[0]

    def blib_button(self):
        self.bLiblineEdit.setText(self.xls_open())

    def ulib_button(self):
        self.uLiblineEdit.setText(self.xls_open())

    def attribute_statistic_button(self):
        try:
            cb1_files = eval(self.cb1lineEdit_2.text())
            self.logtextEdit_2.append(
                '{0}\n{1}\n{2}\n'.format(self.cb1lineEdit_2.text(), self.bLiblineEdit.text(), self.uLiblineEdit.text()))
            blib_xls = self.bLiblineEdit.text()
            ulib_xls = self.uLiblineEdit.text()
            attribute_statistic(cb1_files, blib_xls, ulib_xls)
            self.logtextEdit_2.append('Success: The Attributes was added in UserLib.xls')
        except:
            self.logtextEdit_2.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))

    def result_folder_button(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.mrFolderlineEdit.setText(directory)

    def attribute_add_button(self):
        try:
            cb1_files = eval(self.cb1lineEdit_2.text())
            blib_xls = self.bLiblineEdit.text()
            ulib_xls = self.uLiblineEdit.text()
            field = self.fieldlineEdit.text()
            result_folder = self.mrFolderlineEdit.text()
            self.logtextEdit_2.append(
                '{0}\n{1}\n{2}\n{3}\n{4}\n'.format(self.cb1lineEdit_2.text(), blib_xls,
                                                   ulib_xls, field, result_folder))
            if self.outdoorCheckBox02.isChecked():
                attribute_add_outdoor(cb1_files, field, blib_xls, ulib_xls, result_folder)
            else:
                attribute_add_indoor(cb1_files, field, blib_xls, ulib_xls, result_folder)

            self.logtextEdit_2.append('Success: The Attributes was added.')
        except:
            self.logtextEdit_2.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))  # 某一行字体加颜色

    # </editor-fold>

    # <editor-fold desc="Tool 3 Button Function">
    def cb1_open_btn3(self):
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'Cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1FilelineEdit_3.setText(str(file_name[0]))

    def cb1_save_btn3(self):
        file_name, file_type = QFileDialog.getSaveFileName(self, "文件保存", '', "All Files (*);;Cb1 Files (*.cb1)")
        # print(file_name)
        self.cb1SavelineEdit.setText(file_name)

    def floor_merge_btn(self):
        try:
            cb1_files = eval(self.cb1FilelineEdit_3.text())
            cb1_path_save = self.cb1SavelineEdit.text()
            coding_abbre = self.bNameCodelineEdit.text()
            self.logtextEdit_3.append('{0}\n{1}\n'.format(cb1_files, cb1_path_save))
            # floor_two_merge(cb1_files[0], cb1_files[1])
            building_floor_merge(cb1_files, cb1_path_save, coding_abbre)
            self.logtextEdit_3.append('Success: Floor Merging ')
        except:
            self.logtextEdit_3.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))

    # </editor-fold>

    # <editor-fold desc="Tool 4 Button Function">
    def cb1_open_btn4(self):
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1FilelineEdit_4.setText(str(file_name[0]))

    def folder_open_btn4(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.rFolderlineEdit_4.setText(directory)

    def id_recoding_btn4(self):
        try:
            cb1_files = eval(self.cb1FilelineEdit_4.text())
            building_name_code = self.bNameCodelineEdit_2.text()
            folder = self.rFolderlineEdit_4.text()
            self.logtextEdit_4.append('{0}\n{1}\n{2}\n'.format(cb1_files, building_name_code, folder))
            model_id_recoding(cb1_files, building_name_code, folder)
            self.logtextEdit_4.append('Success: Model Recoding ')
        except:
            self.logtextEdit_4.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))

    # </editor-fold>

    # <editor-fold desc="Tool 5 Button Function">
    def cb1_open_btn5(self):
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1FilelineEdit_5.setText(str(file_name[0]))

    def cus_cb1_open_btn5(self):
        # file_name = QFileDialog.getOpenFileName(self, '选择文件', '', '{0} files(*.{0})'.format(_file_extension))
        file_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cusCb1lineEdit_5.setText(file_name[0])

    def ulib_btn5(self):
        self.uLiblineEdit_5.setText(self.xls_open())

    def folder_open_btn5(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.rFolderlineEdit_5.setText(directory)

    def custom_model_replace_btn5(self):
        try:
            cb1_files = eval(self.cb1FilelineEdit_5.text())
            model_mmd = self.modelMmdlineEdit.text()
            model_custom = self.cusModellineEdit.text()
            cb1_custom = self.cusCb1lineEdit_5.text()
            user_xls = self.uLiblineEdit_5.text()
            folder = self.rFolderlineEdit_5.text()
            self.logtextEdit_5.append(
                '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n'.format(cb1_files, model_mmd, model_custom, cb1_custom, user_xls,
                                                        folder))
            for fl in cb1_files:
                cb1_model_replace(model_mmd, fl, model_custom, cb1_custom, user_xls, 'UserLib', folder)
                self.logtextEdit_5.append('Done: {}'.format(fl))
            self.logtextEdit_5.append('Success: Model Replacing ')
        except:
            self.logtextEdit_5.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))

    # </editor-fold>

    # <editor-fold desc="Tool 6 Button Function">
    def cb1_open_btn6(self):
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1FilelineEdit_6.setText(str(file_name[0]))

    def folder_open_btn6(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.rFolderlineEdit_6.setText(directory)

    def version_run_btn6(self):
        try:
            cb1_files = eval(self.cb1FilelineEdit_6.text())
            building_name = self.bNamelineEdit_6.text()
            version = self.versionlineEdit_6.text()
            folder = self.rFolderlineEdit_6.text()
            self.logtextEdit_6.append(
                '{0}\n{1}\n{2}\n'.format(cb1_files, building_name, version, folder))
            cb1_version_publish(cb1_files, building_name, version, folder)
            self.logtextEdit_6.append('Success: Model Rename')
        except:
            self.logtextEdit_6.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))

    # </editor-fold>

    # <editor-fold desc="Tool 7 Button Function">
    def jump_dialog_btn7(self):
        # self.hide()
        _temp_dialog = QtWidgets.QDialog()
        _ui = xlsDialog.XlsDialog()
        _ui.setupUi(_temp_dialog)
        _temp_dialog.show()
        _ui.modelTextSignal.connect(self.get_dialog_signal)
        self.modelBtn_7.setEnabled(False)  # 锁定按钮
        _temp_dialog.exec_()
        self.modelBtn_7.setEnabled(True)  # 释放按钮
        # self.show()

    def get_dialog_signal(self, _connect):
        self.modelLineEdit_7.setText(_connect.replace("'", ""))

    def cb1_open_btn7(self):
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1FilelineEdit_7.setText(str(file_name[0]))

    def folder_open_btn7(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.rFolderlineEdit_7.setText(directory)

    def model_shape_btn7(self):
        try:
            model_id = self.modelLineEdit_7.text()
            cb1_files = eval(self.cb1FilelineEdit_7.text())
            _pose_h = self.hPoselineEdit_7.text()
            _scale_h = self.hScalelineEdit_7.text()
            folder = self.rFolderlineEdit_7.text()
            self.logtextEdit_7.append(
                '{0}\n{1}\n{2}\n{3}\n{4}\n'.format(model_id, cb1_files, _pose_h, _scale_h, folder))
            cb1_model_height_modify(model_id, cb1_files, _pose_h, _scale_h, folder)
            self.logtextEdit_7.append('Success: Model Height Modify')
        except:
            self.logtextEdit_7.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))

    # </editor-fold>

    # <editor-fold desc="Tool 8 Button Function">
    def cb1_open_btn8(self):
        file_name = QFileDialog.getOpenFileNames(self, '选择文件', '', 'cb1 files(*.cb1)')
        print(file_name[0])
        self.cb1FilelineEdit_8.setText(str(file_name[0]))

    def folder_open_btn8(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(type(directory))
        self.rFolderlineEdit_8.setText(directory)

    def xls_save_btn8(self, btn):
        file_name, file_type = QFileDialog.getSaveFileName(self, "文件保存", '',
                                                           "All Files (*);;Excel Files (*.xls)")
        self.xlsSaveLineEdit_8.setText(file_name)

    def jump_dialog_btn8(self):
        # self.hide()
        _temp_dialog = QtWidgets.QDialog()
        _ui = xlsDialog.XlsDialog()
        _ui.setupUi(_temp_dialog)
        _temp_dialog.show()
        _ui.modelTextSignal.connect(self.get_dialog_signal8)
        _ui.fieldTitleSignal.connect(self.get_field_title_signal8)
        self.modelBtn_8.setEnabled(False)  # 锁定按钮
        self.fieldBtn_8.setEnabled(False)
        _temp_dialog.exec_()
        self.modelBtn_8.setEnabled(True)  # 释放按钮
        self.fieldBtn_8.setEnabled(True)
        # self.show()

    def get_dialog_signal8(self, _connect):
        if '.xls' in _connect or '.xlsx' in _connect:
            pass
        else:
            self.modelLineEdit_8.setText(_connect.replace("'", ""))

    def get_field_title_signal8(self, _connect):
        self.fieldlineEdit_8.setText(_connect)

    def model_info_extract_btn8(self):
        try:
            model_id = self.modelLineEdit_8.text()
            cb1_files = eval(self.cb1FilelineEdit_8.text())
            xls_path = self.xlsSaveLineEdit_8.text()
            outdoor_bool = self.outdoorcheckBox_8.isChecked()
            self.logtextEdit_8.append(
                '{0}\n{1}\n{2}\n{3}\n'.format(model_id, cb1_files, xls_path, outdoor_bool))
            model_attribute_extract(cb1_files, model_id, xls_path, outdoor_bool)
            self.logtextEdit_8.append('Success: Model Information Extract')
        except:
            self.logtextEdit_8.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))

    def model_attributes_add_btn8(self):
        try:
            fields = eval(self.fieldlineEdit_8.text())
            cb1_files = eval(self.cb1FilelineEdit_8.text())
            xls_path = self.xlsSaveLineEdit_8.text()
            folder = self.rFolderlineEdit_8.text()
            outdoor_bool = self.outdoorcheckBox_8.isChecked()
            self.logtextEdit_8.append(
                '{0}\n{1}\n{2}\n{3}\n{4}\n'.format(fields, cb1_files, xls_path, folder, outdoor_bool))
            model_attribute_add(cb1_files, fields, xls_path, folder, outdoor_bool)
            self.logtextEdit_8.append('Success: Model Information add')
        except:
            self.logtextEdit_8.append('Error: '
                                      "<font color = red>{}</font> \n".format(traceback.format_exc()))
    # </editor-fold>


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
