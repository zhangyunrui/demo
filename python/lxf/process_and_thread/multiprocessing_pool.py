from multiprocessing import Pool
import os, time, random


def long_time_proc(name):
    print 'Run task %s(%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print 'Task %s takes %.6f' % (name, end - start)


if __name__ == '__main__':
    print 'Parent Process (%s)' % os.getpid()
    p = Pool()
    for i in range(9):
        p.apply_async(long_time_proc, (i,))
        print 'Task applied'
    print 'All task applied'
    p.close()
    print 'Task closed'
    p.join()
    print 'All Subprocesses done'
