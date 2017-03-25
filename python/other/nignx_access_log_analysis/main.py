# -*- coding:utf-8 -*-
import re

import datetime
import pyinotify
from django.core.mail import send_mail

time_key = datetime.datetime.now()
time_ip_list = [[] for i in range(120)]


class ProcessTransientFile(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        line = file.readline()
        if line:
            # 倒数第三项是ip
            line_list = line.split(' ')
            try:
                ip = line_list[-3]
                time = line_list[3]
                # 检测ip是否合法
                ip_pattern = r'([1-9]|[1-9]\d|1\d{2}|2[1-4]\d|25[0-5])' \
                             r'(.([0-9]|[1-9]\d|1\d{2}|2[1-4]\d|25[0-5])){2}.' \
                             r'([1-9]|[1-9]\d|1\d{2}|2[1-4]\d|25[0-5])'
                if re.match(ip_pattern, ip):
                    time = time[1:]
                    _time = datetime.datetime.strptime('%d/%m/%Y:%T', time)
                    now = datetime.datetime.now()
                    global time_key
                    if now - datetime.timedelta(seconds=1) > time_key:
                        time_key = now
                        time_ip_list.pop(0)
                        time_ip_list.append([ip])
                    else:
                        time_ip_list[-1].append(ip)

                    for x in time_ip_list:
                        for y in x:
                            ip_dict = {}
                            ip_dict.setdefault(y, 0)
                            ip_dict[y] += 1
                            if ip_dict[y] > 60:
                                # 发邮件
                                pass
                                # send_mail('nginx_access_log_analysis', '%s: %s' % (time_key, y),
                                #           'david.zhang@maiziedu.com', ['soso@maiziedu.com'])
            except Exception:
                pass


filename = '/tmp/tmp/out.log'
file = open(filename, 'r')
# 移到末尾
file.seek(0, 2)

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)

wm.watch_transient_file(filename, pyinotify.IN_MODIFY, ProcessTransientFile)
notifier.loop()


