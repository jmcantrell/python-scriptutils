import sys
from pathutils import condense
from unicodeutils import encode

from . import ENCODING, TERMINAL, VERBOSE

def info(message='All updates are complete.', check=False):
    if check and not VERBOSE: return
    message = condense(message)
    print >>sys.stderr, TERMINAL.BOLD+encode(message, encoding=ENCODING)+TERMINAL.NORMAL

def warn(**kwargs):
    kwargs.setdefault('message', 'A warning has occurred.')
    kwargs['message'] = TERMINAL.YELLOW+'WARNING: %s' % kwargs['message']
    info(**kwargs)

def error(**kwargs):
    kwargs.setdefault('message', 'An error has occurred.')
    kwargs['message'] = TERMINAL.RED+'ERROR: %s' % kwargs['message']
    info(**kwargs)
