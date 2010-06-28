import sys
from pathutils import condense
from unicodeutils import encode

from . import ENCODING, TERMINAL, VERBOSE

def color(c, message):
    return c + message + TERMINAL.NORMAL

def bold(message):
    return TERMINAL.BOLD + message + TERMINAL.NORMAL

def info_message(message='All updates are complete.'):
    message = condense(message)
    return bold(encode(message, encoding=ENCODING))

def info(check=False, **kwargs):
    if check and not VERBOSE: return
    print >>sys.stderr, info_message(**kwargs)

def warn_message(**kwargs):
    kwargs.setdefault('message', 'A warning has occurred.')
    kwargs['message'] = color(TERMINAL.YELLOW, 'WARNING: %s' % kwargs['message'])
    return info_message(**kwargs)

def warn(check=False, **kwargs):
    if check and not VERBOSE: return
    print >>sys.stderr, warn_message(**kwargs)

def error_message(**kwargs):
    kwargs.setdefault('message', 'An error has occurred.')
    kwargs['message'] = color(TERMINAL.RED, 'ERROR: %s' % kwargs['message'])
    return info_message(**kwargs)

def error(**kwargs):
    if check and not VERBOSE: return
    print >>sys.stderr, error_message(**kwargs)
