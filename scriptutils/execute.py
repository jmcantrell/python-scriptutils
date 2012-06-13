import os, shlex, sys
from subprocess import PIPE, Popen


def split_command(command):
    if isinstance(command, (list, tuple)):
        return command
    return shlex.split(command)


def get_output(value):
    if not value:
        return sys.stdout
    if isinstance(value, (str, unicode)):
        return open(value, 'w')
    return value


def getattr_safe(o, attr, default=None):
    try:
        return getattr(o, attr) or default
    except AttributeError:
        return default


def in_directory(f, directory=None):
    """Decorator for running a function within a directory."""
    def new_f(*args, **kwargs):
        d = directory or kwargs.get('directory', os.getcwd())
        prev_cwd = os.getcwd()
        os.chdir(d)
        try:
            return f(*args, **kwargs)
        finally:
            os.chdir(prev_cwd)
    return new_f


def in_self_directory(m, directory=None):
    """Decorator for running a function within a directory."""
    def new_m(self, *args, **kwargs):
        d = directory or getattr_safe(self, 'directory', os.getcwd())
        prev_cwd = os.getcwd()
        os.chdir(d)
        try:
            return m(self, *args, **kwargs)
        finally:
            os.chdir(prev_cwd)
    return new_m


@in_directory
def system(command, **kwargs):
    kwargs.setdefault('stdout', sys.stdout)
    kwargs.setdefault('stderr', sys.stderr)
    return execute(command, **kwargs)[0]


@in_directory
def execute(command, **kwargs):
    kwargs.setdefault('stdout', PIPE)
    kwargs.setdefault('stderr', PIPE)
    p = Popen(split_command(command), **kwargs)
    o, e = p.communicate()
    return p.returncode, o, e


@in_directory
def chain(commands, output=None, **kwargs):
    stdin = None
    for command in commands:
        p = Popen(command, stdout=PIPE, stdin=stdin)
        stdin = p.stdout
    p.stdout = get_output(output)
    e, o = p.communicate()
    return p.returncode, o, e
