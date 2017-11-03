from common import *
from models import *
from backend import *

__author__ = 'zadjii'

def keep(argv):
    cwd = os.getcwd()
    E_NOT_IMPL(argv)

def go(argv):
    E_NOT_IMPL(argv)

def _do_list_workspaces(): 
    root_model = load_backend()
    
    workspace = root_model.globals
    print('{} {} {}'.format(workspace.id, workspace.name,  workspace.root))

    for workspace in root_model.workspaces:
        print('{} {} {}'.format(workspace.id, workspace.name,  workspace.root))


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

def do_command(argv):
    E_NOT_IMPL(argv)

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

def usage(argv):
    print('usage')

def new_usage(argv):
    print('usage: new <directory> <name>')
    print('\tCreates a new workspace in the given dir with the given name.')

def init_usage(argv):
    print('usage: init <workspace id> <comamnds>')
    print('\tCreates a new workspace in the given dir with the given name.')

def E_NOT_IMPL(argv):
    print('Command not implemented yet.')
    print('argv={}'.format(argv))

commands = {
    'keep': keep
    , 'go': go
    , 'work': work
    , 'do': do_command
    , 'new': new
    , 'init': init
}
