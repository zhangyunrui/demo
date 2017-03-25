# -*- coding: utf8 -*-

import time


def timeit(func):
    def wrap(*args, **kwargs):
        now = time.time()
        res = func(*args, **kwargs)
        print """
        func:%s proceed,
        takes %f s""" % (func.__name__, time.time() - now)
        return res

    return wrap


def timeit2(text):
    def decorator(func):
        def wrap(*args, **kwargs):
            now = time.time()
            res = func(*args, **kwargs)
            print """
            func:%s proceed,
            takes %f s,
            text is %s""" % (func.__name__, time.time() - now, text)
            return res

        return wrap

    return decorator
