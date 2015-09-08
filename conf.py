#!/usr/bin/env python
# coding=utf-8
# *************************************************************************
# File Name: log.py
# Author: snailwalker
# Mail: qiyu1001@gmail.com
# Created Time: 五  7/31 15:12:16 2015
# *************************************************************************
__author__ = 'silent'

EMAIL_HOST = "smtp.163.com"
SENDER_SMTP_PORT = 25
EMAIL_USER = "shangbanredmine@163.com"
EMAIL_PASSWORD = ###
EMAIL_POSTFIX = "163.com"
TO_EMAIL = "qiyu1001@gmail.com"
EMAIL_HEADER = "每日错误日志汇总"
CONTENT_FILE_NAME = "error.log"
ATTACHMENT_FILE_NAME = ['error.log',]
ME = EMAIL_USER + EMAIL_POSTFIX

