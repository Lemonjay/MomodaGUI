#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import xlrd
import xlwt
import os
import json
import shutil
import zipfile
from xlutils.copy import copy
from PackageOperation import Cb1Operation


class LineShapeOperation(object):
    '''
    因为防火分区和道路的需要，需要一些辅助要素，如：curveLines , arrowLines 和 arrowDataLines：
    # 1.通过point的个数和长度，进行选择，选择对象；
    # 2.线宽，高度，颜色；
    # 3.导出thingjs时，只保留了curvelines 和 pipelines 项
    '''

    # curve_selected = {}
    # arrow_selected = {}
    # arrow_data_selected = {}
    # routes_selected = {}
    # text3ds_selected = {}
    # pipe_selected = {}
    # leak_selected = {}

    def __init__(self, _json_scene):

        self.curve_selected = {}
        self.arrow_selected = {}
        self.arrow_data_selected = {}
        self.routes_selected = {}
        self.text3ds_selected = {}
        self.pipe_selected = {}
        self.leak_selected = {}

        self._json_folder = os.path.split(_json_scene)[0]
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            self.js_plan = self.js_dict['objects']['0']['plan']  # 室外场景
            self.js_bds = self.js_dict['objects']['0']['bds']
            if len(list(self.js_bds.keys())) == 1:  # 判断bds项是否只有一项
                print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']

    def curve_lines(self, _dict_plan, _math_relation, _point_num, _path_length_list):
        '''
        通过个数和线段长度范围作为条件来选择
        :param _dict_plan: self.plans 室内场景 ，self.plan 室外场景
        :param _math_relation: 判断运算符
        :param _point_num:
        :param _path_length_list:
        :return:
        '''

        def length_function(x, y):
            return (float(y) - float(x)) ** 2

        np_lists = list(_dict_plan.keys())
        for np in np_lists:
            js_num_plans = _dict_plan[np]
            # _floor = js_num_plans['uid']
            js_curve = js_num_plans['curveLines']
            for nc in list(js_curve.keys()):
                js_num_curve = js_curve[nc]
                js_path = js_num_curve['path']
                _length = 0
                if _math_relation == '==':
                    if len(js_path) == _point_num:
                        for i in range(len(js_path) - 1):
                            _point_coord1 = js_path[i + 1].split(' ')
                            _point_coord2 = js_path[i].split(' ')
                            _len_list = list(map(length_function, _point_coord1, _point_coord2))
                            _length = sum(_len_list) + _length
                        if _path_length_list[0] < _length <= _path_length_list[1]:
                            self.curve_selected[nc] = js_num_curve
                elif _math_relation == '>=':
                    if len(js_path) >= _point_num:
                        self.curve_selected[nc] = js_num_curve

                elif _math_relation == '<=':
                    if len(js_path) <= _point_num:
                        self.curve_selected[nc] = js_num_curve
        pass

    def arrow_lines(self, _dict_plan, _point_num, _path_length_list):
        def length_function(x, y):
            return (float(y) - float(x)) ** 2

        np_lists = list(_dict_plan.keys())
        for np in np_lists:
            js_num_plans = _dict_plan[np]
            # _floor = js_num_plans['uid']
            js_arrow = js_num_plans['arrowLines']
            for na in list(js_arrow.keys()):
                js_num_arrow = js_arrow[na]
                js_path = js_num_arrow['path']
                _length = 0
                if len(js_path) == _point_num:
                    for i in range(len(js_path) - 1):
                        _point_coord1 = js_path[i + 1].split(' ')
                        _point_coord2 = js_path[i].split(' ')
                        _len_list = list(map(length_function, _point_coord1, _point_coord2))
                        _length = sum(_len_list) + _length
                    if _path_length_list[0] < _length <= _path_length_list[1]:
                        self.arrow_selected[na] = js_num_arrow
        pass

    def arrow_data_lines(self, _dict_plan, _point_num, _path_length_list):
        def length_function(x, y):
            return (float(y) - float(x)) ** 2

        np_lists = list(_dict_plan.keys())
        for np in np_lists:
            js_num_plans = _dict_plan[np]
            # _floor = js_num_plans['uid']
            js_arrow_data = js_num_plans['arrowDataLines']
            for na in list(js_arrow_data.keys()):
                js_num_arrow_data = js_arrow_data[na]
                js_points = js_num_arrow_data['points']
                _length = 0
                if len(js_points) == _point_num:
                    for i in range(len(js_points) - 1):
                        _point_coord1 = js_points[i + 1]['pose'].split(' ')
                        _point_coord2 = js_points[i]['pose'].split(' ')
                        _len_list = list(map(length_function, _point_coord1, _point_coord2))
                        _length = sum(_len_list) + _length
                    if _path_length_list[0] < _length <= _path_length_list[1]:
                        self.arrow_data_selected[na] = js_num_arrow_data
        pass

    def routes_(self, _dict_plan, _point_num, _path_length_list):
        def length_function(x, y):
            return (float(y) - float(x)) ** 2

        np_lists = list(_dict_plan.keys())
        for np in np_lists:
            js_num_plans = _dict_plan[np]
            # _floor = js_num_plans['uid']
            js_routes = js_num_plans['routes']
            for na in list(js_routes.keys()):
                js_num_routes = js_routes[na]
                js_path = js_num_routes['path']
                _length = 0
                if len(js_path) == _point_num:
                    for i in range(len(js_path) - 1):
                        _point_coord1 = js_path[i + 1].split(' ')
                        _point_coord2 = js_path[i].split(' ')
                        _len_list = list(map(length_function, _point_coord1, _point_coord2))
                        _length = sum(_len_list) + _length
                    if _path_length_list[0] < _length <= _path_length_list[1]:
                        self.routes_selected[na] = js_num_routes
        pass

    def text_3ds(self, _dict_plan, _text_name):
        np_lists = list(_dict_plan.keys())
        for np in np_lists:
            js_num_plans = _dict_plan[np]
            js_text3d = js_num_plans['text3Ds']
            for nt in list(js_text3d.keys()):
                js_num_text3d = js_text3d[nt]
                if js_num_text3d['text'] == _text_name:
                    self.text3ds_selected[nt] = js_num_text3d
        pass

    def pipe_lines(self, _dict_plan, _point_num, _path_length_list, _shape):
        def length_function(x, y):
            return (float(y) - float(x)) ** 2

        np_lists = list(_dict_plan.keys())
        for np in np_lists:
            js_num_plans = _dict_plan[np]
            # _floor = js_num_plans['uid']
            js_pipe = js_num_plans['pipeLines']
            for na in list(js_pipe.keys()):
                js_num_pipe = js_pipe[na]
                js_path = js_num_pipe['path']
                _length = 0
                if len(js_path) == _point_num and js_num_pipe['secTp'] == _shape:
                    for i in range(len(js_path) - 1):
                        _point_coord1 = js_path[i + 1].split(' ')
                        _point_coord2 = js_path[i].split(' ')
                        _len_list = list(map(length_function, _point_coord1, _point_coord2))
                        _length = sum(_len_list) + _length
                    if _path_length_list[0] < _length <= _path_length_list[1]:
                        self.pipe_selected[na] = js_num_pipe
        pass

    def leak_water_lines(self, _dict_plan, _point_num, _path_length_list):
        def length_function(x, y):
            return (float(y) - float(x)) ** 2

        np_lists = list(_dict_plan.keys())
        for np in np_lists:
            js_num_plans = _dict_plan[np]
            # _floor = js_num_plans['uid']
            js_leak = js_num_plans['leakWaterLines']
            for na in list(js_leak.keys()):
                js_num_leak = js_leak[na]
                js_path = js_num_leak['path']
                _length = 0
                if len(js_path) == _point_num:
                    for i in range(len(js_path) - 1):
                        _point_coord1 = js_path[i + 1].split(' ')
                        _point_coord2 = js_path[i].split(' ')
                        _len_list = list(map(length_function, _point_coord1, _point_coord2))
                        _length = sum(_len_list) + _length
                    if _path_length_list[0] < _length <= _path_length_list[1]:
                        self.leak_selected[na] = js_num_leak
        pass

    def parameters_add(self, _dict_parameter, _parameter_name, _parameter_value):
        '''
        :param _dict_parameter: 目标dict: curve_selected ,arrow_selected, arrow_data_selected
        :param _parameter_name: 'color': (r/255,g/255,b/255,opacity) , 'width': float() ,pose_h: float()
        :param _parameter_value:
        :return:
        '''
        for ns in list(_dict_parameter.keys()):
            num_temp = _dict_parameter[ns]

            # Text 3D 文字
            if num_temp['name'] == 'Text3D':  # 该项在thingjs 中不显示
                if _parameter_name == 'color':
                    num_temp['col'] = _parameter_value
                elif _parameter_name == 'font':
                    num_temp['font'] = _parameter_value
                elif _parameter_name == 'pose_h':
                    pose_list = num_temp['pos'].split(' ')
                    num_temp['pos'] = '{0} {1} {2}'.format(pose_list[0], _parameter_value, pose_list[2])
                    num_temp['sus'] = _parameter_value

            # LeakWaterLine 没有颜色key值，但是可以修改颜色，且可以在campus builder 可以中显示，
            # 显示的颜色与蓝色叠加的效果，再编辑后导出，没有‘col’项
            elif num_temp['name'] == 'LeakWaterLine':
                if _parameter_name == 'pose_h':
                    pose_list = num_temp['pos'].split(' ')
                    num_temp['pos'] = '{0} {1} {2}'.format(pose_list[0], _parameter_value, pose_list[2])

            # pipline 没有颜色key值，但是可以修改颜色，且可以在campus builder 中显示，
            # 保存后再编辑后导出，没有‘col’项，默认蓝色
            elif num_temp['name'] == 'PipeLine':
                if _parameter_name == 'radius':
                    num_temp['rds'] = _parameter_value
                elif _parameter_name == 'pose_h':
                    pose_list = num_temp['pos'].split(' ')
                    num_temp['pos'] = '{0} {1} {2}'.format(pose_list[0], _parameter_value, pose_list[2])

            # curveLines,arrowLines,arrowDataLines,routes
            else:
                if _parameter_name == 'color':
                    num_temp['col'] = _parameter_value
                elif _parameter_name == 'width':
                    num_temp['wd'] = _parameter_value
                elif _parameter_name == 'pose_h':
                    pose_list = num_temp['pos'].split(' ')
                    num_temp['pos'] = '{0} {1} {2}'.format(pose_list[0], _parameter_value, pose_list[2])
        pass

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


def curve_lines_parameters_add(cb1_files, outdoor_bool, folder, parameter_dict, math_relation, point_num,
                               path_length_list=None):
    '''
    曲线的属性参数修改
    :param cb1_files:
    :param outdoor_bool:
    :param folder:
    :param parameter_dict:
    :param math_relation:
    :param point_num:
    :param path_length_list:
    :return:
    '''
    for fl in cb1_files:
        cb1 = Cb1Operation(fl)
        js_path = cb1.json_extract()
        lso = LineShapeOperation(js_path)
        if outdoor_bool:
            lso.curve_lines(lso.js_plan, math_relation, point_num, path_length_list)
        else:
            lso.curve_lines(lso.js_plans, math_relation, point_num, path_length_list)

        for key in list(parameter_dict.keys()):
            lso.parameters_add(lso.curve_selected, key, parameter_dict[key])
        lso.json_scene_save()
        cb1.cb1_create(_cb1_folder=folder)
    pass
