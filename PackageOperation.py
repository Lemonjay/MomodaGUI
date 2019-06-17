import os, re
import shutil
import zipfile


# cb1 文件操作
class Cb1Operation(object):

    def __init__(self, _cb1_path):
        self._cb1_path = _cb1_path
        self._cb1_name = os.path.split(_cb1_path)[1]
        self._cb1_folder = os.path.split(_cb1_path, )[0]
        self._zip_path = os.path.join(self._cb1_folder, self._cb1_name.replace('.cb1', '.zip'))
        self._zip_folder = os.path.join(self._cb1_folder, self._cb1_name.replace('.cb1', ''))
        self._custom_folder = os.path.join(self._zip_folder, 'CustomModel')

    def json_extract(self):
        '''
        'scene_backup.json' 文件生成,返回scene_backup.json 路径值
        :return:
        '''
        # # 删除zip文件夹
        # if os.path.exists(self._zip_folder):
        #     shutil.rmtree(self._zip_folder)

        # 删除已有的zip文件
        if os.path.exists(self._zip_path):
            os.remove(self._zip_path)

        # 复制cb1，修改后缀成.zip
        shutil.copyfile(self._cb1_path, self._zip_path)
        # 解压文件
        temp_zip = zipfile.ZipFile(self._zip_path)
        for file in temp_zip.namelist():
            temp_zip.extract(file, self._zip_folder)
        temp_zip.close()

        # 删除zip文件
        os.remove(self._zip_path)

        # 设置文件夹路径
        os.chdir(self._zip_folder)

        # 生成 'scene_backup.json' 文件
        shutil.copy('scene.json', 'scene_backup.json')
        os.remove('scene.json')
        return os.path.join(self._zip_folder, 'scene_backup.json')

    def model_folder_delete(self, *_model_id):
        '''
        自定义模型会存在cb1场景包中，因为要删除室外场景，场景包中自定义的模型有的是室内的，
        也有的是是室外的，如果只要删除室外的模型，需要跟据model id 删除指定的模型。
        :param _model_id: 模型的id 与文件夹的id相同
        :return:
        '''
        if os.path.exists(self._custom_folder):
            os.chdir(self._custom_folder)
            _files = os.listdir(self._custom_folder)
            for mi in _model_id:
                if mi in _files:
                    shutil.rmtree(os.path.join(self._custom_folder, mi))
            _files = os.listdir(self._custom_folder)
            if len(_files) == 0:
                os.chdir(self._cb1_folder)
                shutil.rmtree(self._custom_folder)

    def cb1_create(self, _cb1_name=None, _cb1_folder=None):
        '''
        压缩文件，改后缀'.zip'到'.cb1',生成cb1的场景包
        :param _cb1_name:
        :param _cb1_folder:
        :return:
        '''
        _cb1_name = _cb1_name if _cb1_name else self._cb1_name.replace('.cb1', '_modify.cb1')
        _folder = _cb1_folder if _cb1_folder else self._cb1_folder
        _cb1_path = os.path.join(_folder, _cb1_name)
        os.chdir(self._zip_folder)
        _files = os.listdir(self._zip_folder)
        print(_files)
        if 'scene.json' in _files:
            _zip = zipfile.ZipFile(self._zip_path, 'w', zipfile.ZIP_DEFLATED)
            # for _file in _files:
            #     if _file != 'scene_backup.json':
            #         _zip.write(_file)
            for root, dirs, files in os.walk(self._zip_folder):
                _file_path = root.replace(self._zip_folder, '')  # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                for file in files:
                    if file != 'scene_backup.json':
                        _zip.write(os.path.join(root, file), os.path.join(_file_path, file))
            _zip.close()
            shutil.copy(self._zip_path, _cb1_path)
            os.remove(self._zip_path)
            # Delete the temp folder
            os.chdir(self._cb1_folder)  # 这里只切换一下默认路径，为了能删除底下的‘self._zip_folder’文件夹
            shutil.rmtree(self._zip_folder)  # 因为os.chdir(self._zip_folder)在调用该文件夹，所以无法删除

            print('The cb1 was created.')
        else:
            # Delete the temp folder
            os.chdir(self._cb1_folder)
            shutil.rmtree(self._zip_folder)
            print('Error: There is no scene.json file.\n'
                  'The {} Folder was delete'.format(self._zip_folder))


# cb1 文件操作
class Cb1OperationModify(object):

    def __init__(self, _cb1_path):
        self._cb1_path = _cb1_path
        self._cb1_name = os.path.split(_cb1_path)[1]
        self._cb1_folder = os.path.split(_cb1_path, )[0]
        self._zip_path = os.path.join(self._cb1_folder, self._cb1_name.replace('.cb1', '.zip'))
        self._zip_folder = os.path.join(self._cb1_folder, self._cb1_name.replace('.cb1', ''))
        self._custom_folder = os.path.join(self._zip_folder, 'CustomModel')

    def cb1_extract(self):
        # 删除已有的zip文件
        if os.path.exists(self._zip_path):
            os.remove(self._zip_path)

        # 复制cb1，修改后缀成.zip
        shutil.copyfile(self._cb1_path, self._zip_path)
        # 解压文件
        temp_zip = zipfile.ZipFile(self._zip_path)
        for file in temp_zip.namelist():
            temp_zip.extract(file, self._zip_folder)
        temp_zip.close()

        # 删除zip文件
        os.remove(self._zip_path)
        return self._zip_folder

    def json_extract(self):
        '''
        'scene_backup.json' 文件生成,返回scene_backup.json 路径值
        :return:
        '''
        # 设置文件夹路径
        os.chdir(self._zip_folder)

        # 生成 'scene_backup.json' 文件
        shutil.copy('scene.json', 'scene_backup.json')
        os.remove('scene.json')
        return os.path.join(self._zip_folder, 'scene_backup.json')

    def model_folder_delete(self, *_model_id):
        '''
        自定义模型会存在cb1场景包中，因为要删除室外场景，场景包中自定义的模型有的是室内的，
        也有的是是室外的，如果只要删除室外的模型，需要跟据model id 删除指定的模型。
        :param _model_id: 模型的id 与文件夹的id相同
        :return:
        '''
        if os.path.exists(self._custom_folder):
            os.chdir(self._custom_folder)
            _files = os.listdir(self._custom_folder)
            for mi in _model_id:
                if mi in _files:
                    shutil.rmtree(os.path.join(self._custom_folder, mi))
            _files = os.listdir(self._custom_folder)
            if len(_files) == 0:
                os.chdir(self._cb1_folder)
                shutil.rmtree(self._custom_folder)

    def model_remainder_delete(self, model_id_lists):
        model_folder_lists = os.listdir(self._custom_folder)
        for id in model_folder_lists:
            if id not in model_id_lists:
                print(id)
                shutil.rmtree(os.path.join(self._custom_folder, id))

    def cb1_create(self, _cb1_name=None, _cb1_folder=None):
        '''
        压缩文件，改后缀'.zip'到'.cb1',生成cb1的场景包
        :param _cb1_name:
        :param _cb1_folder:
        :return:
        '''
        _cb1_name = _cb1_name if _cb1_name else self._cb1_name.replace('.cb1', '_modify.cb1')
        _folder = _cb1_folder if _cb1_folder else self._cb1_folder
        _cb1_path = os.path.join(_folder, _cb1_name)
        os.chdir(self._zip_folder)
        _files = os.listdir(self._zip_folder)
        print(_files)
        if 'scene.json' in _files:
            _zip = zipfile.ZipFile(self._zip_path, 'w', zipfile.ZIP_DEFLATED)
            # for _file in _files:
            #     if _file != 'scene_backup.json':
            #         _zip.write(_file)
            for root, dirs, files in os.walk(self._zip_folder):
                _file_path = root.replace(self._zip_folder, '')  # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                for file in files:
                    if file != 'scene_backup.json':
                        _zip.write(os.path.join(root, file), os.path.join(_file_path, file))
            _zip.close()
            shutil.copy(self._zip_path, _cb1_path)
            os.remove(self._zip_path)
            # Delete the temp folder
            os.chdir(self._cb1_folder)  # 这里只切换一下默认路径，为了能删除底下的‘self._zip_folder’文件夹
            shutil.rmtree(self._zip_folder)  # 因为os.chdir(self._zip_folder)在调用该文件夹，所以无法删除

            print('The cb1 was created.')
        else:
            # Delete the temp folder
            os.chdir(self._cb1_folder)
            shutil.rmtree(self._zip_folder)
            print('Error: There is no scene.json file.\n'
                  'The {} Folder was delete'.format(self._zip_folder))


def cb1_version_publish(cb1_files, building_abbre, _version, _folder):
    for fl in cb1_files:
        fl_name = os.path.split(fl)[1]
        print(fl_name)
        # floor_name = fl_name.replace(building_abbre, '').split('_')[1]
        floor_name = re.split('[_.]', fl_name.replace(building_abbre, ''))[1]
        print(floor_name)
        fl_new_name = '{0}_{1}_{2}.cb1'.format(building_abbre, floor_name, _version)
        fl_new_path = os.path.join(_folder, fl_new_name)
        shutil.copy(fl, fl_new_path)
