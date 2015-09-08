#!/usr/bin/env python3
# coding: utf-8
# *************************************************************************
# File Name: log.py
# Author: snailwalker
# Mail: qiyu1001@gmail.com
# Created Time: 五  7/31 15:12:16 2015
# *************************************************************************
__author__ = 'silent'

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.encoders import encode_base64
from email.header import Header


class SendMail:
    """发送邮件工具类"""

    # 构造函数（用户名，密码，发送服务，端口，是否使用ttls等）
    def __init__(self, user, password, smtp, port=25, usettls=False):
        self.mailUser = user
        self.mailPassword = password
        self.smtpServer = smtp
        self.smtpPort = port
        self.mailServer = smtplib.SMTP(self.smtpServer, self.smtpPort)
        self.mailServer.ehlo()
        if usettls:
            self.mailServer.starttls()
        self.mailServer.ehlo()
        self.mailServer.login(self.mailUser, self.mailPassword)
        self.msg = MIMEMultipart()

    # 对象销毁时,关闭mailserver
    # def __del__(self):
        # self.mailServer.close()

    # 重新初始化邮件信息部分
    def reinitMailInfo(self):
        self.msg = MIMEMultipart()

    # 设置邮件的基本信息（收件人，主题，邮件正文，正文类型html或者plain，可变参数附件列表）
    def setMailInfo(self, receive_user, subject, text, text_type, *attachmentFilePaths):
        self.msg['From'] = self.mailUser
        self.msg['To'] = receive_user

        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(text, text_type, 'utf-8'))
        for attachmentFilePath in attachmentFilePaths:
            self.msg.attach(self.getAttachmentFromFile(attachmentFilePath))

    # 通用方法添加邮件信息
    def addPart(self, part):
        self.msg.attach(part)

    # 发送邮件
    def sendMail(self):
        if not self.msg['To']:
            print "没有收件人，请先设置邮件基本信息"
            return
        self.mailServer.sendmail(self.mailUser, self.msg['To'], self.msg.as_string())
        print('Sent email to %s' % self.msg['To'])

    # 通过路径添加附件
    def getAttachmentFromFile(self, attachmentFilePath):
        part = MIMEBase('application', "octet-stream")
        part.set_payload(str(open(attachmentFilePath, "rb").read()))
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % str(Header(attachmentFilePath, 'utf8')))
        return part