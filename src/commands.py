from common import *
from models import *
from backend import *

__author__ = 'zadjii'


###################################### keep ####################################
def keep(argv):

    new_dir_path = os.getcwd()
    if len(argv) == 1:
        new_dir_path = argv[0]
    new_dir_path = normalize_path(new_dir_path)

    root_model = load_backend()
    new_dir = DirectoryModel(new_dir_path)

    working_id = get_working_workspace()
    workspace = root_model.get_workspace(working_id)
    if workspace is not None:
        workspace.add_dir(new_dir)

    write_backend(root_model)
################################################################################

###################################### list ####################################
def _list_dirs(workspace):
    for _dir in workspace.dirs:
        print(_dir.to_list_string())

def _do_list_dirs(workspace):
    print(workspace.to_list_string())
    _list_dirs(workspace)

def _do_list(workspace):
    print(workspace.to_list_string())

    print(colorize_string('Directories:', DIRECTORIES_LABEL_COLOR))
    _list_dirs(workspace)

    print(colorize_string('Commands:', COMMANDS_LABEL_COLOR))
    _list_commands(workspace)

def list_workspace(argv):
    root_model = load_backend()
    working_id = get_working_workspace()
    workspace = root_model.get_workspace(working_id)
    if workspace is not None:
        _do_list(workspace)
    else:
        print('This is an unexpected error. If there is no active workspace, '
              'you should be given the globals.')

    write_backend(root_model)
################################################################################

####################################### go #####################################
def _do_go(workspace, dir_id):
    dir_model = workspace.get_dir(dir_id)
    if dir_model is not None:
        print(dir_model.path)
    else:
        print('.')
        print("")
        print('Directory {} is not in the current workspace({})'.format(dir_id, workspace.id))
    # print(workspace.root)


def go(argv):

    root_model = load_backend()
    working_id = get_working_workspace()
    workspace = root_model.get_workspace(working_id)

    if workspace is not None:
        if len(argv) == 0:
            _do_list_dirs(workspace)
            sys.exit()
        elif len(argv) == 1:
            dir_id = int(argv[0])
            _do_go(workspace, dir_id)
    else:
        print('This is an unexpected error. If there is no active workspace, '
              'you should be given the globals.')
################################################################################

###################################### stash ###################################
def _list_commands(workspace):
    for _cmd in workspace.commands:
        print(_cmd.to_list_string())

def _do_list_commands(workspace):
    print(workspace.to_list_string())
    _list_commands(workspace)

def stash(argv):
    root_model = load_backend()
    working_id = get_working_workspace()
    workspace = root_model.get_workspace(working_id)
    if workspace is not None:
        if len(argv) < 1:
            _do_list_commands(workspace)
        else:
            new_cmd_str = ' '.join(argv[0:])
            new_cmd = CommandModel(new_cmd_str)
            workspace.add_cmd(new_cmd)
            print(new_cmd.to_list_string())
    else:
        print('This is an unexpected error. If there is no active workspace, '
              'you should be given the globals.')

    write_backend(root_model)
################################################################################

###################################### work ####################################
def _do_list_workspaces():
    root_model = load_backend()

    workspace = root_model.globals
    print(workspace.to_list_string())
    # print('{} {} {}'.format(workspace.id, workspace.name,  workspace.root))

    for workspace in root_model.workspaces:
        print(workspace.to_list_string())
        # print('{} {} {}'.format(workspace.id, workspace.name,  workspace.root))


def work(argv):
    if len(argv) == 0:
        _do_list_workspaces()
        sys.exit()
    elif len(argv) == 1:
        root_model = load_backend()
        workspace_id = argv[0]
        workspace = root_model.get_workspace(int(workspace_id))
        if workspace is not None:
            print(workspace.root)
            print(workspace.init)
        else:
            print()
            print()
            print('Did not find matching workspace')
################################################################################

####################################### do #####################################
def _do_do(workspace, cmd_id):
    cmd_model = workspace.get_cmd(cmd_id)
    if cmd_model is not None:
        print(cmd_model.command)
    else:
        print('.')
        print("")
        print('Command {} is not in the current workspace({})'.format(cmd_id, workspace.id))


def do_command(argv):
    root_model = load_backend()
    working_id = get_working_workspace()
    workspace = root_model.get_workspace(working_id)
    if workspace is not None:
        if len(argv) < 1:
            _do_list_commands(workspace)
        elif len(argv) == 1:
            cmd_id = int(argv[0])
            _do_do(workspace, cmd_id)
    else:
        print('This is an unexpected error. If there is no active workspace, '
              'you should be given the globals.')
################################################################################

####################################### new ####################################
def _do_new(new_dir, new_name):
    root_model = load_backend()

    new_workspace = WorkspaceModel()
    new_workspace.root = new_dir
    new_workspace.name = new_name

    root_model.add_workspace(new_workspace)

    write_backend(root_model)
    return new_workspace

def new(argv):
    if len(argv) < 2:
        new_usage(argv)
        sys.exit()
    new_dir = argv[0]
    new_name = argv[1]

    new_dir = os.path.abspath(new_dir)
    new_dir = os.path.realpath(new_dir)

    new_workspace = _do_new(new_dir, new_name)

    print('created new workspace [{}] {}'.format(new_workspace.id, new_workspace.name))
################################################################################

####################################### name ###################################
def _do_name(workspace, entry_type, entry_id, entry_name):
    model = workspace.get_cmd(entry_id) if entry_type == 'cmd' else workspace.get_dir(entry_id)
    if model is not None:
        if entry_name is None:
            if model.name is not None:
                print(model.name)
                return False
            else:
                print('{} {} has no name'.format(entry_type, entry_id))
                return False
        else:
            model.set_name(entry_name)
            print(model.to_list_string())
            return True
    else:
        print('{} {} is not in the current workspace({})'.format(entry_type, entry_id, workspace.id))
        return False


def name(argv):
    root_model = load_backend()
    working_id = get_working_workspace()
    workspace = root_model.get_workspace(working_id)
    if workspace is not None:
        if len(argv) < 2:
            name_usage(argv)
        # TODO: be able to name things with just .N or /N (for cmds/dirs)
        # elif len(argv) == 1:
        #     cmd_id = int(argv[0])
        #     _do_do(workspace, cmd_id)
        else:
            entry_type = argv[0]
            entry_id = int(argv[1])
            entry_name = argv[2] if len(argv) > 2 else None
            if not ((entry_type == 'cmd') or (entry_type == 'dir')):
                name_usage(argv)
                print('Expected either \'cmd\' or \'dir\', got \'{}\''.format(entry_type))
            else:
                save = _do_name(workspace, entry_type, entry_id, entry_name)
                if save:
                    write_backend(root_model)
    else:
        print('This is an unexpected error. If there is no active workspace, '
              'you should be given the globals.')
################################################################################

################################################################################
def init(argv):
    if len(argv) < 2:
        init_usage(argv)
        sys.exit()

    root_model = load_backend()
    workspace_id = argv[0]
    workspace = root_model.get_workspace(int(workspace_id))
    if workspace is not None:
        workspace.init = ' '.join(argv[1:])
        print('Set workspace {}\'s init command to `{}`'.format(workspace.id, workspace.init))
        write_backend(root_model)
################################################################################

##################################### backend ##################################
def backend_command(argv):
    backend_path = os.path.join(KEEP_BACKEND_ROOT, 'backend')
    if not os.path.exists(backend_path):
        print('Backend path {} doesn\'t exist'.format(backend_path))
    print('Path to backend file: {}'.format(backend_path))
################################################################################


def usage(argv):
    print('usage')

def new_usage(argv):
    print('usage: new <directory> <name>')
    print('\tCreates a new workspace in the given dir with the given name.')

def init_usage(argv):
    print('usage: init <workspace id> <command>')
    print('\tCreates a new workspace in the given dir with the given name.')

def name_usage(argv):
    print('usage: name <cmd|dir> <id> [name]')
    print('\tNames either a dir or command. If [name] is omitted, instead prints the name of the dir/command')

def E_NOT_IMPL(argv):
    print('Command not implemented yet.')
    print('argv={}'.format(argv))

commands = {
    'keep': keep
    , 'list': list_workspace
    , 'go': go
    , 'work': work
    , 'stash': stash
    , 'do': do_command
    , 'new': new
    , 'init': init
    , 'backend': backend_command
    , 'name': name
}
# name [cmd|dir] [id] <name>
# sets the name for the cmd or dir with the given id to name, or prints it's name
