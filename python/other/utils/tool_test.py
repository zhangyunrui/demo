# -*- coding:utf8 -*-
import time

from tools import timeit, timeit2


@timeit2('timeit_test2')
def time_it_test():
    print time.time()
    time.sleep(1)
    print time.time()

# timeit2('test_text')(time_it_test)()

time_it_test()
