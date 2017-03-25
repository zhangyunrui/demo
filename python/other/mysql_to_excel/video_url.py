# -*- coding: utf-8 -*-

import xlwt
import MySQLdb


def mysql_to_xlsx():
    conn = MySQLdb.connect(
        host='rm-bp1q9x0s7w5igdb75o.mysql.rds.aliyuncs.com',
        port=3306,
        user='dev',
        passwd='65fg_weArd',
        db='dev_lps_20170207',
        charset='utf8'
    )

    cur = conn.cursor()

    cur.execute("""SELECT
      s.name,
      t.name,
      k.name,
      l.name,
      l.video_url
    FROM mz_course_stage AS s
      JOIN mz_lps3_stagetaskrelation AS str ON (s.id = str.stage_id AND s.career_course_id = 13 AND lps_version = '3.0')
      JOIN mz_lps3_task AS t ON t.id = str.task_id
      JOIN mz_lps3_taskknowledgerelation AS tkr ON tkr.task_id = t.id
      JOIN mz_lps3_knowledge AS k ON k.id = tkr.knowledge_id
      JOIN mz_lps3_knowledgeitem AS ki ON (ki.parent_id = tkr.knowledge_id AND ki.obj_type = 'LESSON')
      JOIN mz_course_lesson AS l ON l.id = ki.obj_id
    ORDER BY s.`index`, str.`index`, tkr.`index`, ki.`index`;""")

    data = cur.fetchall()

    _file = xlwt.Workbook()
    table = _file.add_sheet('python_video_url')

    r = 0

    for row in data:
        c = 0
        for col in row:
            table.write(r, c, col)
            c += 1
        r += 1

    _file.save('/home/cloud/Desktop/python_video_url.xlsx')


if __name__ == '__main__':
    mysql_to_xlsx()
