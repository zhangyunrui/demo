from multiprocessing import Process, Queue
import time, random


def write(q):
    for v in ['A', 'B', 'C']:
        print 'Put %s in Q' % v
        q.put(v)
        time.sleep(random.random())


def read(q):
    while True:
        print 'Get %s from Q' % q.get(True)


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()
