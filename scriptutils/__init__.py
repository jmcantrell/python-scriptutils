__all__ = ['cache', 'config', 'input', 'messages', 'options', 'terminal']

from .terminal import Terminal

VERBOSE = True
INTERACTIVE = True
ENCODING = 'utf-8'
TERMINAL = Terminal()
