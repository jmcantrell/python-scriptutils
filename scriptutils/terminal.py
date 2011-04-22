import re

try:
    import curses; curses.setupterm()
    CURSES = True
except:
    CURSES = False

class Terminal(object):

    COLS = None
    LINES = None

    COLORS = 0

    FG = {}
    BG = {}
    FX = {}

    CAPS = {
            'RESET':       'sgr0',
            'BOLD':        'bold',
            'DIM':         'dim',
            'STANDOUT':    'smso',
            'ITALIC':      'sitm',
            'UNDERLINE':   'smul',
            'BLINK':       'blink',
            'REVERSE':     'rev',
            }

    COLOR_NAMES = [
            'BLACK',
            'RED',
            'GREEN',
            'YELLOW',
            'BLUE',
            'MAGENTA',
            'CYAN',
            'WHITE',
            ]

    set_fg = ''
    set_bg = ''

    def __init__(self):
        self.COLS = self.tigetnum('cols')
        self.LINES = self.tigetnum('lines')
        self.COLORS = self.tigetnum('colors')

        for attr, cap in self.CAPS.items():
            setattr(self, attr, self.tigetstr(cap) or '')

        for mode in 'FG', 'BG':
            parm = self.tigetstr('seta%s' % mode[0].lower())
            if not parm: continue
            setattr(self, 'set_%s' % mode.lower(), parm)
            for n, color in enumerate(self.COLOR_NAMES):
                attr = '%s_%s' % (mode.upper(), color)
                setattr(self, attr, self.tparm(parm, n))

    def fg(self, num):
        if num not in self.FG:
            self.FG[num] = self.tparm(self.set_fg, num)
        return self.FG[num]

    def bg(self, num):
        if num not in self.BG:
            self.BG[num] = self.tparm(self.set_bg, num)
        return self.BG[num]

    def fx(self, name):
        if name not in self.FX:
            self.FX[name] = self.tigetstr(name)
        return self.FX[name]

    def tparm(self, parm, name):
        if not CURSES: return ''
        return curses.tparm(parm, name) or ''

    def tigetnum(self, cap):
        if not CURSES: return 0
        return curses.tigetnum(cap)

    def tigetstr(self, cap):
        """
        String capabilities can include "delays" of the form "$<2>".
        For any modern terminal, we should be able to just ignore
        these, so strip them out.
        """
        if not CURSES: return ''
        return re.sub(r'\$<\d+>[/*]?', '', curses.tigetstr(cap) or '')
