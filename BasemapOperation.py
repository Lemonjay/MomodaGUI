#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import os
import json
import time
import shutil
from PackageOperation import Cb1Operation


# Base Map Operation
class JsonBaseMap(object):
    def __init__(self, _json_scene):
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            self.js_bds = self.js_dict['objects']['0']['bds']
            self.js_outplan = self.js_dict['objects']['0']['plan']
            if len(list(self.js_bds.keys())) == 1:
                print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']

    def indoor_features_delete(self, _input_floor):
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            if _input_floor == js_num_plans['uid']:
                js_num_plans['corners'] = {}
                js_num_plans['rooms'] = {}
                js_num_plans['walls'] = {}

    def indoor_map_add(self, _input_floor, _base_map=None, _bm_save_path=None):
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            if _input_floor == js_num_plans['uid']:
                _id_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                _postfix_bm = _base_map.split('.')[-1] if _base_map else '.jpg'
                js_num_plans['bmUrl'] = _id_time + _input_floor + '.' + _postfix_bm
                print(js_num_plans['bmUrl'])
                if _base_map and _bm_save_path:
                    shutil.copy(_base_map, os.path.join(_bm_save_path, js_num_plans['bmUrl']))

    def outdoor_map_add(self, _out_scene, _base_map=None, _bm_save_path=None):
        if _out_scene == 'Outdoor Scene':
            js_num_outplan = self.js_outplan[list(self.js_outplan.keys())[0]]
            _id_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            _postfix_bm = _base_map.split('.')[-1] if _base_map else '.jpg'
            js_num_outplan['bmUrl'] = _id_time + '.' + _postfix_bm
            print(js_num_outplan['bmUrl'])
            if _base_map and _bm_save_path:
                shutil.copy(_base_map, os.path.join(_bm_save_path, js_num_outplan['bmUrl']))

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


def base_map_add(cb1_path, floor, bm_path, user_path, _indoor_delete):
    '''
    模模搭底图加载，有两种情况：1）是制作模型时，层与层结构差异较大，需要删除墙体、地板等要素；
    2）修改模型时，需要更换底图，但是不能删除要素。
    :param cb1_path:
    :param floor:
    :param bm_path:
    :param user_path:
    :param _indoor_delete: 控制是否删除场景要素的选项
    :return:
    '''
    cfo = Cb1Operation(cb1_path)
    jbm = JsonBaseMap(cfo.json_extract())
    if _indoor_delete:
        jbm.indoor_features_delete(floor)
    jbm.indoor_map_add(floor, bm_path, user_path)
    jbm.json_scene_save()
    cfo.cb1_create('{}_basemap.cb1'.format(cb1_path.split('\\')[-1].replace('.cb1', '')))

# # cb1 operation
# class Cb1Operation(object):
#
#     def __init__(self, _cb1_path):
#         self._cb1_name = _cb1_path.split('\\')[-1]
#         # self._cb1_folder = _cb1_path.replace('\\' + self._cb1_name, '')  # error
#         self._cb1_folder = os.path.split(_cb1_path,)[0]
#         self._cb1_path = _cb1_path
#
#         self._zip_path = os.path.join(self._cb1_folder, self._cb1_name.replace('.cb1', '.zip'))
#         self._zip_folder = os.path.join(self._cb1_folder, self._cb1_name.replace('.cb1', ''))
#         self._custom_folder = os.path.join(self._zip_folder, 'CustomModel')
#
#     def json_extract(self):
#
#         if os.path.exists(self._zip_folder):
#             shutil.rmtree(self._zip_folder)
#
#         if os.path.exists(self._zip_path):
#             os.remove(self._zip_path)
#
#         shutil.copyfile(self._cb1_path, self._zip_path)
#
#         temp_zip = zipfile.ZipFile(self._zip_path)
#         for file in temp_zip.namelist():
#             temp_zip.extract(file, self._zip_folder)
#         temp_zip.close()
#
#         os.remove(self._zip_path)
#
#         os.chdir(self._zip_folder)
#
#         shutil.copy('scene.json', 'scene_backup.json')
#         os.remove('scene.json')
#         return os.path.join(self._zip_folder, 'scene_backup.json')
#
#     def model_folder_delete(self, *_model_id):
#
#         if os.path.exists(self._custom_folder):
#             os.chdir(self._custom_folder)
#             _files = os.listdir(self._custom_folder)
#             for mi in _model_id:
#                 if mi in _files:
#                     shutil.rmtree(os.path.join(self._custom_folder, mi))
#             _files = os.listdir(self._custom_folder)
#             if len(_files) == 0:
#                 os.chdir(self._cb1_folder)
#                 shutil.rmtree(self._custom_folder)
#
#     def cb1_create(self, _cb1_name=None, _cb1_folder=None):
#         _cb1_name = _cb1_name if _cb1_name else self._cb1_name.replace('.cb1', '_modify.cb1')
#         _folder = _cb1_folder if _cb1_folder else self._cb1_folder
#         _cb1_path = os.path.join(_folder, _cb1_name)
#         os.chdir(self._zip_folder)
#         _files = os.listdir(self._zip_folder)
#         print(_files)
#         if 'scene.json' in _files:
#             _zip = zipfile.ZipFile(self._zip_path, 'w', zipfile.ZIP_DEFLATED)
#             # for _file in _files:
#             #     if _file != 'scene_backup.json':
#             #         _zip.write(_file)
#             for root, dirs, files in os.walk(self._zip_folder):
#                 _file_path = root.replace(self._zip_folder, '')
#                 for file in files:
#                     if file != 'scene_backup.json':
#                         _zip.write(os.path.join(root, file), os.path.join(_file_path, file))
#             _zip.close()
#             shutil.copy(self._zip_path, _cb1_path)
#             os.remove(self._zip_path)
#             # Delete the temp folder
#             try:
#                 os.chdir(self._cb1_folder)
#                 shutil.rmtree(self._zip_folder)
#             except(IOError):
#                 print('Error Info:' + IOError)
#             print('The cb1 was created.')
#         else:
#             print('Error: There is no scene.json file.')
