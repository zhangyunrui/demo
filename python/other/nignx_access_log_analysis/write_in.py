# -*- coding: utf-8 -*-

# 每秒写入的条数随机(通过sleep随机的时间实现)
# ip随机生成，通过调窄生成范围来提高重复率
import datetime
import random

import time

import sys

from main2 import T_FORMAT

sys.setcheckinterval(10000)

_MAX = 1


def write_in_log():
    filename = '/tmp/tmp/out.log'
    now = datetime.datetime.now()
    st_now = now.strftime(T_FORMAT)
    with open(filename, 'a') as file:
        file.write(
            '- - - [%s +0800] "POST /v4/getTeacherAllBadges/ '
            'HTTP/1.1" 200 142 "-" "MaizieduTeacher/1.1.1 (iPhone; iOS 10.0.1; Scale/2.00)" '
            '"%s.%s.%s.%s" - "http://dev.microoh.com:99"\n' %
            (st_now, random.randint(1, _MAX), random.randint(0, _MAX),
             random.randint(0, _MAX), random.randint(1, _MAX)))
    sleep_time = random.uniform(0.1, 2)
    time.sleep(sleep_time)
    write_in_log()


if __name__ == '__main__':
    write_in_log()
