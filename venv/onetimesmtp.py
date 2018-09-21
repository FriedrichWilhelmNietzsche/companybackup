import smtplib
import email.mime.text
import email.mime.multipart

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def get_type_file(keyword='.txt'):  # 这里可以更改扩展名如.doc,.py,.zip等等
    # 打印当前的工作目录
    print("当前目录为: ", os.getcwd())

    # 列举当前工作目录下的文件名
    files = os.listdir()
    keyword = keyword
    filelist = []

    i = 0
    for file in files:
        if keyword in file:
            i = i + 1
            print(i, file)
            filelist.append(file)

    return filelist


def send_email(filelist, content=""):
    smtpHost = 'smtp.139.com'  # 139邮箱SMTP服务器
    sendAddr = '123456789@163.com'
    password = 'David123'  # 163邮箱,则为授权码
    receiver = '2657070472@qq.com'
    subject = "测试发送多个文件"
    content = '来自pythton邮件'

    msg = MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = receiver
    msg['subject'] = subject

    txt = MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)  # 添加邮件正文

    # 添加附件,传送filelist列表里的文件
    filename = ""
    i = 0
    for file in filelist:
        i = i + 1
        filename = file
        # print(str(i),filename)
        part = MIMEApplication(open(filename, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

    server = smtplib.SMTP(smtpHost, 25)  # SMTP协议默认端口为25
    # server.set_debuglevel(1)  # 出错时可以查看

    server.login(sendAddr, password)
    server.sendmail(sendAddr, receiver, str(msg))
    print("\n"+ str(len(filelist)) + "个文件发送成功")
    server.quit()

"""
def main():
    filelist = get_type_file()
    send_email(filelist)
    main()

"""
if __name__ == '__main__':
    filelist = get_type_file()
    send_email(filelist)
    main()
