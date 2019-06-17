# !/usr/bin/python3.7
# -*- coding: utf-8 -*-

import xlrd
import xlwt
import os
import json
from xlutils.copy import copy
from PackageOperation import Cb1Operation


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


class GisMmdDataConvert(object):
    '''
    1.因为缩放和共面问题，需要修改插入物体高度和垂直位置，调整起来比较麻烦；
    2.平面位置不好修改，目前可以修改的两个参数：pos (位置)悬空位置数据，相对于楼层的位置；
    3.scl（比例，高度）相对于原插入物体的比例而言
    '''
    js_plans = {}
    _bid_list_dict = {}

    # 对于只有一个室内建筑场景
    def __init__(self, _json_scene):
        self.js_plans = {}
        self._bid_list_dict = {}
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            self.js_bds = self.js_dict['objects']['0']['bds']
            self.js_plan = self.js_dict['objects']['0']['plan']  # 室外场景plan
            if len(list(self.js_bds.keys())) == 1:  # 判断bds项是否只有一项
                print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']  # 室内场景plans
                pass

    def bidlist_add(self, _model_id, _xls_path, _sheet_name):
        '''
        根据模型的id，从excel中调取指定的'model_info'模型信息，添加到bIdList中
        :param _model_id:
        :param _xls_path: 19294BundleLib.xlsx 模模搭模型库
        :param _sheet_name:
        :return:
        '''
        # _temp_str = field_value_got(_model_id, 'model_info', _xls_path, _sheet_name)
        # print(_temp_str)
        # _temp_list = [x.replace("'", "") for x in _temp_str.split(',')]
        # _temp_list[0] = _temp_list[0].replace('[', '')
        # _temp_list[-1] = _temp_list[0].replace(']', '')
        _temp_list = eval(field_value_got(_model_id, 'model_info', _xls_path,
                                          _sheet_name))  # 将字符串'[value,value,.....]'转换成 list，dict也可以用
        if list(_temp_list) not in self.js_dict['bIdList']:
            self.js_dict['bIdList'].append(_temp_list)

    def bidlist_dict_create(self):
        '''
        根据"bIdList"矩阵创建bIdx字典
        :return:
        '''
        js_bidx = self.js_dict['bIdList']
        for i in range(len(js_bidx)):
            self._bid_list_dict.update({str(i): js_bidx[i][0]})
        print('bIdList value dict: {}'.format(self._bid_list_dict))

    def model_bidx_got(self, _model_id):
        '''
        :param _model_id: 模模搭中的模型ID
        :return: 模模搭bIDList 模型矩阵中的排序的序号
        '''
        _temp_dict = dict(zip(self._bid_list_dict.values(), self._bid_list_dict.keys()))
        return _temp_dict[_model_id]

    def pose_excel_extract(self, _model_id, _xls_path, _sheet_name):
        '''
        将cb1文件中指定模型的pose信息提取出来，生成excel表格
        :param _model_id: 模型id
        :param _xls_path: 生成的excel路径
        :param _sheet_name: excel表格中的sheet的名称
        :return:
        '''
        _model_pose = []
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            # _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if 'clds' not in list(js_num_plcs.keys()):
                    if js_num_plcs['bIdx'] == self.model_bidx_got(_model_id):
                        if 'uid' in list(js_num_plcs.keys()):
                            temp_pose = {'id': str(js_num_plcs['uid']), 'pose': js_num_plcs['pos']}
                            _model_pose.append(temp_pose)
                        else:
                            print('The model had no "uid" keys')
                            temp_pose = {'id': str(npls), 'pose': js_num_plcs['pos']}
                            _model_pose.append(temp_pose)
                else:
                    print('The js_num_pls item had a group')
        _xls_title = ['id', 'pose']
        excel_create_write(_xls_path, _sheet_name, _model_pose, _xls_title)

    def plcs_model_dict_extract(self, _xls_path, _sheet_name):
        '''
        将样本中模型插入的model_dict，提取出来存入excel表中
        :param _xls_path:
        :param _sheet_name:
        :return:
        '''
        _model_dict = []
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            # _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if 'clds' not in list(js_num_plcs.keys()):
                    _model_id = self._bid_list_dict[js_num_plcs['bIdx']]
                    temp_dict = {'model_id': _model_id, 'model_dict': str(js_plcs[npls])}
                    _model_dict.append(temp_dict)
                else:
                    print('The js_num_pls item had a "clds" group.')
        _xls_title = ['model_id', 'model_dict']
        excel_create_write(_xls_path, _sheet_name, _model_dict, _xls_title)

    def _gis_model_dict(self, _model_id, _pose, _uid_part, _xls_path, _sheet_name):
        '''
        根据模型的id，从excel中调取指定的'model_info'模型信息，添加到bIdList中
        def model_insert(_bidx, _uid, _pos, _type_name, _type_chs):
            _plcs_model = {
                "name": _type_name,
                "clsId": 3,
                "uid": _uid,
                "pos": _pos,
                "rot": "0.000 1.000 0.000 0.000",
                "bIdx": _bidx,
                "prop": {'TYPE': _type_chs},
                "AnimInfo": {
                    "clip": "rotate"
                }}
        :param _model_id:
        :param _pose:位置信息
        :param _uid_part: 加入的编号
        :param _xls_path:19294BundleLib.xlsx 模模搭模型库
        :param _sheet_name:
        :return:
        '''
        _temp_dict = eval(field_value_got(_model_id, 'model_dict', _xls_path, _sheet_name))
        # print(_temp_dict)
        _temp_dict['name'] = field_value_got(_model_id, 'type_name', _xls_path, _sheet_name)  # 模型类别名称
        _temp_dict['bIdx'] = self.model_bidx_got(_model_id)
        _temp_dict['pos'] = _pose
        _uid = '{0}{1}'.format(field_value_got(_model_id, 'userid_prefix', _xls_path, _sheet_name), _uid_part)
        _temp_dict.update({'uid': _uid})
        if 'prop' not in list(_temp_dict.keys()):
            _temp_dict.update({'prop': {'TYPE': field_value_got(_model_id, 'TYPE', _xls_path, _sheet_name)}})
        else:
            _temp_prop = _temp_dict['prop']
            _temp_prop.update({'TYPE': field_value_got(_model_id, 'TYPE', _xls_path, _sheet_name)})
        return _temp_dict

    def gis_model_insert_indoor(self, _model_id, _gis_xls_path, _gis_sheet_name, _mmd_xls_path, _mmd_sheet_name,
                                *_field_list):
        '''
        将GIS点位数据通过一定的转换关系，pose信息转换，插入模模搭的cb1模型中，打通GIS和模模搭的模型生产的流程。
        基础信息的添加：("uid","pos","bIdx","prop": {'TYPE': value})
        :param _model_id:
        :param _gis_xls_path: 点位模型的pose excel表
        :param _gis_sheet_name:
        :param _mmd_xls_path: 模模搭模型的类型库
        :param _mmd_sheet_name:
        :return:
        '''
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            _gis_xls = xlrd.open_workbook(_gis_xls_path)
            _gis_table = _gis_xls.sheet_by_name(_gis_sheet_name)
            for i in range(1, _gis_table.nrows):
                _id = _gis_table.cell_value(i, 0)
                # print(_id)
                # _model_id_xls = field_value_got(_id, 'model_id', _gis_xls_path, _gis_sheet_name, 'id')
                _model_id_xls = field_value_got(_id, 'model_id', _gis_xls_path, _gis_sheet_name, 'id').replace("'", "")
                _floor_xls = field_value_got(_id, 'floor_name', _gis_xls_path, _gis_sheet_name, 'id')
                # print(_model_id_xls)
                # print(_id)
                if _floor == _floor_xls and _model_id == _model_id_xls:
                    _uid_part = '{0}{1}'.format(str(int(_id)), _floor)
                    _pose = '{0} {1} {2}'.format(
                        round(field_value_got(_id, 'pose_x', _gis_xls_path, _gis_sheet_name, 'id'), 3),
                        round(field_value_got(_id, 'pose_h', _gis_xls_path, _gis_sheet_name, 'id'), 3),
                        round(field_value_got(_id, 'pose_y', _gis_xls_path, _gis_sheet_name, 'id'), 3))
                    _temp_dict = self._gis_model_dict(_model_id, _pose, _uid_part, _mmd_xls_path, _mmd_sheet_name)
                    _num_key = _temp_dict['uid']  # 该项为了保持数据的唯一性，暂时给的编码，后续需要通过JsonIdCoding类，进行重新编码
                    print(_num_key)
                    if _field_list:
                        for fld in _field_list:
                            fld_value = field_value_got(_model_id, fld, _gis_xls_path, _gis_sheet_name)
                            _temp_dict['prop'].update({fld: fld_value})
                    js_plcs.update({_num_key: _temp_dict})

    def outdoor_scene_delete(self):
        '''
        因为是在室外场景下制作室内场景的，室内场景下保留了室外场景，现在因为需要，要将室外场景删除。
        （制作无锡国金时，在室外场景下制作室内场景的，这样可以保证模型的位置确定性，更好地合作和分工）
        目前，已经知道可以在ps下进行配准，目前，该功能基本上用不到
        :return: model_id lists 返回值
        '''
        np_lists = list(self.js_plan.keys())
        # print(np_lists)
        _model_id_list = []
        for np in np_lists:
            js_num_plan = self.js_plan[np]
            # 删除室外场景
            for key in list(js_num_plan.keys()):
                if key not in ['name', 'clsId', 'bmUrl', 'bmAlpha', 'bmScale', 'bmCenter']:
                    js_num_plan.pop(key)
            # 删除外立面模型
            for nb in list(self.js_bds.keys()):
                js_num_bds = self.js_bds[nb]
                js_facades = js_num_bds['facades']
                for fn in list(js_facades.keys()):
                    js_num_facades = js_facades[fn]
                    _model_id = self._bid_list_dict[str(js_num_facades['bIdx'])]
                    _model_id_list.append(_model_id)
                js_num_bds['facades'] = {}
        return _model_id_list

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


def mmd_gis_pose_extract(_cb1_path, _model_id, _pose_xls):
    '''
    统一配准的底图下，在gis创建fishnet，有生成gis点位的底图，
    以该底图为参考，创建带有对应点位的cb1文件，提取点位pose数据，
    通过与gis的坐标相比较，找出对应的转换关系。
    :param _cb1_path:
    :param _model_id:
    :param _pose_xls:
    :return:
    '''
    cb1 = Cb1Operation(_cb1_path)
    js_scene = cb1.json_extract()
    mso = GisMmdDataConvert(js_scene)
    mso.bidlist_dict_create()
    mso.pose_excel_extract(_model_id, _pose_xls, 'Sheet1')
    cb1.cb1_create()


def mmd_model_dict_extract(_cb1_path, _dict_xls):
    '''
    提取plcs项插入模型的dict字典
    :param _cb1_path:
    :param _dict_xls:
    :return:
    '''
    cb1 = Cb1Operation(_cb1_path)
    js_scene = cb1.json_extract()
    mso = GisMmdDataConvert(js_scene)
    mso.bidlist_dict_create()
    mso.plcs_model_dict_extract(_dict_xls, 'Sheet1')
    cb1.cb1_create()


def gis_model_insert(_model_id, _cb1_files, _gis_xls, _lib_xls, _field_lists, _folder):
    '''
    通过xls 表添加模型数据，并添加对应的模型属性
    :param _model_id:
    :param _cb1_files:
    :param _gis_xls:
    :param _lib_xls:
    :param _field_lists:
    :param _folder:
    :return:
    '''
    for fl in _cb1_files:
        cb1 = Cb1Operation(fl)
        js_scene = cb1.json_extract()
        mso = GisMmdDataConvert(js_scene)
        lib_sheet_name = 'BundleLib' if 'BundleLib' in _lib_xls else 'UserLib'  # 默认的两个库：19294BundleLib和UserLib
        mso.bidlist_add(_model_id, _lib_xls, lib_sheet_name)
        mso.bidlist_dict_create()
        mso.gis_model_insert_indoor(_model_id, _gis_xls, 'Sheet1', _lib_xls, lib_sheet_name, *_field_lists)
        mso.json_scene_save()
        cb1.cb1_create(_cb1_folder=_folder)
        # print(len(list(mso.js_plans.keys())))
        # print(len(list(mso._bid_list_dict.keys())))
