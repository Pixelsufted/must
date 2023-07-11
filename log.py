import sys


def warn(*args) -> None:
    sys.stderr.write('[WARN]: ' + ' '.join([str(_x) for _x in args]))


def info(*args) -> None:
    sys.stdout.write('[INFO]: ' + ' '.join([str(_x) for _x in args]))
