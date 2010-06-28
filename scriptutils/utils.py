def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def truth(value):
    true_values = ['yes', 'y', 'true', 't', 'on', '1']
    return str(value).strip().lower() in true_values

def zip_pad(*itrs):
    m = len(max(itrs, key=len))
    return zip(*[i+[None]*(m-len(i)) for i in itrs])
