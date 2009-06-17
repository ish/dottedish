__all__ = ['dotted', 'set', 'get', 'flatten', 'unflatten']


from simplegeneric import generic


##
# High-level API.

_sentinel = object()

def dotted(o):
    """
    Return an object that support dotted key access.
    """
    wrapped = wrap(o)
    if o is wrapped:
        raise TypeError()
    return wrapped

def set(o, key, value):
    """
    Set the item with the given dotted key to the given value.
    """
    parent, key = _parent_and_key(o, key)
    setitem(parent, key, value)

def get(o, key, default=_sentinel):
    """
    Get the item with the given dotted key.
    """
    return wrap(_get(o, key, default))

def flatten(o):
    """
    Flatten an object graph into a sequence of (key, value) pairs where key is
    a nested key with segments separated by a '.'.
    """
    stack = [(wrap(o).iteritems(), None)]
    while stack:
        items_iter, parent_key = stack[-1]
        for (key, value) in items_iter:
            if parent_key is None:
                full_key = key
            else:
                full_key = '.'.join([parent_key, key])
            if value is not unwrap(value):
                stack.append((iter(value.items()), full_key))
                break
            yield full_key, value
        else:
            stack.pop()

def unflatten(l):
    """
    Expand a flattened list into a graph of dictionaries.

    Note: By default, this will not reverse the result of flatten() if the
    flattened object contained any lists as there is no information in a key
    such as 'foo.0' to say if the container 'foo' is a dict or a list.
    """
    root = {}
    for (key, value) in l:
        key = key.split('.')
        container_key, item_key = key[:-1], key[-1]
        container = reduce(lambda container, key: container.setdefault(key, {}), container_key, root)
        container[item_key] = value
    return root


##
# Extension API.

@generic
def setitem(o, key, value):
    raise NotImplementedError()

@generic
def getitem(o, key):
    raise NotImplementedError()

@generic
def wrap(o):
    return o

@generic
def unwrap(o):
    return o


##
# Internal implemenation.

def _parent_and_key(o, key):
    key = key.split('.')
    parent_key, item_key = key[:-1], key[-1]
    if parent_key:
        o = _get(o, '.'.join(parent_key))
    return o, item_key

def _get(o, key, default=_sentinel):
    key = key.split('.')
    parent_key, item_key = key[:-1], key[-1]
    for k in parent_key:
        o = getitem(o, k)
    try:
        return getitem(o, item_key)
    except KeyError:
        if default is _sentinel:
            raise
        else:
            return default

