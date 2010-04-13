from getpass import getpass

from . import chunks, zip_pad
from .terminal import Terminal

def truth(value):
    true_values = ['yes', 'y', 'true', 't', 'on', '1']
    return str(value).strip().lower() in true_values

def input_safe(prompt='Enter value', secret=False, default=None, num=None):
    getter = getpass if secret else raw_input
    if not secret and default is not None:
        prompt += " [%s]" % default
    try:
        reply = getter(prompt+': ')
    except:
        reply = None
    if not (len(reply) or secret):
        reply = str(default)
    return reply.strip()

def input_cast(cast=str, **kwargs):
    while True:
        reply = input_safe(**kwargs)
        if not len(reply):
            return None
        try:
            value = cast(reply)
        except:
            continue

def input_bool(**kwargs):
    if truth(input_safe(**kwargs)): return True
    return False

def input_float(minval=None, maxval=None, **kwargs):
    kwargs.setdefault('prompt', 'Enter a float')
    cast = kwargs.get('cast', float)
    while True:
        value = input_cast(cast=cast, **kwargs)
        if value is None: return None
        if minval is not None and value < minval: continue
        if maxval is not None and value > maxval: continue
        return value

def input_int(**kwargs):
    kwargs['cast'] = int
    kwargs.setdefault('prompt', 'Enter an integer')
    return input_float(**kwargs)

def question(**kwargs):
    kwargs.setdefault('prompt', 'Are you sure you want to proceed?')
    if 'default' in kwargs:
        kwargs['default'] = 'y' if truth(kwargs['default']) else 'n'
    return input_bool(**kwargs)

def choice(choices, prompt='Select from these choices'):
    print prompt+':'
    print choice_list
    reply = input_int(prompt='#', minval=1, maxval=len(choices))
    if reply is None: return None
    return choices[reply]

def choice_list(choices):
    if not len(choices): return
    choices = [str(i) for i in choices]
    t = Terminal()
    c_len = len(choices)
    m_elm = len(str(max(choices, key=len)))
    m_idx = len(str(c_len))
    # Every column will be as wide as the largest item
    m_col = m_idx + m_elm + 4  # 4 for ') ' and '  ' for padding
    cols = (t.COLS / m_col) or 1
    rows = (c_len / cols + int(c_len % cols != 0)) or 1
    cols = (c_len / rows + int(c_len % rows != 0)) or 1
    if rows == 1:
        rows = cols
        cols = 1
    grid = list(chunks(range(len(choices)), rows))
    grid_max = [len(str(i[-1])) for i in grid]
    def f(m, ln, n, li, i):
        s = '%*s) %-*s' % (ln, n, li, i)
        return '%-*s' % (m, s)
    for row in zip_pad(*grid):
        print ''.join(
                f(m_col, grid_max[i], n+1, m_elm, choices[n])
                for i, n in enumerate(row)
                if n is not None
                )
