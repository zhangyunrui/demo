# -*- coding:utf-8 -*-
import re

import datetime
import pyinotify
import time
from django.core.mail import send_mail

FILENAME = '/tmp/tmp/out.log'
FILE = open(FILENAME, 'r')
# 光标移到末尾
FILE.seek(0, 2)

BUF_SIZE = 120
SEC_LIMIT = 60
WARN_IP_COUNT_LIMIT = 10

TIME_KEY = int(time.mktime(datetime.datetime.timetuple(datetime.datetime.now())))
# TIME_KEY = 1484279343
TIME_IP_LIST = [[] for i in range(BUF_SIZE)]
T_FORMAT = '%d/%b/%Y:%H:%M:%S'
IP_DICT = {}
IP_WHITE_LIST = ['192.1.2.3']


class ProcessTransientFile(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        line = FILE.readline()
        if line:
            # 倒数第三项是ip
            line_list = line.split(' ')
            try:
                ip = eval(line_list[-3])
                ac_time = line_list[3]
                ip_pattern = r'([1-9]|[1-9]\d|1\d{2}|2[1-4]\d|25[0-5])' \
                             r'(.([0-9]|[1-9]\d|1\d{2}|2[1-4]\d|25[0-5])){2}.' \
                             r'([1-9]|[1-9]\d|1\d{2}|2[1-4]\d|25[0-5])'
                # 检测ip是否合法
                if re.match(ip_pattern, ip):
                    ac_time = ac_time[1:]  # 去除开头的[
                    # 转成时间戳
                    ac_time_stamp = int(time.mktime(time.strptime(ac_time, T_FORMAT)))
                    global TIME_KEY
                    # 当差值大于1时，TIME_IP_LIST去头加尾
                    while ac_time_stamp - TIME_KEY > 0:
                        TIME_IP_LIST.pop(0)
                        TIME_IP_LIST.append([])
                        TIME_KEY += 1

                    # 保证ac_time_stamp - TIME_KEY == 0，其它的不写入
                    if ac_time_stamp - TIME_KEY == 0:
                        TIME_IP_LIST[-1].append(ip)

                    for x in TIME_IP_LIST[-SEC_LIMIT:]:
                        for y in x:
                            # 如果在白名单里，就不参与
                            if y not in IP_WHITE_LIST:
                                IP_DICT.setdefault(y, 0)
                                IP_DICT[y] += 1
                                if IP_DICT[y] > WARN_IP_COUNT_LIMIT:
                                    # 发邮件
                                    msg = 'time:%s ip:"%s" count:%s' % (ac_time, y, IP_DICT[y])
                                    print msg
                                    # send_mail('nginx_access_log_analysis', msg,
                                    #           'david.zhang@maiziedu.com', ['soso@maiziedu.com'])
            except Exception:
                pass


def nginx_log_moniter():
    # 初始化文件监控器
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm)

    # 监控FILENAME，只监控文件修改，在文件修改时执行ProcessTransientFile
    wm.watch_transient_file(FILENAME, pyinotify.IN_MODIFY, ProcessTransientFile)
    notifier.loop()


nginx_log_moniter()

FILE.close()
