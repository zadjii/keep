import os
import sys


KEEP_PATH=os.path.dirname(os.path.abspath(__file__));
KEEP_BACKEND=os.path.join(KEEP_PATH, '.dirs')

################################################################################
# Turns VT output support on
def enable_vt_support():
    if os.name == 'nt':
        import ctypes
        hOut = ctypes.windll.kernel32.GetStdHandle(-11)
        out_modes = ctypes.c_uint32()
        ENABLE_VT_PROCESSING = ctypes.c_uint32(0x0004)
        # ctypes.addressof()
        ctypes.windll.kernel32.GetConsoleMode(hOut, ctypes.byref(out_modes))
        out_modes = ctypes.c_uint32(out_modes.value | 0x0004)
        ctypes.windll.kernel32.SetConsoleMode(hOut, out_modes)


################################################################################
class KeepEntry(object):
    def __init__(self, index, path):
        super(KeepEntry, self).__init__()
        self.index = int(index)
        self.path = path
        

################################################################################
class KeepData(object):
    def __init__(self):
        super(KeepData, self).__init__()
        self._lines = []
        self._next_index = 0
        self.read_backend()

    def read_backend(self):
        lines = []
        try:
            with open(KEEP_BACKEND) as handle:
                lines = handle.readlines()

        except IOError:
            # Couldn't find backend
            pass
        # you may also want to remove whitespace characters like `\n` at the end of each line
        lines = [line.strip() for line in lines] 
        for line in lines:
            parts = line.split(',')
            if len(parts) >= 2:
                index, path = int(parts[0]), parts[1]
                entry = KeepEntry(index, path)
                self._lines.append(entry)
                if entry.index >= self._next_index:
                    self._next_index = entry.index + 1

    def write_backend(self):
        try:
            with open(KEEP_BACKEND, 'wb') as handle:
                for entry in self._lines:
                    handle.write('{},{}\n'.format(entry.index, entry.path))

        except IOError:
            # Couldn't find backend
            pass

    def list_entries(self):
        for entry in self._lines:
            print(self.entry_to_string(entry))

    def entry_to_string(self, entry):
        abs_path = os.path.abspath(os.getcwd())
        abs_path = os.path.realpath(abs_path)
        # fmt = '{}*\t{}' if abs_path == entry.path else '{}\t{}'
        fmt = '{}*\t\x1b[1;32m{}\x1b[0m' if abs_path == entry.path else '{}\t{}'
        return fmt.format(entry.index, entry.path)

    def add_path(self, path):
        abs_path = os.path.abspath(path)
        abs_path = os.path.realpath(abs_path)
        found = False
        for entry in self._lines:
            if entry.path == abs_path:
                found = True
                print(self.entry_to_string(entry))
                break

        if not found:
            entry = KeepEntry(self._next_index, path)
            self._lines.append(entry)
            self._next_index = entry.index + 1
            print(self.entry_to_string(entry))

    def change_dir(self, index):
        index = int(index)
        for entry in self._lines:
            if entry.index == index:
                # with open('CONIN$', mode='wb') as inhandle:
                #     inhandle.write('cd {}'.format(entry.path))
                # print('cd {}'.format(entry.path))
                print('{}'.format(entry.path))
                # os.chdir(entry.path)
                return
        print('Could not find an entry for {}'.format(index))

    def refresh_entries(self):
        """
        takes all the entries and removes gaps 
        eg. [1, 3, 5, 7] -> [0, 1, 2, 3]
        """
        for index, entry in enumerate(self._lines):
            # print('{}'.format(entry.path, index))
            entry.index = index
        self.write_backend()
        self.list_entries()


################################################################################

def keep(argv):
    data = KeepData()
    data.add_path(os.getcwd())
    data.write_backend()
    # print('keep')

def list(argv):
    data = KeepData()
    data.list_entries()

def go(argv):
    data = KeepData()
    # I want this to work, but it really REALLY doesn't work with the bat script.
    # number = None
    # if len(argv) < 1:
    #     s = raw_input('enter a dir #:')
    #     number = int(s)
    # else:
    #     number = argv[0]
    number = argv[0]
    data.change_dir(number)

def refresh(argv):
    data = KeepData()
    data.refresh_entries()

commands = {
    'keep': keep
    , 'list': list
    , 'go': go
    , 'refresh': refresh
}


def main(argv):
    enable_vt_support()
    cmd = argv[1]
    # print(cmd)
    if cmd in commands.keys():
        commands[cmd](argv[2:])
    else:
        print('unknown command')

if __name__ == '__main__':
    argv = sys.argv

    main(argv)