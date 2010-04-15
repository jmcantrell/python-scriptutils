import os, shlex
from subprocess import PIPE, Popen

def in_directory(f, directory=None):
    def new_f(*args, **kwargs):
        d = directory or kwargs.get('directory', os.getcwd())
        prev_cwd = os.getcwd()
        os.chdir(directory)
        try:
            f(*args, **kwargs)
        finally:
            os.chdir(prev_cwd)
    return new_f

@in_directory
def execute(command, stdin=None, directory=None):
    if not isinstance(command, (list, tuple)):
        command = shlex.split(command)
    if not stdin:
        stdin = PIPE
    p = Popen(command, stdin=stdin, stdout=PIPE, stderr=PIPE)
    return p.communicate()  #==> (stdout, stderr)
