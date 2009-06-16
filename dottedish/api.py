from simplegeneric import generic


##
# High-level API.

def dotted(o):
    return wrap(o)

def set(o, key, value):
    key = key.split('.')
    parent_key, item_key = key[:-1], key[-1]
    if parent_key:
        o = _get(o, '.'.join(parent_key))
    setitem(o, item_key, value)

def get(o, key, default=None):
    return wrap(_get(o, key, default))

def del(o, key):

def _get(o, key, default=None):
    sentinel = object()
    key = key.split('.')
    parent_key, item_key = key[:-1], key[-1]
    for k in parent_key:
        o = getitem(o, k, sentinel)
        if o is sentinel:
            raise KeyError(k)
    return getitem(o, item_key, default)


##
# Extension API.

@generic
def setitem(o, key, value):
    raise NotImplementedError()

@generic
def getitem(o, key, default):
    raise NotImplementedError()

@generic
def wrap(o):
    return o

