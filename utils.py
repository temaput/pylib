""" my version of summerfield utils, 
some usefull funcs for imstrumental"""

import logging
log = logging.getLogger(__name__)

# 
# class decorators
#



def delegate(methodnames, wrapper=None, attrname=None):
    """ decorates class with methods in methodnames
        methods are references to the same methods in
        attrname object (if given), or in parent class
        if wrapper (func reference) is given 
        than the result of these methods will be passed to it first 

        using this class decorator makes the effect of decorating each
        class method i.e.

        @delegate(('add', 'sub'), wrapper, 'obj') 
        class...:

        is the same as to say

        class ...:
        @wrapper
        def add(self):
            return obj.add()

        @wrapper
        def sub(self):
            return obj.sub()
    """
    if wrapper is None and attrname is None: 
        return lambda cls: cls 
    result_wrapper = wrapper or (lambda result: result)
    def func_decorator(cls, mname):
        def func_wrapper(self, *args, **kwargs):
            return result_wrapper(
                getattr(
                getattr(self, attrname) if attrname else super(cls, self), 
                mname)(*args, **kwargs))
        return func_wrapper
    def class_decorator(cls):
        for mname in methodnames:
                setattr(cls, mname, func_decorator(cls, mname))
        return cls
    return class_decorator
                    
