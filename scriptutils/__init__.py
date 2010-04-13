__all__ = ['cache', 'config', 'input', 'options', 'terminal']

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def zip_pad(*itrs):
    m = len(max(itrs, key=len))
    return zip(*[i+[None]*(m-len(i)) for i in itrs])
