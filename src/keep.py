from common import *
from models import *

__author__ = 'zadjii'


def do_load_backend():
    #type () -> ResultAndData
    backend_path = os.path.join(KEEP_BACKEND_ROOT, 'backend')
    print(backend_path)
    if not os.path.exists(backend_path):
        # return Error('Backend file does not exist')
        return Success([])
    with open(backend_path) as f:
        file_contents = f.read()
        print(file_contents)
        backend_dict = json.loads(file_contents)
        if not 'workspaces' in backend_dict.keys():
            return Error('Error parsing backend data')
        serialized_obj = RootModel.deserialize(backend_dict)
        # workspaces = [WorkspaceModel.deserialize(_work) for _work in backend_dict['workspaces']]
        return Success(serialized_obj.workspaces)


def do_write_backend(workspaces):
    backend_path = os.path.join(KEEP_BACKEND_ROOT, 'backend')
    serialized_obj = RootModel()
    serialized_obj.workspaces = workspaces
    serialized_string = serialized_obj.serialize()

    if not os.path.exists(KEEP_BACKEND_ROOT):
        os.makedirs(KEEP_BACKEND_ROOT)

    with open(backend_path, mode='wb') as f:
        f.write(serialized_string)

    return Success()

def load_backend():
    rd = do_load_backend()
    if not rd.success:
        print('Failed to load the keep backend.')
        print('Error: {}'.format(rd.data))
        sys.exit()
    return rd.data

def write_backend(workspaces):
    rd = do_write_backend(workspaces)
    if not rd.success:
        print('Failed to write the keep backend.')
        print('Error: {}'.format(rd.data))
        sys.exit()
    return rd.data


def keep(argv):
    pass
def go(argv):
    pass
def work(argv):
    pass
def do_command(argv):
    pass

def new(argv):
    print(argv)
    workspaces = load_backend()
    new_workspace = WorkspaceModel()
    new_workspace.root = 'foo'
    new_workspace.name = 'bar'
    workspaces.append(new_workspace)
    write_backend(workspaces)
    print('created new workspace {}'.format(new_workspace.name))

def usage(argv):
    print('usage')

commands = {
    'keep': keep
    , 'go': go
    , 'work': work
    , 'do': do_command
    , 'new': new
}

def main(argv):

    if len(argv) < 2:
        usage(argv)
        sys.exit()

    command = argv[1]
    if command in commands.keys():
        commands[command](argv[2:])
    # space = WorkspaceModel()
    # space.dirs.append(DirectoryModel('foo'))
    # space.dirs.append(DirectoryModel('bar'))
    # space_str = space.serialize() 
    # print(space_str)
    # outer_dict = json.loads(space_str)
    # outer_obj = WorkspaceModel.deserialize(outer_dict)
    # print(outer_obj)
    # print(outer_obj.__dict__)

    workspaces = load_backend()


if __name__ == '__main__':
    main(sys.argv)
