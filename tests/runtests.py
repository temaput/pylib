import unittest
import logging


log = logging.getLogger('Test suite')

# ========================================
#       testing utils:decorators
# ========================================

from tema.utils import wrapsimilar
class Root:
    def __add__(self, other):
        return 1 + other
    def __sub__(self, other):
        return 1 - other


def wrapper(methodname, callee):
    log.debug("methodname is %s", methodname)
    def _method(self, *args, **kwargs): 
        o = callee(self) or super(self.__class__, self)
        result = getattr(o, methodname)(*args, **kwargs)
        log.debug("result is %s", result)
        return 'even' if not result % 2 else 'odd'
    return _method



@wrapsimilar(wrapper, ('__add__', '__sub__'))
class Sub(Root): pass

@wrapsimilar(wrapper, ('__add__', '__sub__'), '_obj')
class Wrapper:
    _obj = Root()

class Decorators(unittest.TestCase):
    def testWrapsimilar(self):
        s = Sub()
        self.assertEqual(s + 1, 'even')
        self.assertEqual(s + 2, 'odd')



if __name__ == '__main__':
    unittest.main()

