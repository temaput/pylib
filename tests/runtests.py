import unittest
import logging
log = logging.getLogger("Test suite")

#======================================== 
# testing decorators
#========================================

from tema.utils import delegate

class Root(object):
    def __add__(self, other):
        return 1 + other
    def __sub__(self, other):
        return 1 - other


def wrapper(result):
    return 'positive' if result >= 0 else 'negative'

@delegate(('__add__', '__sub__'), wrapper, '_object')
class Wrapper(object):
    def __init__(self, obj):
        self._object = obj


@delegate(('__add__', '__sub__'))
class SubEmpty(Root): pass


@delegate(('__add__', '__sub__'), lambda x: "{}".format(x))
class Sub(Root): pass

class TestDecorators(unittest.TestCase):
    def testWrappingDelegation(self):
        w = Wrapper(Root())
        log.debug("Testing wrapping delegation, _object is %s", w._object)
        self.assertEqual(w + 1, 'positive')
        neg = -10
        self.assertEqual(w + neg, 'negative')
        self.assertEqual(w - 4, 'negative')
        self.assertEqual(w - 0, 'positive')

    def testEmptyDecoratorAdd(self):
        s = SubEmpty()
        self.assertEqual(s + 1, 2)

    def testEmptyDecoratoriSub(self):
        s = SubEmpty()
        self.assertEqual(s - 1, 0)

    def testParentDelegationAdd(self):
        s = Sub()
        log.debug("s.__add__ is %s, s.__sub__ is %s", s.__add__, s.__sub__)
        self.assertEqual(s + 1, '2')

    def testParentDelegationSub(self):
        s = Sub()
        self.assertEqual(s - 1, '0')

class TestFunctions(unittest.TestCase):
    """ Here we test simple functions from utils e.g. removeany"""

    def testRemoveAny(self):
        from os import makedirs
        from os.path import dirname, join, exists
        path = join(dirname(__file__), 'test1')
        longpath = join(path, 'test2/test3')
        makedirs(longpath)
        fn = 'test.tmp'
        with open(join(longpath, fn), 'w') as f:
            f.write('test file')
        with open(join(path, fn), 'w') as f:
            f.write('test file')

        from tema.utils import removeany
        removeany(join(path, fn))
        self.assertFalse(exists(join(path, fn)))
        removeany(path)
        self.assertFalse(exists(path))


if __name__ == '__main__':
    unittest.main()
