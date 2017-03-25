# -*- coding:utf-8 -*-
import time
import threading


def printf(i):
    for x in xrange(5):
        time.sleep(1)
        print i,


def test():
    thread_list = []
    for i in xrange(10):
        sthread = threading.Thread(target=printf, args=str(i))
        sthread.start()
        thread_list.append(sthread)
    for i in xrange(10):
        thread_list[i].join()


if __name__ == '__main__':
    test()
