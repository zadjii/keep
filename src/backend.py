from common import *
from models import *

__author__ = 'zadjii'

def do_load_backend():
    #type () -> ResultAndData
    backend_path = os.path.join(KEEP_BACKEND_ROOT, 'backend')
    if not os.path.exists(backend_path):
        return Success(RootModel())
    with open(backend_path) as f:
        file_contents = f.read()
        backend_dict = {}
        if len(file_contents) > 0:
            backend_dict = json.loads(file_contents)
        serialized_obj = RootModel.deserialize(backend_dict)
        return Success(serialized_obj)


def do_write_backend(root_model):
    # serialized_obj = RootModel()
    serialized_string = root_model.serialize()

    backend_path = os.path.join(KEEP_BACKEND_ROOT, 'backend')
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
