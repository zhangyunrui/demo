from multiprocessing import Pool
import os, time, random


def long_time_proc(name):
    print 'Run task %s(%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 0.01)
    end = time.time()
    print 'Task %s takes %.6f' % (name, end - start)


if __name__ == '__main__':
    print 'Parent Process (%s)' % os.getpid()
    p = Pool()
    for i in range(5):
        p.apply_async(long_time_proc, (i,))
    p.close()
    p.join()
    print 'All Subprocesses done'
