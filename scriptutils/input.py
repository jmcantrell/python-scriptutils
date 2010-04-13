from getpass import getpass
from unicodeutils import decode
from pathutils import condense

from . import chunks, truth, zip_pad
from . import ENCODING, INTERACTIVE, TERMINAL

def input(prompt='Enter value', secret=False, default=None, check=False): #{{{1
    if check and not INTERACTIVE:
        if secret: return u''
        return default or u''
    prompt = condense(prompt)
    default = decode(default, encoding=ENCODING)
    getter = getpass if secret else raw_input
    if not secret and default is not None:
        prompt += " [%s]" % default
    try:
        if prompt:
            reply = getter(prompt.strip()+': ')
        else:
            reply = getter()
    except:
        reply = ''
    reply = decode(reply, encoding=ENCODING)
    if not (len(reply) or secret):
        reply = default
    return reply.strip()

def input_cast(cast=str, **kwargs): #{{{1
    while True:
        reply = input(**kwargs)
        if not len(reply):
            return None
        try:
            value = cast(reply)
        except:
            continue

def input_bool(**kwargs): #{{{1
    if truth(input(**kwargs)): return True
    return False

def input_float(minval=None, maxval=None, **kwargs): #{{{1
    kwargs.setdefault('prompt', 'Enter a float')
    cast = kwargs.get('cast', float)
    while True:
        value = input_cast(cast=cast, **kwargs)
        if value is None: return None
        if minval is not None and value < minval: continue
        if maxval is not None and value > maxval: continue
        return value

def input_int(**kwargs): #{{{1
    kwargs['cast'] = int
    kwargs.setdefault('prompt', 'Enter an integer')
    return input_float(**kwargs)

def input_lines(prompt='Enter values', check=False): #{{{1
    if check and not INTERACTIVE: return None
    lines = []
    print '%s (one per line):' % condense(prompt)
    while True:
        try:
            lines.append(input(prompt=''))
        except EOFError:
            return lines
        except KeyboardInterrupt:
            return None

def question(**kwargs): #{{{1
    kwargs.setdefault('prompt', 'Are you sure you want to proceed?')
    if 'default' in kwargs:
        kwargs['default'] = 'y' if truth(kwargs['default']) else 'n'
    return input_bool(**kwargs)

def choice(choices, prompt='Select from these choices'): #{{{1
    if not INTERACTIVE: return None
    print prompt+':'
    print choice_list
    reply = input_int(prompt='#', minval=1, maxval=len(choices))
    if reply is None: return None
    return choices[reply]

def choice_list(choices): #{{{1
    if not len(choices): return
    choices = [str(i) for i in choices]
    c_len = len(choices)
    m_elm = len(str(max(choices, key=len)))
    m_idx = len(str(c_len))
    # Every column will be as wide as the largest item
    m_col = m_idx + m_elm + 4  # 4 for ') ' and '  ' for padding
    cols = (TERMINAL.COLS / m_col) or 1
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
