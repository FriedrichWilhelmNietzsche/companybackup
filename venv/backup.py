#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 自动运行服务器备份程序，并将备份文件进行邮件发送
# 现在是发送指定路径下的文件，如何发送指定路径下未知文件夹中的所有文件？——待解决

import os
import time
from datetime import datetime as dt
from pynput.mouse import Controller as Mouse
from pynput.mouse import Button as bt
from pynput.keyboard import Controller as Keyboard
from pynput.keyboard import Key
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import partial

"""
# 自动运行服务器备份程序
def TellHer(ms, kb):
    os.startfile(r'C:\LYWINSR5X\LyBackUp.exe')  # 运行
    time.sleep(0.3)

    kb.type("LY")  # 登陆
    kb.press(Key.enter)
    kb.release(Key.enter)
    kb.type("ly")
    kb.press(Key.enter)
    kb.release(Key.enter)
    time.sleep(30)

    ms.position = (255, 335)  # 日期
    ms.click(bt.left, 2)
    # ms.press(bt.left)
    # ms.release(bt.left)
    time.sleep(3)

    ms.position = (296, 562)  # 全选
    ms.click(bt.left, 2)
    time.sleep(3)

    ms.position = (639, 566)  # 确定
    ms.click(bt.left, 2)
    time.sleep(1800)

    ms.position = (565, 429)  # 确定
    ms.click(bt.left, 2)

    print("Sucess")

"""


def send_mail():
    with open(report_file, 'r', encoding='UTF-8') as f:  # 读取备份文件内容
        content = f.read()
    msg = MIMEMultipart('mixed')

    # msg_html = MIMEText(content, 'html', 'utf-8')
    # msg.attach(msg_html)
    msg_html = MIMEText("来自服务器资料备份", 'html', 'utf-8')  # 添加邮件内容
    msg.attach(msg_html)

    msg_attachment = MIMEText(content, 'html', 'utf-8')  # 添加为附件
    msg_attachment["Content-Disposition"] = 'attachment; filename="{0}"'.format(report_file)
    msg.attach(msg_attachment)

    msg['subject'] = mail_subjet
    msg['from'] = mail_user
    msg['to'] = ','.join(mail_to)
    msg['cc'] = ','.join(mail_cc)
    receive = mail_to
    receive.extend(mail_cc)
    receive.extend(mail_bcc)
    try:
        s = smtplib.SMTP(mail_host, 25)  # 连接邮件服务器
        s.login(mail_user, mail_pwd)  # 登陆
        s.sendmail(mail_user, mail_to, msg.as_string())  # 发送邮件
        s.quit()  # 退出
    except Exception as e:
        print("Exceptioin ", e)


if __name__ == '__main__':


   # ms = Mouse()
   # kb = Keyboard()
    #for i in range(2):
    #    TellHer(ms, kb);


       mail_host = 'smtp.163.com'  # 邮件服务器
       mail_user = '15555706876@163.com'  # 发件人用户名
       mail_pwd = 'David123'  # 授权密码，非登陆密码
       mail_subjet = u'Test_备份测试_{0}'.format(dt.now().strftime('%Y%m%d'))  # 邮件标题
       mail_to = ['david.lee@dediprog.com.cn']  # 收件人地址list
       mail_cc = ['2657070472@qq.com']  # 抄送
       mail_bcc = ['2657070472@qq.com']  # 暗送
       current_time = time.strftime('%Y%m%d', time.localtime(time.time()))  # 测试报告名称
       filename = str(current_time)
       # print(filename)
       path = r'E:'
       # print(os.listdir(  path ))
       for file in os.listdir(path):
           #    print( file.split(".")[0] )
           if str(file.split(".")[0]) == filename:
               file_dir = os.path.join(path, file)
               #       print(file_dir)
               report_file = file_dir

       print('Send Test Report Mail Now...')  # 发送备份资料邮件
       send_mail()
"""

缺点：1）一直运行；2）备份期间使用鼠标键盘控制
备份期间不能有第二个用户访问，否则程序崩溃，备份中断
"""
