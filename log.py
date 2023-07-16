import sys


enable_logging = True


def warn(*args) -> None:
    if enable_logging:
        sys.stderr.write('[WARN]: ' + ' '.join([str(_x) for _x in args]) + '\n')


def info(*args) -> None:
    if enable_logging:
        sys.stdout.write('[INFO]: ' + ' '.join([str(_x) for _x in args]) + '\n')
