#!/usr/bin/python
# coding:utf8
# *************************************************************************
# File Name: log.py
# Author: snailwalker
# Mail: qiyu1001@gmail.com
# Created Time: 五  7/31 15:12:16 2015
# *************************************************************************

import os
from conf import *
from mail import SendMail
import datetime
import time


class LogAnalyse:

    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, file_path):
        self.file_path = file_path

    def get_lines(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')

        logfile = open(self.file_path, 'r')
        result = [i for i in logfile]
        logfile.close()
        return result

    def get_error_detail_info(self):
        temp_list = self.get_lines()
        return [j for j in [i for i in temp_list if i.find('[DEBUG]') == -1] if j.find('[INFO]') == -1]

    def get_error_lines(self):
        temp_list = self.get_lines()
        return [i for i in temp_list if i.find('[ERROR]') != -1]

    def get_error_counts(self):
        temp_list = self.get_error_lines()
        result = {}
        for i in temp_list:
            # j = i[26:]
            if not i in result:
                result[i] = 1
            else:
                result[i] += 1
        return result

    def get_latest_log(self, minute):
        result = []
        latest_min = datetime.datetime.now() - datetime.timedelta(minutes=minute)
        for i in self.get_lines():
            try:
                log_time = datetime.datetime.strptime(i[1:20], self.ISOTIMEFORMAT)
            except Exception:
                continue
            if log_time > latest_min:
                result.append(i)
        return result


def main():
    temp_file = os.path.sep + 'data ' + os.path.sep + 'log' + os.path.sep + 'item' + os.path.sep +'root.log'
    la = LogAnalyse(temp_file)
    error_log = open('error.log', 'w')
    a = ''
    for k, v in la.get_error_counts().items():
        error_log.write(k.strip('\n').decode("utf8") + "出现次数：" + str(v) + '\n')
        a = a + k.strip('\n').decode("utf8") + "出现次数：" + str(v) + '\n'
    
    tempList = la.get_latest_log(5)

    # 初始化发送邮件类
    sml = SendMail(EMAIL_USER, EMAIL_PASSWORD, EMAIL_HOST)
    # 设置邮件信息
    text_type = 'plain'
    sml.setMailInfo(TO_EMAIL, EMAIL_HEADER, a, text_type, os.getcwd() + os.path.sep + 'error.log')
    sml.sendMail()
    for i in tempList:
        if 'Disconnected' in i:
            sml.reinitMailInfo()
            sml.setMailInfo(TO_EMAIL, "zookeeper挂了", "zookeeper又尼玛挂了，赶紧去看看啊！！！", text_type)
            sml.sendMail()
            break
    error_log.close()

if __name__ == '__main__':
    main()
