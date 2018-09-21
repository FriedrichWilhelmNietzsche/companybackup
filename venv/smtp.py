#! /usr/bin/env python  
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime as dt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import partial

def send_mail():
    # 读取测试报告内容
    with open( report_file, 'r', encoding='UTF-8') as f:
        content = f.read()

    msg = MIMEMultipart('mixed')
    # 添加邮件内容
    #msg_html = MIMEText(content, 'html', 'utf-8')
    #msg.attach(msg_html)
    msg_html = MIMEText("来自服务器资料备份", 'html', 'utf-8')
    msg.attach(msg_html)

    # 添加附件
    msg_attachment = MIMEText(content, 'html', 'utf-8')
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
        # 连接邮件服务器
        s = smtplib.SMTP(mail_host, 25)
        # 登陆
        s.login(mail_user, mail_pwd)
        # 发送邮件
        s.sendmail(mail_user, mail_to+mail_cc, msg.as_string())
        # 退出
        s.quit()
    except Exception as e:
        print ("Exceptioin ", e)



if __name__ == '__main__':
    # 邮件服务器
    mail_host = 'smtp.163.com'
    # 发件人用户名
    mail_user = '15555706876@163.com'
    # 授权密码，非登陆密码
    mail_pwd = 'David123'
    # 邮件标题
    mail_subjet = u'NoseTests_测试报告_{0}'.format(dt.now().strftime('%Y%m%d'))
    # 收件人地址list
    mail_to = ['2657070472@qq.com','david.lee@dediprog.com.cn']
    mail_cc = ['15555706876@163.com']
    mail_bcc = ['chinayixia@icloud.com']
    # 测试报告名称
    current_time =  time.strftime('%Y%m%d',time.localtime( time.time() ))
    filename = str ( current_time )
    print(filename)
    path = r'C:\Users\Administrator\Desktop'
    print(os.listdir(  path ))
    for file in os.listdir(path):
        print( file.split(".")[0] )
        if str( file.split(".")[0] ) == filename:
            file_dir = os.path.join(path, file)
            print(file_dir)
            report_file = file_dir
        else:
            print("something maybe wrong")



    # 发送测试报告邮件
    print ('Send Test Report Mail Now...')
    send_mail()



"""
参考：https://m.aliyun.com/jiaocheng/524490.html
"""