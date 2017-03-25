# -*- coding:utf8 -*-
from multiprocessing import Process
import os


# # use os
# print 'Process (%s) start ...' % os.getpid()
# pid = os.fork()
# if pid == 0:
#     print 'I`m child process (%s) and my parent is (%s)' % (os.getpid(), os.getppid())
# else:
#     print 'I (%s) just create a child process (%s)' % (os.getpid(), pid)


# use multiprocessing
def run_proc():
    print 'I`m child process (%s) and my parent is (%s)' % (os.getpid(), os.getppid())


print 'Process (%s) start ...' % os.getpid()
p = Process(target=run_proc)
p.start()
p.join()
print 'I (%s) just create a child process (%s)' % (os.getpid(), p.pid)
