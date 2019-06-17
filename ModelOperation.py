#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import xlrd
import xlwt
import os
import json
import shutil
import zipfile
from xlutils.copy import copy
from PackageOperation import Cb1OperationModify


def excel_create_write(_xls_path, _sheet_name, _info_lists, _xls_title):
    '''
      创建新的excel，写入新的信息，写入的方法增加行，通过key和title的匹配，在相应的title列中填入指定的值
      :param _xls_path:
      :param _sheet_name:
      :param _info_lists: 需要写入 excel 的信息 [{key01:value01,key02:value02,.....},{},......]
      :param _xls_title: excel 标题 [title01,title02,......]
      :return:
    '''
    _book = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    _sheet = _book.add_sheet(_sheet_name, True)  # 新建sheet
    for j in range(len(_xls_title)):
        _sheet.write(0, j, _xls_title[j])

    for i in range(len(_info_lists)):
        _dict = _info_lists[i]
        _list = list(_dict.keys())
        for j in range(len(_xls_title)):
            if _xls_title[j] in _list:
                _sheet.write(i + 1, j, _dict[_xls_title[j]])
    _book.save(_xls_path)


def excel_append_write(_xls_path, _sheet_name, _info_lists, _xls_title):
    '''
    对于已有的excel，需要附加写入新的信息，写入的方法增加行，通过key和title的匹配，在相应的title列中填入指定的值
    :param _xls_path:
    :param _sheet_name:
    :param _info_lists: 需要写入 excel 的信息 [{key01:value01,key02:value02,.....},{},......]
    :param _xls_title: excel 标题 [title01,title02,......]
    :return:
    '''
    _book = xlrd.open_workbook(_xls_path)
    _sheet = _book.sheet_by_name(_sheet_name)
    _rows_old = _sheet.nrows  # 获取表格中已存在的数据的行数
    _new_book = copy(_book)  # 将xlrd对象拷贝转化为xlwt对象
    _new_sheet = _new_book.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(len(_info_lists)):
        _dict = _info_lists[i]
        _list = list(_dict.keys())
        # print(_list)
        for j in range(len(_xls_title)):
            if _xls_title[j] in _list:
                _new_sheet.write(i + _rows_old, j, _dict[_xls_title[j]])
    _new_book.save(_xls_path)


def excel2dict(_xls_path, _sheet_name, _target_field_title):
    '''
    为了方便操作，对于数据小的excel 进行一次性数据提取，提取成dict，
    然后对提取时的dict进行操作，为什么提取成dict，因为提取成dict，
    对应的excel首行标题和每一行的值相对应{model_id:{key01:value01,key02:value02,..,}}
    :param _xls_path:
    :param _sheet_name:
    :param _target_field_title:
    :return: 字典
    '''
    _temp_lists = []  # 保存从excel表中读取出来的值，每一行为一个list，_temp_lists中保存了所有行的内容
    _result_lists = []  # 是由dict组成的list，是将_temp_lists中的内容全部转成字典组成的list：result
    _mmd_dict = {}  # 创建以model id 为 key 的dict

    _xls = xlrd.open_workbook(_xls_path)
    _table = _xls.sheet_by_name(_sheet_name)
    for i in range(0, _table.nrows):
        row_values = _table.row_values(i)
        # id 项取整
        _id = row_values[0]
        row_values[0] = int(_id) if _id != 'id' else _id  # 默认第一列的title是‘id’
        # model_id 项去除单引号
        _model_id = row_values[1]
        row_values[1] = _model_id.replace("'", "")
        _temp_lists.append(row_values)
        # print(row_values)
    # 将list转化成dict
    for i in range(1, len(_temp_lists)):
        _temp_dict = dict(zip(_temp_lists[0], _temp_lists[i]))
        _result_lists.append(_temp_dict)
    # 生成以model_id为key的dict
    for _dict in _result_lists:
        _mmd_dict.update({_dict[_target_field_title]: _dict})
    # self._user_list = _result_lists
    return _mmd_dict


def field_value_got(_model_id, _field, _xls_path, _sheet_name, _target_field_title='model_id'):
    '''
    通过model id 获取指定的字段值，_bidx 等等
    :param _model_id:
    :param _field: 字段名
    :param _xls_path:
    :param _sheet_name:
    :param _target_field_title:
    :return:
    '''
    _model_dict = excel2dict(_xls_path, _sheet_name, _target_field_title)
    if _model_id in list(_model_dict.keys()):
        _temp_dict = _model_dict[_model_id]
        if _field in list(_temp_dict.keys()):
            return _temp_dict[_field]


class ModelClassify(object):
    mmd_target_dict = {}  # 创建以bidx的序号为key的dict - 模型库
    _user_list = []
    _user_dict = {}  # 创建以model_id为key的dict - 自定义模型库

    # _user_target_dict = {}  # 创建以bidx的序号为key的dict - 自定义模型库

    def __init__(self, _bid_list=None):
        self._list = _bid_list

    def excel2dict(self, _xls_path, _sheet_name):
        '''
        为了方便操作，对于数据小的excel 进行一次性数据提取，提取成dict，
        然后对提取时的dict进行操作，为什么提取成dict，因为提取成dict，
        对应的excel首行标题和每一行的值相对应{model_id:{key01:value01,key02:value02,..,}}
        :param _xls_path:
        :param _sheet_name:
        :return: 字典
        '''
        _temp_lists = []  # 保存从excel表中读取出来的值，每一行为一个list，_temp_lists中保存了所有行的内容
        _result_lists = []  # 是由dict组成的list，是将_temp_lists中的内容全部转成字典组成的list：result
        _mmd_dict = {}  # 创建以model id 为 key 的dict

        _xls = xlrd.open_workbook(_xls_path)
        _table = _xls.sheet_by_name(_sheet_name)
        for i in range(0, _table.nrows):
            row_values = _table.row_values(i)
            # id 项取整
            _id = row_values[0]
            row_values[0] = int(_id) if _id != 'id' else _id
            # model_id 项去除单引号
            _model_id = row_values[1]
            row_values[1] = _model_id.replace("'", "")
            _temp_lists.append(row_values)
            # print(row_values)
        # 将list转化成dict
        for i in range(1, len(_temp_lists)):
            _temp_dict = dict(zip(_temp_lists[0], _temp_lists[i]))
            _result_lists.append(_temp_dict)
        # 生成以model_id为key的dict
        for _dict in _result_lists:
            _mmd_dict.update({_dict['model_id']: _dict})
        # self._user_list = _result_lists
        return _mmd_dict

    def got_user_dict(self, _xls_path, _sheet_name):
        _model_dict = self.excel2dict(_xls_path, _sheet_name)
        for i in range(len(self._list)):
            _model_id = self._list[i][0]
            if _model_id not in list(_model_dict.keys()):
                _model_title = self._list[i][2]
                _model_type = self._list[i][4]
                _model_info = str(self._list[i])
                # _temp_dict.update({'id': str(i)})
                _info = {'id': str(i), 'model_id': '{}'.format(_model_id), 'model_title': _model_title,
                         'model_type': _model_type, 'model_info': _model_info}
                self._user_list.append(_info)
                self._user_dict.update({_model_id: _info})
            # else:
            #     self._mmd_target_dict.update({str(i): _model_dict[_model_dict]})

    def dict2excel(self, _xls_user_path, _sheet_name='UserLib'):
        _xls_path = _xls_user_path
        _xls_title = ['id', 'model_id', 'model_title', 'model_type', 'mmd_type2nd', 'mmd_type1st',
                      'userid_prefix', 'type_name', 'TYPE', 'type_eng', 'model_info']
        if not os.path.exists(_xls_path):
            excel_create_write(_xls_path, _sheet_name, self._user_list, _xls_title)
        else:
            _dict_old = self.excel2dict(_xls_path, _sheet_name)
            for _mid in list(self._user_dict.keys()):
                if _mid in list(_dict_old.keys()):
                    self._user_dict.pop(_mid)
            _temp_lists = list(self._user_dict.values())
            print(_temp_lists)
            excel_append_write(_xls_path, _sheet_name, _temp_lists, _xls_title)

    def user_target_dict(self, _xls_path, _sheet_name, _xls_user_path, _sheet_user_name):
        '''
        每一个模模搭的cb1文件，都有一个对应 bIDList，根据bIDList生成一个以model id 为key的字典，
        通过对应的字典，给模型添加属性。
        :param _xls_path: 模模搭的模型库BundleLib.xls
        :param _sheet_name:
        :param _xls_user_path: 用户自定义的模型库UserLib.xls
        :param _sheet_user_name:
        :return:
        '''
        _model_dict = self.excel2dict(_xls_path, _sheet_name)
        if os.path.exists(_xls_user_path):
            _model_dict.update(self.excel2dict(_xls_user_path, _sheet_user_name))

        for i in range(len(self._list)):
            _model_id = self._list[i][0]
            _model_title = self._list[i][2]
            if _model_id in list(_model_dict.keys()):
                self.mmd_target_dict.update({str(i): _model_dict[_model_id]})
            else:
                print('{} was not existed'.format(_model_title))

    def field_value_got(self, _model_id, _field, _xls_path, _sheet_name):
        '''
        通过model id 获取指定的字段值，_bidx 等等
        :param _model_id:
        :param _field: 字段名
        :param _xls_path:
        :param _sheet_name:
        :return:
        '''
        _model_dict = self.excel2dict(_xls_path, _sheet_name)
        if _model_id in list(_model_dict.keys()):
            _temp_dict = _model_dict[_model_id]
            if _field in list(_temp_dict.keys()):
                return _temp_dict[_field]


class ModelReplacement(object):
    '''
    因为需求，需要将官方模型库的指定模型替换成自定义模型：
    1）需要3dmax，制作自定义模型，要求需要和官方模型的默认大小，方向一致
    2）用模模搭，搭建室内辅助场景，model_scene；
    3) 替换修改目标场景中的‘bIdLists’项，添加CustomModel 文件夹
    '''

    # js_plans = {}
    # _bid_list_dict = {}
    # js_dict = {}

    # 对于只有一个室内建筑场景
    def __init__(self, _json_scene):
        self.js_dict = {}
        self._json_folder = os.path.split(_json_scene)[0]
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            # self.js_bds = self.js_dict['objects']['0']['bds']
            # self.js_plan = self.js_dict['objects']['0']['plan']  # 室外场景plan
            # if len(list(self.js_bds.keys())) == 1:  # 判断bds项是否只有一项
            #     print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
            #     self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']  # 室内场景plans
            pass

    def bidlist_replace(self, _model_old_id, _model_target_id, _xls_path, _sheet_name):
        '''
        根据模型的id，从excel中调取指定的'model_info'模型信息，添加到bIdList中
        :param _model_old_id: 需要被替换的模型的id
        :param _model_target_id: 目标模型，大小，和默认方向与需要被替换的模型完全一致
        :param _xls_path: 导入的数据库，UserLib.xls 或者 19294BundleLib.xlsx
        :param _sheet_name:
        :return:
        '''
        _bool = False
        _temp_list = eval(field_value_got(_model_target_id, 'model_info', _xls_path,
                                          _sheet_name))  # 将字符串'[value,value,.....]'转换成 list，dict也可以用
        _list = self.js_dict['bIdList']
        for i in range(len(_list)):
            if _model_old_id == _list[i][0]:
                self.js_dict['bIdList'][i] = _temp_list
                _bool = True
                break
        return _bool

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


class ModelShapeOperation(object):
    '''
    # 1.因为缩放和共面问题，需要修改插入物体高度和垂直位置，调整起来比较麻烦；
    # 2.平面位置不好修改，目前可以修改的两个参数：pos (位置)悬空位置数据，相对于楼层的位置；
    # 3.scl（比例，高度）相对于原插入物体的比例而言
    '''

    # js_plans = {}
    # bidx_dict = {}

    # 对于只有一个室内建筑场景
    def __init__(self, _json_scene):
        self.js_plans = {}
        self.bidx_dict = {}
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            self.js_bds = self.js_dict['objects']['0']['bds']
            if len(list(self.js_bds.keys())) == 1:  # 判断bds项是否只有一项
                print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']

    def bidlist_dict_create(self):
        '''
        根据bIdList中的模型插入的顺序，生成以模型id 为key，序号为value
        :return:
        '''
        js_bidx = self.js_dict['bIdList']
        for i in range(len(js_bidx)):
            self.bidx_dict.update({str(i): js_bidx[i][0]})
        print('bIdList value dict: {}'.format(self.bidx_dict))

    def _model_bidx_got(self, _model_id):
        '''
        :param _model_id: 模模搭中的模型ID
        :return: 模模搭bIDList 模型矩阵中的排序的序号
        '''
        _temp_dict = dict(zip(self.bidx_dict.values(), self.bidx_dict.keys()))
        return _temp_dict[_model_id]

    def model_info_return(self, _model_id):
        js_bidx = self.js_dict['bIdList']
        for i in range(len(js_bidx)):
            if _model_id == js_bidx[i][0]:
                print(js_bidx[i][0])
                return str(js_bidx[i][0])

    def _model_height_modify(self, _insert_model_dict, _pose_h_value, _scale_h_value):
        '''
        模型位置和大小，自定义函数
        :param _insert_model_dict: 插入模型在plcs项中的dict
        :param _pose_h_value: 模型高度位置修改
        :param _scale_h_value: 模型高度比例修改
        :return:
        '''
        # 插入模型悬空高度修改
        if _pose_h_value:
            _pos_value = '{0} {1} {2}'.format(_insert_model_dict['pos'].split(' ')[0],
                                              _pose_h_value,
                                              _insert_model_dict['pos'].split(' ')[2])
            _insert_model_dict['pos'] = _pos_value
            print(_insert_model_dict['pos'])

        # 插入模型高度缩放比例修改
        if _scale_h_value:
            if _scale_h_value == '1':
                if 'scl' in list(_insert_model_dict.keys()):
                    _scl_value = '{0} {1} {2}'.format(_insert_model_dict['scl'].split(' ')[0],
                                                      _scale_h_value,
                                                      _insert_model_dict['scl'].split(' ')[2])
                    _insert_model_dict['scl'] = _scl_value
                    print(_insert_model_dict['scl'])
            else:
                if 'scl' in list(_insert_model_dict.keys()):
                    _scl_value = '{0} {1} {2}'.format(_insert_model_dict['scl'].split(' ')[0],
                                                      _scale_h_value,
                                                      _insert_model_dict['scl'].split(' ')[2])
                    _insert_model_dict['scl'] = _scl_value
                else:
                    _insert_model_dict.update({'scl': '1.000 {} 1.000'.format(_scale_h_value)})

    def pose_modify(self, _model_id, _pose_h_value=None, _scale_h_value=None):
        '''
        高度和位置修改
        :param _model_id: 模型的id
        :param _pose_h_value: 模型高度位置修改
        :param _scale_h_value: 模型高度比例修改
        :return:
        '''
        print('The insert model of plcs attribute modify')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            # _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if 'clds' not in list(js_num_plcs.keys()):
                    _bidx = str(js_num_plcs['bIdx'])
                    if self._model_bidx_got(_model_id) == _bidx:
                        self._model_height_modify(js_num_plcs, _pose_h_value, _scale_h_value)
                else:
                    js_clds = js_num_plcs['clds']
                    for ncls in list(js_clds.keys()):
                        js_num_clds = js_clds[ncls]
                        _bidx = str(js_num_clds['bIdx'])
                        if self._model_bidx_got(_model_id) == _bidx:
                            self._model_height_modify(js_num_clds, _pose_h_value, _scale_h_value)

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


def cb1_model_replace(_model_mmd_id, _cb1_main, _custom_model_id, _custom_model_scene, _xls_path, _sheet_name, _folder):
    '''
    模型替换，不一定是自定义模型替换官方模型，也可能是自定义模型之间的替换
    :param _model_mmd_id:
    :param _custom_model_id:
    :param _cb1_main:
    :param _custom_model_scene:
    :param _xls_path:
    :param _sheet_name:
    :param _folder:
    :return:
    '''
    cm = Cb1OperationModify(_cb1_main)
    cm_folder = cm.cb1_extract()
    js_path = cm.json_extract()
    cm_mr = ModelReplacement(js_path)
    replace_bool = cm_mr.bidlist_replace(_model_mmd_id, _custom_model_id, _xls_path, _sheet_name)
    cm_mr.json_scene_save()

    if replace_bool:
        cm_model_folder = os.path.join(cm_folder, 'CustomModel')

        if not os.path.exists(cm_model_folder):
            os.mkdir(cm_model_folder)

        cms = Cb1OperationModify(_custom_model_scene)
        cms_folder = cms.cb1_extract()

        cms_model_folder = os.path.join(cms_folder, 'CustomModel')
        if os.path.exists(cms_model_folder):
            _folder_lists = os.listdir(cms_model_folder)
            print(_folder_lists)
            if _custom_model_id in _folder_lists and not os.path.exists(
                    os.path.join(cm_model_folder, _custom_model_id)):
                shutil.copytree(os.path.join(cms_model_folder, _custom_model_id),
                                os.path.join(cm_model_folder, _custom_model_id))
        # 删除原有的自定义模型
        # print(os.path.exists(os.path.join(cm_model_folder, _model_mmd_id)))
        if os.path.exists(os.path.join(cm_model_folder, _model_mmd_id)):
            shutil.rmtree(os.path.join(cm_model_folder, _model_mmd_id))

    cm.cb1_create(_cb1_folder=_folder)


def cb1_model_height_modify(_model_id, _cb1_files, _pose_height, _pose_scale, _folder):
    for fl in _cb1_files:
        com = Cb1OperationModify(fl)
        com.cb1_extract()
        js_path = com.json_extract()
        mso = ModelShapeOperation(js_path)
        mso.bidlist_dict_create()
        mso.pose_modify(_model_id, _pose_height, _pose_scale)
        mso.json_scene_save()
        com.cb1_create(_cb1_folder=_folder)


def model_folder_remainder_delete(_cb1_file, _folder):
    cb1 = Cb1OperationModify(_cb1_file)
    cb1.cb1_extract()
    js_path = cb1.json_extract()
    mso = ModelShapeOperation(js_path)
    mso.bidlist_dict_create()
    _list = mso.bidx_dict.values()
    cb1.model_remainder_delete(_list)
    mso.json_scene_save()
    cb1.cb1_create(_cb1_folder=_folder)


if __name__ == '__main__':
    # cb1 = r'D:\myDocuments\Desktop\folderModi\wxCity_jlcIFS_f16f20_modify_modify.cb1'
    # model_id = '9f3c6b63-a99e-42bf-96c9-2084498d63be'
    # custom_model = 'u419wgcur7zusqkhza79rk0bwy67crse'
    # custom_scene = r'D:\myDocuments\Documents\pyqtGui\data\CustomModel\CustomModel_indoor.cb1'
    # xlsPath = r'D:\myDocuments\Documents\pyqtGui\data\xls\UserLib.xls'
    # sheetName = 'UserLib'
    # cb1_model_replace(model_id, cb1, custom_model, custom_scene, xlsPath, sheetName)
    cb1Folder = r"D:\myDocuments\Desktop\国金 - 防火分区修改20190530\cb1"
    Folder = r'D:\myDocuments\Desktop\国金 - 防火分区修改20190530\cb1_v11'
    cb1Lists = os.listdir(cb1Folder)
    for fl in cb1Lists:
        fl_path = os.path.join(cb1Folder, fl)
        model_folder_remainder_delete(fl_path, Folder)
