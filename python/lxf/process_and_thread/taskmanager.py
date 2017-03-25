import Queue
import random
from multiprocessing.managers import BaseManager

task_queue = Queue.Queue()
result_queue = Queue.Queue()


class QueueManager(BaseManager):
    pass


QueueManager.register('get_task_queue', lambda: task_queue)
QueueManager.register('get_result_queue', lambda: result_queue)

manager = QueueManager(('', 5000), 'abc')
manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

for i in range(10):
    n = random.randint(0, 10000)
    print 'Put task %d...' % n
    task.put(n)

print('Try get results...')
for i in range(10):
    r = result.get(timeout=10)
    print 'Result: %s' % r

manager.shutdown()
