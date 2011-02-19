import sys
from pathutils import condense
from unicodeutils import encode

from . import ENCODING, TERMINAL, VERBOSE

def pack(t, text):
    return ''.join([t, text, TERMINAL.NORMAL])

def black(text):
    return pack(TERMINAL.BLACK, text)

def blue(text):
    return pack(TERMINAL.BLUE, text)

def green(text):
    return pack(TERMINAL.GREEN, text)

def cyan(text):
    return pack(TERMINAL.CYAN, text)

def red(text):
    return pack(TERMINAL.RED, text)

def magenta(text):
    return pack(TERMINAL.MAGENTA, text)

def yellow(text):
    return pack(TERMINAL.YELLOW, text)

def white(text):
    return pack(TERMINAL.WHITE, text)

def bold(text):
    return pack(TERMINAL.BOLD, text)

def tag_message(tag, message):
    message = white(encode(condense(message), encoding=ENCODING))
    return bold(' '.join([tag, message]))

def info_message(message='All updates are complete.'):
    return tag_message(blue('==>'), message)

def info(check=False, **kwargs):
    if check and not VERBOSE: return
    print >>sys.stderr, info_message(**kwargs)

def warn_message(message='A warning has occurred.'):
    return tag_message(yellow('WARNING:'), message)

def warn(check=False, **kwargs):
    if check and not VERBOSE: return
    print >>sys.stderr, warn_message(**kwargs)

def error_message(message='An error has occurred.'):
    return tag_message(red('ERROR:'), message)

def error(check=False, **kwargs):
    if check and not VERBOSE: return
    print >>sys.stderr, error_message(**kwargs)
