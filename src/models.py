from common import *
from json import JSONEncoder

__author__ = 'zadjii'

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class CommandModel(object):
    """docstring for CommandModel"""
    def __init__(self, command=''):
        super(CommandModel, self).__init__()
        self.command = command
        self.id = INVALID_ID
        self.name = ''
        self.notes = []

    def set_name(self, name):
        self.name = name

    def serialize(self):
        # self_box = Box(self)
        # return self_box.to_json()
        return json.dumps(self.__dict__, cls=MyEncoder, indent=4)

    @staticmethod
    def deserialize(json_dict):
        obj = CommandModel()
        obj.command = json_dict['command']
        obj.id = json_dict['id']
        obj.name = json_dict['name']
        obj.notes = json_dict['notes']
        return obj

    def to_list_string(self):
        if (self.name is not None) and not (self.name == ''):
            fmt = '{}\t{}\x1b[0m\t{}'
            return fmt.format(colorize_string(self.id, COMMAND_NUMBER_COLOR),
                              colorize_string(self.name, NAME_LABEL_COLOR),
                              self.command)
        else:
            fmt = '{}\t{}'
            return fmt.format(colorize_string(self.id, COMMAND_NUMBER_COLOR), self.command)


class DirectoryModel(object):
    """docstring for DirectoryModel"""
    def __init__(self, path=''):
        super(DirectoryModel, self).__init__()
        self.path = path
        self.id = INVALID_ID
        self.name = ''
        self.notes = []

    def set_name(self, name):
        self.name = name

    def serialize(self):
        # self_box = Box(self)
        # return self_box.to_json()
        return json.dumps(self.__dict__, cls=MyEncoder, indent=4)

    @staticmethod
    def deserialize(json_dict):
        obj = DirectoryModel()
        obj.path = json_dict['path']
        obj.id = json_dict['id']
        obj.name = json_dict['name']
        obj.notes = json_dict['notes']
        return obj

    def to_list_string(self):
        curr_path = normalize_path(os.getcwd())
        prefix = '*' if curr_path == self.path else ''
        id_str = colorize_string(self.id, DIRECTORY_NUMBER_COLOR)
        name = '{}\x1b[0m\t'.format(colorize_string(self.name, NAME_LABEL_COLOR)) if (self.name is not None) and not (self.name == '') else ''
        path = colorize_string(self.path, CURRENT_DIR_COLOR if curr_path == self.path else RESET_COLORS)
        return '{}{}\t{}{}'.format(prefix, id_str, name, path)


class WorkspaceModel(object):
    """docstring for WorkspaceModel"""
    def __init__(self, root='', _id=INVALID_ID, name=''):
        super(WorkspaceModel, self).__init__()
        self.root = root
        self.init = ''
        self.id = _id
        self.name = name
        self.notes = []
        self.dirs = []
        self.commands = []

    def serialize(self):
        # self_box = Box(self.__dict__, box_it_up=True)
        # return self_box.to_json()
        return json.dumps(self.__dict__, cls=MyEncoder, indent=4)

    @staticmethod
    def deserialize(json_dict):
        obj = WorkspaceModel()

        obj.root = json_dict['root']
        obj.init = json_dict['init'] if 'init' in json_dict else ''
        obj.id = json_dict['id']
        obj.name = json_dict['name']
        obj.notes = json_dict['notes']
        obj.dirs = [DirectoryModel.deserialize(_dir) for _dir in json_dict['dirs']] if 'dirs' in json_dict else []
        obj.commands = [CommandModel.deserialize(_cmd) for _cmd in json_dict['commands']] if 'commands' in json_dict else []
        return obj

    def _next_dir_id(self):
        next_id = FIRST_VALID_ID
        for _dir in self.dirs:
            if _dir.id >= next_id:
                next_id = _dir.id + 1
        return next_id

    def _next_cmd_id(self):
        next_id = FIRST_VALID_ID
        for _cmd in self.commands:
            if _cmd.id >= next_id:
                next_id = _cmd.id + 1
        return next_id

    def add_dir(self, new_dir):
        for _dir in self.dirs:
            if _dir.path == new_dir.path:
                return
        next_id = self._next_dir_id()
        new_dir.id = next_id
        self.dirs.append(new_dir)

    def add_cmd(self, new_cmd):
        for _cmd in self.commands:
            if _cmd.command == new_cmd.command:
                return
        next_id = self._next_cmd_id()
        new_cmd.id = next_id
        self.commands.append(new_cmd)

    def to_list_string(self):
        working_id = get_working_workspace()
        curr_path = normalize_path(os.getcwd())
        fmt = '*{}/\t\x1b[1;34m{}\t{}\x1b[0m' if working_id == self.id else '{}/\t{}\t{}'
        return fmt.format(self.id, self.name, self.root)

    def get_dir(self, dir_id):
        if dir_id == GLOBALS_ID:
            return DirectoryModel(self.root)
        else:
            for _dir in self.dirs:
                if dir_id == _dir.id:
                    return _dir
            return None

    def get_cmd(self, cmd_id):
        if cmd_id == GLOBALS_ID:
            return self.root
        else:
            for _cmd in self.commands:
                if cmd_id == _cmd.id:
                    return _cmd
            return None


class RootModel(object):
    """docstring for RootModel"""
    def __init__(self):
        super(RootModel, self).__init__()
        self.globals = WorkspaceModel('/', GLOBALS_ID, '<globals>')
        self.workspaces = []

    def serialize(self):
        return json.dumps(self.__dict__, cls=MyEncoder, indent=4)

    @staticmethod
    def deserialize(json_dict):
        obj = RootModel()
        if 'workspaces' in json_dict.keys():
            obj.workspaces = [WorkspaceModel.deserialize(_dir) for _dir in json_dict['workspaces']]
        if 'globals' in json_dict.keys():
            obj.globals = WorkspaceModel.deserialize(json_dict['globals'])
        return obj

    def _next_workspace_id(self):
        next_id = FIRST_VALID_ID
        for workspace in self.workspaces:
            if workspace.id >= next_id:
                next_id = workspace.id + 1
        return next_id

    def add_workspace(self, new_workspace):
        next_id = self._next_workspace_id()
        new_workspace.id = next_id
        self.workspaces.append(new_workspace)

    def get_workspace(self, workspace_id):
        if workspace_id == self.globals.id:
            return self.globals
        else:
            for workspace in self.workspaces:
                if workspace_id == workspace.id:
                    return workspace
            print('[{}] is not a valid workspace id.'.format(workspace_id))
            return None
