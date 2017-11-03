from common import *
from models import *
from backend import *

__author__ = 'zadjii'

def keep(argv):
    pass
def go(argv):
    pass

def _do_list_workspaces(): 
    root_model = load_backend()
    for workspace in root_model.workspaces:
        print('{} {} {}'.format(workspace.id, workspace.name,  workspace.root))


def work(argv):
    if len(argv) == 0:
        _do_list_workspaces()
        sys.exit()


def do_command(argv):
    pass

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

    new_workspace = _do_new(new_dir, new_name)

    print('created new workspace [{}] {}'.format(new_workspace.id, new_workspace.name))

def usage(argv):
    print('usage')

def new_usage(argv):
    print('usage: new <directory> <name>')
    print('\tCreates a new workspace in the given dir with the given name.')

commands = {
    'keep': keep
    , 'go': go
    , 'work': work
    , 'do': do_command
    , 'new': new
}
