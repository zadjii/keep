from commands import *

__author__ = 'zadjii'

def main(argv):
    
    enable_vt_support()

    if len(argv) < 2:
        usage(argv)
        sys.exit()

    command = argv[1]
    if command in commands.keys():
        commands[command](argv[2:])
