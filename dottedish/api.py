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
    # Check that something has actually registered for this type, i.e. we
    # didn't just get wrap's default behaviour.
    if o is wrapped and not wrap.has_type(type(unwrap(o))):
        raise TypeError()
    return wrapped

def set(o, key, value, container_factory=None):
    """
    Set the item with the given dotted key to the given value.
    """
    parent, key = _parent_and_key(o, key, container_factory=container_factory)
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

    Note: flattening an object graph is a lossy process - there is no way to
    reverse the process reliably without help. Dotted key segments are strings
    and there is no way to know if a '0' segment represents a key in a dict or
    an index in a list.
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

def unflatten(l, container_factory=None):
    """
    Expand a flattened list into a graph of dictionaries.

    Note: By default, this will not reverse the result of flatten() if the
    flattened object contained any lists as there is no information in a key
    such as 'foo.0' to say if the container 'foo' is a dict or a list.
    """
    if container_factory is None:
        container_factory = lambda p, c: {}
    root = {}
    for (key, value) in l:
        set(root, key, value, container_factory=container_factory)
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

def _parent_and_key(o, key, container_factory):
    key = key.split('.')
    parent_key, item_key = key[:-1], key[-1]
    for i in range(len(parent_key)):
        container_key = parent_key[:(i+1)]
        try:
            o = getitem(o, container_key[-1])
        except KeyError:
            if container_factory is None:
                raise
            if len(container_key) == len(parent_key):
                container = container_factory('.'.join(container_key), item_key)
            else:
                container = container_factory('.'.join(container_key), parent_key[i+1])
            setitem(o, container_key[-1], container)
            o = container
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

