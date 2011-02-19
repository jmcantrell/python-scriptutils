__all__ = ['arguments', 'cache', 'config', 'input', 'messages', 'terminal']

from .terminal import Terminal

VERBOSE = True
INTERACTIVE = True
ENCODING = 'utf-8'
TERMINAL = Terminal()
