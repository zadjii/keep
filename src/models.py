from common import *
from json import JSONEncoder

__author__ = 'zadjii'

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  

class DirectoryModel(object):
    """docstring for DirectoryModel"""
    def __init__(self, path=''):
        super(DirectoryModel, self).__init__()
        self.path = path
        self.id = INVALID_ID
        self.name = ''
        self.notes = []

    def serialize(self):
        # self_box = Box(self)
        # return self_box.to_json()
        return json.dumps(self.__dict__, cls=MyEncoder)

    @staticmethod
    def deserialize(json_dict):
        obj = DirectoryModel()
        obj.path = json_dict['path']
        obj.id = json_dict['id']
        obj.name = json_dict['name']
        obj.notes = json_dict['notes']
        return obj

class WorkspaceModel(object):
    """docstring for WorkspaceModel"""
    def __init__(self, root=''):
        super(WorkspaceModel, self).__init__()
        self.root = root
        self.id = INVALID_ID
        self.name = ''
        self.notes = []
        self.dirs = []

    def serialize(self):
        # self_box = Box(self.__dict__, box_it_up=True)
        # return self_box.to_json()
        return json.dumps(self.__dict__, cls=MyEncoder)

    @staticmethod
    def deserialize(json_dict):
        obj = WorkspaceModel()

        obj.root = json_dict['root']
        obj.id = json_dict['id']
        obj.name = json_dict['name']
        obj.notes = json_dict['notes']
        obj.dirs = [DirectoryModel.deserialize(_dir) for _dir in json_dict['dirs']]
        return obj

class RootModel(object):
    """docstring for RootModel"""
    def __init__(self):
        super(RootModel, self).__init__()
        self.workspaces = []

    def serialize(self):
        return json.dumps(self.__dict__, cls=MyEncoder)
    
    @staticmethod
    def deserialize(json_dict):
        obj = RootModel()
        if 'workspaces' in json_dict.keys():
            obj.workspaces = [WorkspaceModel.deserialize(_dir) for _dir in json_dict['workspaces']]
        return obj

    def _next_workspace_id(self):
        next_id = 0
        for workspace in self.workspaces:
            if workspace.id >= next_id:
                next_id = workspace.id + 1
        return next_id

    def add_workspace(self, new_workspace):
        next_id = self._next_workspace_id()
        new_workspace.id = next_id
        self.workspaces.append(new_workspace)
