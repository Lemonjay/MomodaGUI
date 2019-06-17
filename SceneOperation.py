#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import os
import json
from PackageOperation import *


def bidx_value_got(_key, _dict, _dict_target):
    '''
    将bidx的value 改成目标json bidx项的value
    :param _key:
    :param _dict:
    :param _dict_target:
    :return:
    '''
    _key_target = ''
    for kt in _dict_target.keys():
        if _dict_target[kt] == _dict[_key]:
            _key_target = kt
    return _key_target


# class JsonIdCoding(object):
#     '''
#     Momoda 室内楼层场景内要素自定义编码
#     '''
#     # 记录每个函数项，dict项的末位编码
#     id_dict = {}
#     corners_dict = {}
#
#     def __init__(self, _json_scene):
#         self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
#         with open(_json_scene, 'rb') as js:
#             self.js_dict = json.loads(js.read())
#             self.js_bds = self.js_dict['objects']['0']['bds']
#             if len(list(self.js_bds.keys())) == 1:
#                 print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
#                 self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']
#
#     # 1.起始plans_num 编码，假设一层场景的要素不超过10000个要素，起始楼层编码‘楼层数 + '0001'
#     # 2.地上部分+‘0001’,地下部分 + ‘00001’
#     # 3.一旦修改过一次id后，修改后再次赋值，会出现编码性错误
#     def plans_num_coding(self, _start_code):  # _start_code 的初始值可以是'0001'或'00001'
#         print('plans num coding')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             js_num_plans = self.js_plans[np]
#             # print(js_num_plans['uid'][0])
#             # np_new = js_num_plans['uid'][1:] + _start_code
#             np_new = js_num_plans['name'][1:] + _start_code
#             print('old item: {0} - new item: {1}'.format(np, np_new))
#             self.js_plans[np_new] = self.js_plans.pop(np)
#             # self.js_plans.pop(np)
#
#         print('new item lists: {0}'.format(list(self.js_plans.keys())))
#
#     def plcs_num_coding(self):
#         print('plcs num coding')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             _num = int(np)
#             js_num_plans = self.js_plans[np]
#             js_plcs = js_num_plans['plcs']
#             for npls in list(js_plcs.keys()):
#                 _num += 1
#                 js_plcs[str(_num)] = js_plcs.pop(npls)
#                 # print('old item: {0} - new item: {1}'.format(npls, str(_num)))
#                 self.id_dict[np] = str(_num)
#         print('The max value of ID code: {}'.format(self.id_dict))
#
#     def clds_num_coding(self):
#         print('clds num coding')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             js_num_plans = self.js_plans[np]
#             js_plcs = js_num_plans['plcs']
#             _num = int(self.id_dict[np])
#             for npls in list(js_plcs.keys()):
#                 js_num_plcs = js_plcs[npls]
#                 if 'clds' in list(js_num_plcs.keys()):
#                     js_clds = js_num_plcs['clds']
#                     for ncls in list(js_clds.keys()):
#                         _num += 1
#                         js_clds[str(_num)] = js_clds.pop(ncls)
#                         # print('old item: {0} - new item: {1}'.format(ncls, str(_num)))
#                         self.id_dict[np] = str(_num)
#         print('The max value of ID code: {}'.format(self.id_dict))
#
#     # 1.暂且不知道 Corners 是什么，对corners进行编码会出现错误，场景无法打开。
#     # 2.通过只有墙体的简单场景测试后知道，Corners：空间点位（角落） ，与Walls墙体有关 ‘sId’和‘eId’有关，startId 和 endId
#     # 3.测试了room,dws和 plcs 项,corners只与walls墙体有关
#     def corners_num_coding(self):
#         print('corners num coding')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             js_num_plans = self.js_plans[np]
#             js_corners = js_num_plans['corners']
#             _num = int(self.id_dict[np])
#             _temp_dict = {}
#             for ncor in list(js_corners.keys()):
#                 _num += 1
#                 js_corners[str(_num)] = js_corners.pop(ncor)
#                 # print('old item: {0} - new item: {1}'.format(ncor, str(_num)))
#                 self.id_dict[np] = str(_num)
#                 _temp_dict.update({'{}'.format(ncor): '{}'.format(str(_num))})
#             self.corners_dict[np] = _temp_dict
#         print('The max value of ID code: {}'.format(self.id_dict))
#         print('origin code and new code: {}'.format(self.corners_dict))
#
#     # sid和eid的值与corners的id有关，所以重新修改后的corners，需要将对应的id值填入walls的子项sid和eid值中
#     # corners的id修改了，必须要运行该函数
#     def walls_sid_eid_modify(self):
#         print('walls start and end value change')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             js_num_plans = self.js_plans[np]
#             js_walls = js_num_plans['walls']
#             _temp_dict = self.corners_dict[np]
#             for nw in list(js_walls.keys()):
#                 js_num_walls = js_walls[nw]
#                 # sId modify
#                 _walls_sid = js_num_walls['sId']
#                 js_num_walls['sId'] = _temp_dict[_walls_sid]
#                 # eId modify
#                 _walls_eid = js_num_walls['eId']
#                 js_num_walls['eId'] = _temp_dict[_walls_eid]
#                 # print('sId: {0} - eId: {1}'.format(js_num_walls['sId'], js_num_walls['eId']))
#
#     def walls_num_coding(self):
#         print('walls num coding')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             _num = int(self.id_dict[np])
#             js_num_plans = self.js_plans[np]
#             js_walls = js_num_plans['walls']
#             for nw in list(js_walls.keys()):
#                 _num += 1
#                 js_walls[str(_num)] = js_walls.pop(nw)
#                 # print('old item: {0} - new item: {1}'.format(nw, str(_num)))
#                 self.id_dict[np] = str(_num)
#         print('The max value of ID code: {}'.format(self.id_dict))
#
#     def dws_num_coding(self):
#         print('dws num coding')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             _num = int(self.id_dict[np])
#             js_num_plans = self.js_plans[np]
#             js_walls = js_num_plans['walls']
#             for nw in list(js_walls.keys()):
#                 js_num_walls = js_walls[nw]
#                 if 'dws' in list(js_num_walls.keys()):
#                     js_dws = js_num_walls['dws']
#                     for ndw in list(js_dws.keys()):
#                         _num += 1
#                         js_dws[str(_num)] = js_dws.pop(ndw)
#                         # print('old item: {0} - new item: {1}'.format(ndw, str(_num)))
#                         self.id_dict[np] = str(_num)
#         print('The max value of ID code: {}'.format(self.id_dict))
#
#     def rooms_num_coding(self):
#         print('rooms num coding')
#         np_lists = list(self.js_plans.keys())
#         for np in np_lists:
#             js_num_plans = self.js_plans[np]
#             js_rooms = js_num_plans['rooms']
#             _num = int(self.id_dict[np])
#             for nr in list(js_rooms.keys()):
#                 _num += 1
#                 js_rooms[str(_num)] = js_rooms.pop(nr)
#                 # print('old item: {0} - new item: {1}'.format(nr, str(_num)))
#                 self.id_dict[np] = str(_num)
#         print('The max value of ID code: {}'.format(self.id_dict))
#
#     # main function execute
#     def coding_main_execute(self):
#         # 1.首先用大的编码，跳过重复编码段
#         self.plans_num_coding('111100001')
#         self.plcs_num_coding()
#         try:
#             self.clds_num_coding()
#         except:
#             print('There were no clds keys.')
#         self.corners_num_coding()
#         self.walls_sid_eid_modify()
#         self.walls_num_coding()
#         self.dws_num_coding()
#         self.rooms_num_coding()
#
#         # 2.再用普通编码重写现在的编码
#         self.id_dict = {}
#         self.corners_dict = {}
#         self.plans_num_coding('0001')  # 一般单楼层的要素不超过10000个，超过1万个，增加字符创的个数，譬如‘00001’
#         self.plcs_num_coding()
#         try:
#             self.clds_num_coding()
#         except:
#             print('There were no clds keys.')
#         self.corners_num_coding()
#         self.walls_sid_eid_modify()
#         self.walls_num_coding()
#         self.dws_num_coding()
#         self.rooms_num_coding()
#
#     # save scene json
#     def json_scene_save(self, _json_name=None):
#         _json_file = _json_name if _json_name else 'scene.json'
#         js_str = json.dumps(self.js_dict, indent=4)
#         os.chdir(self._json_folder)
#         with open(_json_file, 'w') as js:
#             js.write(js_str)
class JsonIdCoding(object):
    # 记录每个函数项，dict项的末位编码
    id_dict = {}
    corners_dict = {}

    # js_dict = {}

    def __init__(self, _json_scene):
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            self.js_bds = self.js_dict['objects']['0']['bds']
            if len(list(self.js_bds.keys())) == 1:
                print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']

    # 1.起始plans_num 编码，假设一层场景的要素不超过10000个要素，起始楼层编码‘楼层数 + '0001'
    # 2.地上部分+‘0001’,地下部分 + ‘00001’
    # 3.一旦修改过一次id后，修改后再次赋值，会出现编码性错误
    def plans_num_coding(self, _start_code, _building_abbre=None):  # _start_code 的初始值可以是'0001'或'00001'
        print('plans num coding')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            np_new = _floor[1:] + _start_code
            _key = _building_abbre + _floor[0] + np_new if _building_abbre else np_new
            print('old item: {0} - new item: {1}'.format(np, np_new))
            self.js_plans[_key] = self.js_plans.pop(np)
            # self.js_plans.pop(np)

        print('new item lists: {0}'.format(list(self.js_plans.keys())))

    def plcs_num_coding(self, _building_abbre=None):
        print('plcs num coding')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            _abbre_len = len(_building_abbre) + 1 if _building_abbre else 0
            _num = int(np[_abbre_len:])
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            for npls in list(js_plcs.keys()):
                _num += 1
                _key = _building_abbre + _floor[0] + str(_num) if _building_abbre else str(_num)
                js_plcs[_key] = js_plcs.pop(npls)
                # print('old item: {0} - new item: {1}'.format(npls, str(_num)))
                self.id_dict[np] = str(_num)
        print('The max value of ID code: {}'.format(self.id_dict))

    def clds_num_coding(self, _building_abbre=None):
        print('clds num coding')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_plcs = js_num_plans['plcs']
            _num = int(self.id_dict[np])
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]
                if 'clds' in list(js_num_plcs.keys()):
                    js_clds = js_num_plcs['clds']
                    for ncls in list(js_clds.keys()):
                        _num += 1
                        _key = _building_abbre + _floor[0] + str(_num) if _building_abbre else str(_num)
                        js_clds[_key] = js_clds.pop(ncls)
                        # print('old item: {0} - new item: {1}'.format(ncls, str(_num)))
                        self.id_dict[np] = str(_num)
        print('The max value of ID code: {}'.format(self.id_dict))

    # 1.暂且不知道 Corners 是什么，对corners进行编码会出现错误，场景无法打开。
    # 2.通过只有墙体的简单场景测试后知道，Corners：空间点位（角落） ，与Walls墙体有关 ‘sId’和‘eId’有关，startId 和 endId
    # 3.测试了room,dws和 plcs 项,corners只与walls墙体有关
    def corners_num_coding(self, _building_abbre=None):
        print('corners num coding')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_corners = js_num_plans['corners']
            _num = int(self.id_dict[np])
            _temp_dict = {}
            for ncor in list(js_corners.keys()):
                _num += 1
                _key = _building_abbre + _floor[0] + str(_num) if _building_abbre else str(_num)
                js_corners[_key] = js_corners.pop(ncor)
                # print('old item: {0} - new item: {1}'.format(ncor, str(_num)))
                self.id_dict[np] = str(_num)
                _temp_dict.update({'{}'.format(ncor): '{}'.format(_key)})
            self.corners_dict[np] = _temp_dict
        print('The max value of ID code: {}'.format(self.id_dict))
        print('origin code and new code: {}'.format(self.corners_dict))

    # sid和eid的值与corners的id有关，所以重新修改后的corners，需要将对应的id值填入walls的子项sid和eid值中
    # corners的id修改了，必须要运行该函数
    def walls_sid_eid_modify(self, _building_abbre=None):
        print('walls start and end value change')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            js_walls = js_num_plans['walls']
            _temp_dict = self.corners_dict[np]
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                # sId modify
                _walls_sid = js_num_walls['sId']
                js_num_walls['sId'] = _temp_dict[_walls_sid]
                # eId modify
                _walls_eid = js_num_walls['eId']
                js_num_walls['eId'] = _temp_dict[_walls_eid]
                # print('sId: {0} - eId: {1}'.format(js_num_walls['sId'], js_num_walls['eId']))

    def walls_num_coding(self, _building_abbre=None):
        print('walls num coding')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            _num = int(self.id_dict[np])
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                _num += 1
                _key = _building_abbre + _floor[0] + str(_num) if _building_abbre else str(_num)
                js_walls[_key] = js_walls.pop(nw)
                # print('old item: {0} - new item: {1}'.format(nw, str(_num)))
                self.id_dict[np] = str(_num)
        print('The max value of ID code: {}'.format(self.id_dict))

    def dws_num_coding(self, _building_abbre=None):
        print('dws num coding')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            _num = int(self.id_dict[np])
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_walls = js_num_plans['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for ndw in list(js_dws.keys()):
                        _num += 1
                        _key = _building_abbre + _floor[0] + str(_num) if _building_abbre else str(_num)
                        js_dws[_key] = js_dws.pop(ndw)
                        # print('old item: {0} - new item: {1}'.format(ndw, str(_num)))
                        self.id_dict[np] = str(_num)
        print('The max value of ID code: {}'.format(self.id_dict))

    def rooms_num_coding(self, _building_abbre=None):
        print('rooms num coding')
        np_lists = list(self.js_plans.keys())
        for np in np_lists:
            js_num_plans = self.js_plans[np]
            _floor = js_num_plans['uid']
            js_rooms = js_num_plans['rooms']
            _num = int(self.id_dict[np])
            for nr in list(js_rooms.keys()):
                _num += 1
                _key = _building_abbre + _floor[0] + str(_num) if _building_abbre else str(_num)
                js_rooms[_key] = js_rooms.pop(nr)
                # print('old item: {0} - new item: {1}'.format(nr, str(_num)))
                self.id_dict[np] = str(_num)
        print('The max value of ID code: {}'.format(self.id_dict))

    # main function execute
    def coding_main_execute(self, _building_abbre=None):
        # 1.首先用大的编码，跳过重复编码段
        self.plans_num_coding('111100001', _building_abbre)
        self.plcs_num_coding(_building_abbre)
        try:
            self.clds_num_coding(_building_abbre)
        except:
            print('There were no clds keys.')
        self.corners_num_coding(_building_abbre)
        self.walls_sid_eid_modify(_building_abbre)
        self.walls_num_coding(_building_abbre)
        self.dws_num_coding(_building_abbre)
        self.rooms_num_coding(_building_abbre)

        # 2.再用普通编码重写现在的编码
        self.id_dict = {}
        self.corners_dict = {}
        self.plans_num_coding('0001', _building_abbre)  # 一般单楼层的要素不超过10000个，超过1万个，增加字符创的个数，譬如‘00001’
        self.plcs_num_coding(_building_abbre)
        try:
            self.clds_num_coding(_building_abbre)
        except:
            print('There were no clds keys.')
        self.corners_num_coding(_building_abbre)
        self.walls_sid_eid_modify(_building_abbre)
        self.walls_num_coding(_building_abbre)
        self.dws_num_coding(_building_abbre)
        self.rooms_num_coding(_building_abbre)

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


class MmdSceneOperation(object):
    '''
    因为Momoda建模多人合作的原因，需要将两个两栋建筑进行拼接场景拼接，在Momoda中调整好两个建筑的位置，进而进行楼层的拼接
        1.两个场景拼接，求两个场景的bIdList的并集，并对其中一个场景进行bidx进行修改
        2.将另一个场景与目标场景进行合并
        3.因为解决了底图配准的问题，合作分工建模，拼接已经不再是问题，因为位置是统一的，所以不需要在Momoda里面调整位置，直接进行楼层的拼接
    '''
    js_plans = {}

    def __init__(self, _json_scene):
        '''
        对于只有一个室内建筑场景
        :param _json_scene:
        '''
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            self.js_bds = self.js_dict['objects']['0']['bds']
            if len(list(self.js_bds.keys())) == 1:  # 判断bds项是否只有一项
                print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']
            else:
                print('The Scene has {} buildings.'.format(len(list(self.js_bds.keys()))))

    def bidlist_merge(self, _target_json):
        '''
        # 以_target_json的bIdList顺序为基础，求两个json的bIdList并集，
        # 替换掉_json_scene中的bIdLists
        :param _target_json:
        :return:
        '''
        tj_lists = []
        with open(_target_json, 'rb') as tj:
            tj_dict = json.loads(tj.read())
            for _list in self.js_dict['bIdList']:
                tj_lists = tj_dict['bIdList']
                if _list not in tj_lists:
                    tj_lists.append(_list)
                    # print(_list)
        # print(tj_lists)
        return tj_lists

    def bidx_value_dict(self, _target_lists=None):
        '''
        # 根据上述self.js_dict['bIdList']，生成对应的bidx_value字典
        :param _target_lists:
        :return:
        '''
        # 确定"bIdx"元素类型，创建字典
        _bidx_dict = {}
        _temp_lists = _target_lists if _target_lists else self.js_dict['bIdList']
        for i in range(len(_temp_lists)):
            # print('{0}  {1}'.format(i, json_bidx[i][2]))
            _bidx_dict.update({str(i): _temp_lists[i][0]})  # 模型名称会重复，需要用模型id
        # print(_bidx_dict)
        return _bidx_dict

    # plcs_bidx modify
    def plcs_bidx_modify(self, _target_json):
        for np in self.js_plans.keys():
            js_plcs = self.js_plans[np]['plcs']
            for npls in list(js_plcs.keys()):
                js_num_plcs = js_plcs[npls]

                # _bidx_lists 需要统计后手动分类
                if 'bIdx' in list(js_num_plcs.keys()):
                    _bidx_value = str(js_num_plcs['bIdx'])
                    js_num_plcs['bIdx'] = bidx_value_got(_bidx_value, self.bidx_value_dict(),
                                                         self.bidx_value_dict(self.bidlist_merge(_target_json)))

                # 'clds' 项
                elif 'clds' in js_num_plcs.keys():
                    # print('true')
                    js_clds = js_num_plcs['clds']
                    for ncls in list(js_clds.keys()):
                        js_num_clds = js_clds[ncls]
                        if 'bIdx' in list(js_num_clds.keys()):
                            _bidx_value = str(js_num_clds['bIdx'])
                            js_num_clds['bIdx'] = bidx_value_got(_bidx_value, self.bidx_value_dict(),
                                                                 self.bidx_value_dict(self.bidlist_merge(_target_json)))

    # walls_bidx modify
    def walls_bidx_modify(self, _target_json):
        for np in self.js_plans.keys():
            js_walls = self.js_plans[np]['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'bIdx' in list(js_num_walls.keys()):  # 玻璃墙，插入的物体是‘bIdx’项
                    _bidx_value = str(js_num_walls['bIdx'])
                    js_num_walls['bIdx'] = bidx_value_got(_bidx_value, self.bidx_value_dict(),
                                                          self.bidx_value_dict(self.bidlist_merge(_target_json)))
                elif 'rBIdx' in list(js_num_walls.keys()):  # 墙纸贴图，右墙
                    _bidx_value = str(js_num_walls['rBIdx'])
                    js_num_walls['rBIdx'] = bidx_value_got(_bidx_value, self.bidx_value_dict(),
                                                           self.bidx_value_dict(self.bidlist_merge(_target_json)))
                elif 'lBIdx' in list(js_num_walls.keys()):  # 墙纸贴图，左墙
                    _bidx_value = str(js_num_walls['lBIdx'])
                    js_num_walls['lBIdx'] = bidx_value_got(_bidx_value, self.bidx_value_dict(),
                                                           self.bidx_value_dict(self.bidlist_merge(_target_json)))

    def dws_bidx_modify(self, _target_json):
        '''
        # 在momoda中，门，消火栓（部分），窗，防火卷帘是嵌进墙里面的，
        # 通过bIdLists对应的模型Id对dws项进行统一'bIdx'值的修改
        :param _target_json:
        :return:
        '''
        for np in self.js_plans.keys():
            js_walls = self.js_plans[np]['walls']
            for nw in list(js_walls.keys()):
                js_num_walls = js_walls[nw]
                if 'dws' in list(js_num_walls.keys()):
                    js_dws = js_num_walls['dws']
                    for nd in list(js_dws.keys()):
                        # dws_number项
                        js_num_dws = js_dws[nd]
                        if 'bIdx' in js_num_dws.keys():
                            _bidx_value = str(js_num_dws['bIdx'])
                            js_num_dws['bIdx'] = int(bidx_value_got(_bidx_value, self.bidx_value_dict(),
                                                                    self.bidx_value_dict(
                                                                        self.bidlist_merge(_target_json))))

    def rooms_bidx_modify(self, _target_json):
        '''
        # 对"room_num"子项的 floor,ceiling,hceiling,roof 子项的bIdx的value进行修改
        :param _target_json:
        :return:
        '''
        for np in list(self.js_plans.keys()):
            js_rooms = self.js_plans[np]['rooms']
            for nr in js_rooms.keys():
                js_num_rooms = js_rooms[nr]

                # floor,ceiling,hceiling,roof 的bidx的value修改
                for _sr in ['floor', 'ceiling', 'hceiling', 'roof']:
                    js_subset = js_num_rooms[_sr]
                    if 'bIdx' in js_subset.keys():
                        _bidx_value = str(js_subset['bIdx'])
                        js_subset['bIdx'] = int(bidx_value_got(_bidx_value, self.bidx_value_dict(),
                                                               self.bidx_value_dict(self.bidlist_merge(_target_json))))

    def scene_bds_merge(self, _target_json):
        '''
        # execute main function
        # 在“bds”项上添加新的建筑，两个建筑场景合并
        :param _target_json:
        :return:
        '''
        self.plcs_bidx_modify(_target_json)
        self.walls_bidx_modify(_target_json)
        self.dws_bidx_modify(_target_json)
        self.rooms_bidx_modify(_target_json)
        # 最后修改一下bIdList
        self.js_dict['bIdList'] = self.bidlist_merge(_target_json)
        print(self.bidlist_merge(_target_json))

        with open(_target_json, 'rb') as tj:
            tj_dict = json.loads(tj.read())
            tj_bds = tj_dict['objects']['0']['bds']
            for nb in tj_bds.keys():
                if nb in self.js_bds.keys():
                    self.js_bds[nb + '01'] = tj_bds[nb]
                else:
                    self.js_bds[nb] = tj_bds[nb]

    def floor_plans_merge(self):
        '''
        楼层“js_num_plans” 合并
        :return:
        '''
        js_num_bds = self.js_bds[list(self.js_bds.keys())[0]]  # bds项中以第一个num项为target项
        js_target_plans = js_num_bds['plans']
        _floor_lists = list(js_target_plans.keys())
        for nb in list(self.js_bds.keys()):
            if nb != list(self.js_bds.keys())[0]:
                js_plans = self.js_bds[nb]['plans']
                for np in list(js_plans.keys()):
                    if np in _floor_lists:
                        js_target_plans[np + '001'] = js_plans[np]
                    else:
                        js_target_plans[np] = js_plans[np]
                # 删除 bds_num 项
                self.js_bds.pop(nb)

    def floor_offset_modify(self):
        def floor_list_sort(_list):
            list_part01 = []
            list_part02 = []
            for l in _list:
                if 'b' in l:
                    list_part01.append(l)
                else:
                    list_part02.append(l)

            list_part01.sort(key=lambda x: int(x[1:]), reverse=True)
            list_part02.sort(key=lambda x: int(x[1:]))
            return list_part01 + list_part02

        _floor_list = []
        js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']
        for np in list(js_plans.keys()):
            js_num_plans = js_plans[np]
            _floor_list.append(js_num_plans['uid'])
        _floor_list = floor_list_sort(_floor_list)
        print(_floor_list)

        for i in range(len(_floor_list)):
            for np in list(js_plans.keys()):
                js_num_plans = js_plans[np]
                if js_num_plans['uid'] == _floor_list[i]:
                    if i == 0:
                        try:
                            js_num_plans.pop('offset')
                        except:
                            print('No offset key ')
                    else:
                        js_num_plans['offset'] = round(float(3 * i), 3)

                    try:
                        bm_1st = js_num_plans['bmCenter'].split(' ')[0]
                        bm_3rd = js_num_plans['bmCenter'].split(' ')[2]
                        js_num_plans['bmCenter'] = '{0} {1} {2}'.format(bm_1st, round((3 * i + 0.100), 3), bm_3rd)
                    except:
                        print('No bmCenter key ')

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


class FloorPlansSort(object):
    def __init__(self, _json_scene):
        self._json_folder = _json_scene.replace('\\{}'.format(_json_scene.split('\\')[-1]), '')
        with open(_json_scene, 'rb') as js:
            self.js_dict = json.loads(js.read())
            self.js_bds = self.js_dict['objects']['0']['bds']
            if len(list(self.js_bds.keys())) == 1:
                print('bulding id: {}'.format(list(self.js_bds.keys())[0]))
                self.js_plans = self.js_bds[list(self.js_bds.keys())[0]]['plans']

    # plans sort
    def plans_sort(self, _building_abbre=None):
        def floor_list_sort(_list, _building_abbre):
            list_part01 = []
            list_part02 = []
            for l in _list:
                if 'b' in l[len(_building_abbre):]:
                    list_part01.append(l)
                else:
                    list_part02.append(l)

            list_part01.sort(key=lambda x: int(x[len(_building_abbre) + 1:]), reverse=True)
            list_part02.sort(key=lambda x: int(x[len(_building_abbre) + 1:]))
            return list_part01 + list_part02

        js_plans = self.js_plans.copy()  # 字典的copy和赋值是不一样的
        _keys = floor_list_sort(list(js_plans.keys()), _building_abbre)
        print('plans sort', _keys)
        for _key in _keys:
            self.js_plans.pop(_key)
        for _key in _keys:
            self.js_plans[_key] = js_plans[_key]

    # save scene json
    def json_scene_save(self, _json_name=None):
        _json_file = _json_name if _json_name else 'scene.json'
        js_str = json.dumps(self.js_dict, indent=4)
        os.chdir(self._json_folder)
        with open(_json_file, 'w') as js:
            js.write(js_str)


def floor_two_merge(_cb1, _cb1_target, _coding_abbre, _cb1_name='temp.cb1'):
    '''
    楼层合并，只限2层
    :param _cb1:
    :param _cb1_target:
    :param _coding_abbre:
    :param _cb1_name:
    :return:
    '''
    _js = Cb1Operation(_cb1)
    _js_target = Cb1Operation(_cb1_target)
    _js_path = _js.json_extract()  # _js_path 是路径字符串，而_js.json_extract()是经过计算后得到的返回值
    _mso = MmdSceneOperation(_js_path)
    _mso.scene_bds_merge(_js_target.json_extract())
    _mso.floor_plans_merge()
    _mso.floor_offset_modify()
    _mso.json_scene_save('scene_backup.json')

    # 字典重新排序
    _jic = JsonIdCoding(_js_path)
    _jic.coding_main_execute(_coding_abbre)
    _jic.json_scene_save('scene_backup.json')

    # Plans 排序
    fps = FloorPlansSort(_js_path)
    fps.plans_sort(_coding_abbre)
    fps.json_scene_save()

    # 生成cb1文件
    _js.cb1_create(_cb1_name)
    _js_target.cb1_create()


def building_floor_merge(_cb1_files, _cb1_target_path, _coding_abbre):
    '''
    楼层合并，2层及2层以上的多楼层合并函数
    :param _cb1_files:
    :param _cb1_target_path:
    :param _coding_abbre:
    :return:
    '''
    if len(_cb1_files) == 1 or len(_cb1_files) == 0:
        print('当前不需要进行楼层合并（floor merge）')
    else:
        _temp = _cb1_files[0]
        _temp_folder = os.path.split(_temp)[0]
        for _fl in _cb1_files:
            if _temp != _fl:
                floor_two_merge(_temp, _fl, _coding_abbre)
                _temp = os.path.join(_temp_folder, 'temp.cb1')
        shutil.copy(_temp, _cb1_target_path)
        os.remove(_temp)


def model_id_recoding(_cb1_files, _coding_abbre, _cb1_folder):
    '''
    场景中模型重新编码
    :param _cb1_files:
    :param _coding_abbre:
    :param _cb1_folder:
    :return:
    '''
    for fl in _cb1_files:
        _js = Cb1Operation(fl)
        _js_path = _js.json_extract()

        _jic = JsonIdCoding(_js_path)
        _jic.coding_main_execute(_coding_abbre)
        _jic.json_scene_save()

        _js.cb1_create(_cb1_folder=_cb1_folder)
