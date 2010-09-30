import os, shlex, sys
from subprocess import PIPE, Popen

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

@in_directory
def system(command, **kwargs):
    kwargs.setdefault('stdout', sys.stdout)
    kwargs.setdefault('stderr', sys.stderr)
    return execute(command, **kwargs)[0]

@in_directory
def execute(command, **kwargs):
    if not isinstance(command, (list, tuple)):
        command = shlex.split(command)
    kwargs.setdefault('stdout', PIPE)
    kwargs.setdefault('stderr', PIPE)
    p = Popen(command, **kwargs)
    e, o = p.communicate()
    return p.returncode, o, e
