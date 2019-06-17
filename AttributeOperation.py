#!/usr/bin/python3.7
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


class BasicAttribute(object):
    '''
    楼层室内要素UserId和属性添加
    '''
    js_plans = {}
    bidx_dict = {}
    _mmd_target_dict = {}

    # 对于只有一个室内建筑场景
    def __init__(self, _json_scene):
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as self.js:
            self.js_dict = json.loads(self.js.read())
            # 室外场景
            self.js_plan = self.js_dict['objects']['0']['plan']

            # 建筑楼层
            try:
                self.js_bds = self.js_dict['objects']['0']['bds']
                if len(list(self.js_bds.keys())) == 1:  # 判断bds项是否只有一项
                    print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                    self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']
            except:
                print('The {} key was not existed'.format('bds'))

    # 根据"bIdList"矩阵创建bIdx字典
    def bidlist_dict_create(self):
        _bid_lists = self.js_dict['bIdList']
        for i in range(len(_bid_lists)):
            self.bidx_dict.update({str(i): _bid_lists[i][2]})
        print('bIdList value dict: {}'.format(self.bidx_dict))

    # 创建user lib excel
    def user_lib_create(self, _xls_mmd_path, _sheet_mmd_name, _xls_user_path, _sheet_user_name):
        _bid_lists = self.js_dict['bIdList']
        _mc = ModelClassify(_bid_lists)
        _mc.got_user_dict(_xls_mmd_path, _sheet_mmd_name)
        _mc.dict2excel(_xls_user_path, _sheet_user_name)

    # 创建属性字典
    def mmd_dict_create(self, _xls_path, _sheet_name, _xls_user_path=None, _sheet_user_name=None):
        _bid_lists = self.js_dict['bIdList']
        _mc = ModelClassify(_bid_lists)
        _mc.user_target_dict(_xls_path, _sheet_name, _xls_user_path, _sheet_user_name)
        self._mmd_target_dict = _mc.mmd_target_dict

    def field_value_got(self, _bidx, _field):  # 根据模型在bIdLists中排序，获取相应字段的值
        if str(_bidx) in list(self._mmd_target_dict.keys()):
            _dict = self._mmd_target_dict[str(_bidx)]
            _value = _dict[_field]
            return _value

    # json文件的ItemId进行了自定义
    def plcs_attribute_add(self, _field):
        print('plcs attribute add')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if 'clds' not in list(js_num_plcs.keys()):
                    _bidx = js_num_plcs['bIdx']
                    _npls_num = npls
                    _uid = '{2}{0}{1}'.format(_npls_num, _floor, self.field_value_got(_bidx, 'userid_prefix'))
                    _name = self.field_value_got(_bidx, 'type_name')
                    # 添加模型固定属性user id和name
                    if 'uid' not in list(js_num_plcs.keys()):
                        js_num_plcs.update({'uid': _uid})
                    js_num_plcs.update({'name': _name})
                    # 添加指定字段field属性
                    if len(self.field_value_got(_bidx, _field)) != 0:
                        if 'prop' not in list(js_num_plcs.keys()):
                            js_num_plcs.update({'prop': {_field: self.field_value_got(_bidx, _field)}})
                        else:
                            js_num_plcs['prop'][_field] = self.field_value_got(_bidx, _field)
                else:
                    js_clds = js_num_plcs['clds']
                    for ncls in list(js_clds.keys()):
                        js_num_clds = js_clds[ncls]
                        _bidx = js_num_clds['bIdx']
                        _npls_num = npls
                        _uid = '{2}{0}{1}'.format(_npls_num, _floor, self.field_value_got(_bidx, 'userid_prefix'))
                        _name = self.field_value_got(_bidx, 'type_name')
                        # 添加模型固定属性user id和name
                        if 'uid' not in list(js_num_plcs.keys()):
                            js_num_plcs.update({'uid': _uid})
                        js_num_plcs.update({'name': _name})
                        # 添加指定字段field属性
                        if len(self.field_value_got(_bidx, _field)) != 0:
                            if 'prop' not in list(js_num_plcs.keys()):
                                js_num_plcs.update({'prop': {_field: self.field_value_got(_bidx, _field)}})
                            else:
                                js_num_plcs['prop'][_field] = self.field_value_got(_bidx, _field)

    # dws attribute add
    def dws_attribute_add(self, _field):
        print('dws attribute add')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for nd in list(js_dws.keys()):
                        js_num_dws = js_dws[nd]
                        _bidx_name = self.bidx_dict[str(js_num_dws['bIdx'])]
                        if _bidx_name != '空窗户':
                            _bidx = js_num_dws['bIdx']
                            _npls_num = nd
                            _uid = '{2}{0}{1}'.format(_npls_num, _floor, self.field_value_got(_bidx, 'userid_prefix'))
                            _name = self.field_value_got(_bidx, 'type_name')
                            # 添加模型固定属性user id和name
                            if 'uid' not in list(js_num_dws.keys()):
                                js_num_dws.update({'uid': _uid})
                            js_num_dws.update({'prop': {'name': _name}})
                            # 添加指定字段field属性
                            if len(self.field_value_got(_bidx, _field)) != 0:
                                js_num_dws['prop'][_field] = self.field_value_got(_bidx, _field)

    # rooms attribute add
    def rooms_attribute_add(self):
        print('rooms attribute add')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plan = self.js_plans[np]
            _floor = js_num_plan['uid']
            js_rooms = js_num_plan['rooms']
            for nr in list(js_rooms.keys()):
                js_num_rooms = js_rooms[nr]
                _nr_num = nr
                # 添加 'uid' 和 'name'项的属性
                js_num_rooms.update({'uid': '{0}{1}{2}'.format('r', _nr_num, _floor)})
                # js_num_rooms.update({'name': _code_list[0]})

    # execute main function
    def indoor_attribute_execute(self, _field, _xls_mmd_path, _sheet_mmd_name, _xls_user_path=None,
                                 _sheet_user_name=None):
        self.bidlist_dict_create()
        self.mmd_dict_create(_xls_mmd_path, _sheet_mmd_name, _xls_user_path, _sheet_user_name)
        self.dws_attribute_add(_field)
        self.plcs_attribute_add(_field)
        self.rooms_attribute_add()

    # 室外场景添加属性
    # outdoor scene
    def plcs_attribute_outdoor(self, _field):
        js_plcs = self.js_plan[list(self.js_plan.keys())[0]]['plcs']
        for npls in list(js_plcs.keys()):
            js_num_plcs = js_plcs[npls]
            if 'clds' not in list(js_num_plcs.keys()):
                # _bidx_name = self.bidx_dict[js_num_plcs['bIdx']]
                _bidx = js_num_plcs['bIdx']
                _npls_num = npls
                _uid = '{1}{0}'.format(_npls_num, self.field_value_got(_bidx, 'userid_prefix'))
                _name = self.field_value_got(_bidx, 'type_name')
                # 添加模型固定属性user id和name
                if 'uid' not in list(js_num_plcs.keys()):
                    js_num_plcs.update({'uid': _uid})
                if js_num_plcs['name'] == '物体' or len(js_num_plcs['name']) == 0:
                    js_num_plcs.update({'name': _name})
                # 添加指定字段field属性
                if len(self.field_value_got(_bidx, _field)) != 0:
                    js_num_plcs.update({'prop': {_field: self.field_value_got(_bidx, _field)}})

            else:
                js_clds = js_num_plcs['clds']
                for ncls in list(js_clds.keys()):
                    js_num_clds = js_clds[ncls]
                    _bidx = js_num_clds['bIdx']
                    _npls_num = npls
                    _uid = '{1}{0}'.format(_npls_num, self.field_value_got(_bidx, 'userid_prefix'))
                    _name = self.field_value_got(_bidx, 'type_name')
                    # 添加模型固定属性user id和name
                    if 'uid' not in list(js_num_plcs.keys()):
                        js_num_plcs.update({'uid': _uid})
                    if js_num_plcs['name'] == '组' or len(js_num_plcs['name']) == 0:
                        js_num_plcs.update({'name': _name})
                    # 添加指定字段field属性
                    if len(self.field_value_got(_bidx, _field)) != 0:
                        js_num_plcs.update({'prop': {_field: self.field_value_got(_bidx, _field)}})

        # dws attribute add

    def dws_attribute_outdoor(self, _field):
        print('dws attribute add')
        np_lists = list(self.js_plan.keys())
        for np in np_lists:
            js_num_plans = self.js_plan[np]
            # _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for nd in list(js_dws.keys()):
                        js_num_dws = js_dws[nd]
                        _bidx_name = self.bidx_dict[str(js_num_dws['bIdx'])]
                        if _bidx_name != '空窗户':
                            _bidx = js_num_dws['bIdx']
                            _npls_num = nd
                            _uid = '{1}{0}'.format(_npls_num, self.field_value_got(_bidx, 'userid_prefix'))
                            _name = self.field_value_got(_bidx, 'type_name')
                            # 添加模型固定属性user id和name
                            if 'uid' not in list(js_num_dws.keys()):
                                js_num_dws.update({'uid': _uid})
                            js_num_dws.update({'prop': {'name': _name}})
                            # 添加指定字段field属性
                            if len(self.field_value_got(_bidx, _field)) != 0:
                                js_num_dws['prop'].update({_field: self.field_value_got(_bidx, _field)})

    def rooms_attribute_outdoor(self):
        print('rooms attribute add')
        np_lists = list(self.js_plan.keys())
        for np in np_lists:
            js_num_plan = self.js_plan[np]
            # _floor = js_num_plan['uid']
            js_rooms = js_num_plan['rooms']
            for nr in list(js_rooms.keys()):
                js_num_rooms = js_rooms[nr]
                _nr_num = nr
                # 添加 'uid' 和 'name'项的属性
                if 'uid' not in list(js_num_rooms.keys()):
                    js_num_rooms.update({'uid': '{0}{1}'.format('s', _nr_num)})
                    js_num_rooms.update({'name': '建筑用地'})

    def outdoor_attribute_execute(self, _field, _xls_mmd_path, _sheet_mmd_name, _xls_user_path=None,
                                  _sheet_user_name=None):
        self.bidlist_dict_create()
        self.mmd_dict_create(_xls_mmd_path, _sheet_mmd_name, _xls_user_path, _sheet_user_name)
        self.plcs_attribute_outdoor(_field)
        self.dws_attribute_outdoor(_field)
        self.rooms_attribute_outdoor()

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        self.js.close()
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)
        js.close()


class AdvanceAttribute(object):
    '''
    给指定模型（通过Model ID）添加属性字段
    '''

    # _bid_list_dict = {}
    # _model_info = []
    # _model_dict = {}

    # 对于只有一个室内建筑场景
    def __init__(self, _json_scene):
        self._bid_list_dict = {}
        self._model_info = []
        self._model_dict = {}
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as self.js:
            self.js_dict = json.loads(self.js.read())
            # 室外场景
            self.js_plan = self.js_dict['objects']['0']['plan']

            # 建筑楼层
            try:
                self.js_bds = self.js_dict['objects']['0']['bds']
                if len(list(self.js_bds.keys())) == 1:  # 判断bds项是否只有一项
                    print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                    self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']
            except:
                print('The {} key was not existed'.format('bds'))

    def bidlist_dict_create(self):
        '''
        根据"bIdList"矩阵创建bIdx字典
        :return:
        '''
        js_bidx = self.js_dict['bIdList']
        for i in range(len(js_bidx)):
            self._bid_list_dict.update({str(i): js_bidx[i][0]})
        print('bIdList value dict: {}'.format(self._bid_list_dict))

    def _model_bidx_got(self, _model_id):
        '''
        :param _model_id: 模模搭中的模型ID
        :return: 模模搭bIDList 模型矩阵中的排序的序号
        '''
        _temp_dict = dict(zip(self._bid_list_dict.values(), self._bid_list_dict.keys()))
        return _temp_dict[_model_id]

    # Indoor & Outdoor Scene Info extract
    def plcs_model_info_extract_indoor(self, _model_id):
        '''
        将cb1文件中指定模型的pose信息提取出来，生成excel表格
        :param _model_id: 模型id
        :return:
        '''
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            # _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if 'clds' not in list(js_num_plcs.keys()):
                    if js_num_plcs['bIdx'] == self._model_bidx_got(_model_id):
                        temp_info = {'key': str(npls), 'model_id': _model_id, 'model_info': str(js_num_plcs)}
                        self._model_info.append(temp_info)
                else:
                    js_clds = js_num_plcs['clds']
                    for ncls in list(js_clds.keys()):
                        js_num_clds = js_clds[ncls]
                        if js_num_clds['bIdx'] == self._model_bidx_got(_model_id):
                            temp_info = {'key': str(npls), 'model_id': _model_id, 'model_info': str(js_num_plcs)}
                            self._model_info.append(temp_info)
                            break
        # _xls_title = ['id', 'model_id', 'model_info']
        # excel_create_write(_xls_path, _sheet_name, _model_info, _xls_title)

    def dws_model_info_extract_indoor(self, _model_id):
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            # _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for nd in list(js_dws.keys()):
                        js_num_dws = js_dws[nd]
                        if js_num_dws['bIdx'] == self._model_bidx_got(_model_id):
                            temp_info = {'key': str(nd), 'model_id': _model_id, 'model_info': str(js_num_dws)}
                            self._model_info.append(temp_info)

    def plcs_model_info_extract_outdoor(self, _model_id):
        '''
        将cb1文件中指定模型的pose信息提取出来，生成excel表格
        :param _model_id: 模型id
        :return:
        '''
        np_lists = list(self.js_plan.keys())
        for np in np_lists:
            js_num_plans = self.js_plan[np]
            # _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if 'clds' not in list(js_num_plcs.keys()):
                    if js_num_plcs['bIdx'] == self._model_bidx_got(_model_id):
                        temp_info = {'key': str(npls), 'model_id': _model_id, 'model_info': str(js_num_plcs)}
                        self._model_info.append(temp_info)
                else:
                    js_clds = js_num_plcs['clds']
                    for ncls in list(js_clds.keys()):
                        js_num_clds = js_clds[ncls]
                        if js_num_clds['bIdx'] == self._model_bidx_got(_model_id):
                            temp_info = {'key': str(npls), 'model_id': _model_id, 'model_info': str(js_num_plcs)}
                            self._model_info.append(temp_info)
                            break

    def dws_model_info_extract_outdoor(self, _model_id):
        np_lists = list(self.js_plan.keys())
        for np in np_lists:
            js_num_plans = self.js_plan[np]
            # _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for nd in list(js_dws.keys()):
                        js_num_dws = js_dws[nd]
                        if js_num_dws['bIdx'] == self._model_bidx_got(_model_id):
                            temp_info = {'key': str(nd), 'model_id': _model_id, 'model_info': str(js_num_dws)}
                            self._model_info.append(temp_info)

    # excel create
    def excel_create(self, _xls_path, _sheet_name):
        _xls_title = ['key', 'model_id', 'model_info']
        excel_create_write(_xls_path, _sheet_name, self._model_info, _xls_title)

    def excel_to_dict(self, _xls_path, _sheet_name):
        _temp_dict = excel2dict(_xls_path, _sheet_name, 'key')
        _list = list(_temp_dict.keys())
        for i in range(len(_list)):
            _key = _list[i]
            try:
                self._model_dict.update({str(int(float(_key))): _temp_dict[_key]})
            except:
                self._model_dict.update({_key: _temp_dict[_key]})

    def _field_value_add(self, _dict, _fields, _model_dict):
        if 'prop' not in list(_dict.keys()):
            _dict['prop'] = {}
        for fld in _fields:
            _dict['prop'][fld] = _model_dict[fld]

    # Attribute Add
    def plcs_attribute_add_indoor(self, _fields):
        print('plcs attribute add')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if str(npls) in list(self._model_dict.keys()):
                    if str(js_num_plcs) == self._model_dict[str(npls)]['model_info']:
                        self._field_value_add(js_num_plcs, _fields, self._model_dict[str(npls)])

    def dws_attribute_add_indoor(self, _fields):
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for nd in list(js_dws.keys()):
                        js_num_dws = js_dws[nd]
                        if str(nd) in list(self._model_dict.keys()):
                            if str(js_num_dws) == self._model_dict[str(nd)]['model_info']:
                                self._field_value_add(js_num_dws, _fields, self._model_dict[str(nd)])

    def plcs_attribute_add_outdoor(self, _fields):
        print('plcs attribute add')
        np_lists = list(self.js_plan.keys())
        for np in np_lists:
            js_num_plans = self.js_plan[np]
            # _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if str(npls) in list(self._model_dict.keys()):
                    if str(js_num_plcs) == self._model_dict[str(npls)]['model_info']:
                        print(list(self._model_dict.keys()))
                        self._field_value_add(js_num_plcs, _fields, self._model_dict[str(npls)])
                        print(js_num_plcs)

    def dws_attribute_add_outdoor(self, _fields):
        np_lists = list(self.js_plan.keys())
        for np in np_lists:
            js_num_plans = self.js_plan[np]
            # _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for nd in list(js_dws.keys()):
                        js_num_dws = js_dws[nd]
                        if str(nd) in list(self._model_dict.keys()):
                            if str(js_num_dws) == self._model_dict[str(nd)]['model_info']:
                                self._field_value_add(js_num_dws, _fields, self._model_dict[str(nd)])

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        self.js.close()
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)
        js.close()


# Execute function
def attribute_statistic(cb1_files, blib_xls, ulib_xls):
    for fl in cb1_files:
        co = Cb1Operation(fl)
        js_scene = co.json_extract()
        mao = BasicAttribute(js_scene)
        mao.user_lib_create(blib_xls, 'BundleLib', ulib_xls, 'UserLib')
        co.cb1_create()


def attribute_add_indoor(cb1_files, field, blib_xls, ulib_xls, result_folder):
    for fl in cb1_files:
        co = Cb1Operation(fl)
        js_scene = co.json_extract()
        mao = BasicAttribute(js_scene)
        # mao.user_lib_create(blib_xls, 'BundleLib', ulib_xls, 'UserLib')
        mao.indoor_attribute_execute(field, blib_xls, 'BundleLib', ulib_xls, 'UserLib')
        mao.json_scene_save()
        co.cb1_create(_cb1_folder=result_folder)


def attribute_add_outdoor(cb1_files, field, blib_xls, ulib_xls, result_folder):
    for fl in cb1_files:
        co = Cb1Operation(fl)
        js_scene = co.json_extract()
        mao = BasicAttribute(js_scene)
        # mao.user_lib_create(blib_xls, 'BundleLib', ulib_xls, 'UserLib')
        mao.outdoor_attribute_execute(field, blib_xls, 'BundleLib', ulib_xls, 'UserLib')
        mao.json_scene_save()
        co.cb1_create(_cb1_folder=result_folder)


def model_attribute_extract(cb1_files, model_id, xls_path, scene_selection=False):
    for fl in cb1_files:
        co = Cb1Operation(fl)
        js_scene = co.json_extract()
        mao = AdvanceAttribute(js_scene)
        mao.bidlist_dict_create()
        if scene_selection:  # 默认Indoor Scene
            mao.plcs_model_info_extract_outdoor(model_id)
            mao.dws_model_info_extract_outdoor(model_id)
        else:
            mao.plcs_model_info_extract_indoor(model_id)
            mao.dws_model_info_extract_indoor(model_id)

        mao.excel_create(xls_path, 'Sheet1')
        co.cb1_create()


def model_attribute_add(cb1_files, fields, xls_path, _folder, scene_selection=False):
    for fl in cb1_files:
        co = Cb1Operation(fl)
        js_scene = co.json_extract()
        mao = AdvanceAttribute(js_scene)
        mao.bidlist_dict_create()
        mao.excel_to_dict(xls_path, 'Sheet1')
        if scene_selection:  # 默认Indoor Scene
            mao.plcs_attribute_add_outdoor(fields)
            mao.dws_attribute_add_outdoor(fields)
        else:
            mao.plcs_attribute_add_indoor(fields)
            mao.dws_attribute_add_indoor(fields)
        mao.json_scene_save()
        co.cb1_create(_cb1_folder=_folder)
