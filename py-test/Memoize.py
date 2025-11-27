'''
Created on Oct 1, 2016

@author: libraryuser
'''

def memoize(f):
    class memodict(dict):
        __slots__ = ()

        def __missing__(self, *key):
            self[key] = ret = f(*key)
            return ret

    return memodict().__getitem__
