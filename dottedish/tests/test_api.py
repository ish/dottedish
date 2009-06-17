import unittest
from dottedish import api


class TestAPI(unittest.TestCase):

    def test_wrapping(self):
        s = ''
        self.assertTrue(s is api.wrap(s))
        self.assertTrue(s is api.unwrap(s))

    def test_dotted(self):
        self.assertRaises(TypeError, api.dotted, 'abc')

    def test_setitem_no_impl(self):
        self.assertRaises(NotImplementedError, api.set, '', 'foo', 0)

    def test_getitem_no_impl(self):
        self.assertRaises(NotImplementedError, api.get, '', 'foo')

    def test_flatten(self):
        for (test, result) in [
            ({}, []),
            ([], []),
            (['foo'], [('0', 'foo')]),
            ({'foo': 'bar'}, [('foo', 'bar')]),
            ({'foo': {'bar': [10, 11, 12, {'wibble': list('matt')}]}},
             [('foo.bar.0', 10), ('foo.bar.1', 11), ('foo.bar.2', 12), ('foo.bar.3.wibble.0', 'm'), ('foo.bar.3.wibble.1', 'a'), ('foo.bar.3.wibble.2', 't'), ('foo.bar.3.wibble.3', 't')])]:
            self.assertTrue(list(api.flatten(test)) == result)

    def test_unflatten(self):
        for (result, test) in [
            ({}, []),
            ({'0': 'foo'}, [('0', 'foo')]),
            ({'foo': 'bar'}, [('foo', 'bar')]),
            ({'foo': {'bar': {'0': 10, '1': 11, '2': 12, '3': {'wibble': {'0': 'm', '1': 'a', '2': 't', '3': 't'}}}}},
             [('foo.bar.0', 10), ('foo.bar.1', 11), ('foo.bar.2', 12), ('foo.bar.3.wibble.0', 'm'), ('foo.bar.3.wibble.1', 'a'), ('foo.bar.3.wibble.2', 't'), ('foo.bar.3.wibble.3', 't')])]:
            self.assertTrue(api.unflatten(test) == result)

