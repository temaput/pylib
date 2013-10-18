""" my version of summerfield utils, 
some usefull funcs for imstrumental"""

import logging
log = logging.getLogger(__name__)

# 
# class decorators
#

def delegate(what, how=None, whom=None):
    """ decorator that makes easy wrapping of similar methods
        what - name of delegated method, e.g. '__add__'
        how - reference to the wrapping method
        whom - reference to the real worker class, that will actually do the 
        job
    """
    def decorator(cls):
        if how is None and whom is None: return cls  # nothing to do here
        for _method in what:
            if not hasattr(cls, _method):
                if not how:  # by default we make simple redirect
                    setattr(cls, _method, lambda self, *args, **kwargs: 
                                getattr(whom, _method)(*args, **kwargs))
                else: setattr(cls, _method, how(whom))


        return cls
    return decorator
                    
def wrapsimilar(wrapperfunc, methodnames, callee=None):
    log.debug("wrapperfunc is %s, callee is %s", wrapperfunc, callee)
    def checkcallee(obj):
        if callee:
            return getattr(obj, callee)
        else:
            return None

    def decorator(cls):
        for mname in methodnames:
            setattr(cls, mname, wrapperfunc(mname, checkcallee))
        return cls
    return decorator

    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
