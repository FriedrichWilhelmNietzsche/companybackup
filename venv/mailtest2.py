1、目标文件夹：D:\mydev\python
2、取第1步中的目标文件夹，自动压缩生成压缩文件zip
3、将第2步中生成的zip文件自动以附件的形式发送到指定邮箱，如762193719@qq.com

项目代码：
我把项目命名为codeManager，主要包含两个module：
1、emailManager，作为发送邮件的handler
2、zipManager，作为压缩文件的handler

项目目录结构如下：
1、emailManager
    [1] __init__.py，作为module import的必要文件
    [2] email_manager.py，发送邮件的必要算法
2、zipManager
    [1] __init__.py，作为module import的必要文件
    [2] zip_manager.py，压缩文件的必要算法
3、run.py，总入口文件

python：自动压缩指定文件夹作为附件发送邮件到指定邮箱

以下是各文件的源代码：
email_manager.py

# -*- coding: utf-8 -*-

'''
发送邮件
'''

import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path
import mimetypes
import os
from os.path import join, getsize
import traceback

# 解决乱码问题
import sys

reload(sys)
SYS_ENCODING = 'cp936'  # 定义系统编码
sys.setdefaultencoding(SYS_ENCODING)  # 设置默认编码


class EmailManager:
    '''
    send email to the given email address automatically
    '''

    def __init__(self, **kw):
        ' 构造函数 '
        self.kw = kw

        self.smtp_server = "smtp.163.com"
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 10M

    def run(self):
        # 总入口
        try:
            # 初始化
            self.__my_init()
            # 登录SMTP服务器，验证授权
            server = self.get_login_server()
            # 生成邮件主体内容
            main_msg = self.get_main_msg()
            # 生成邮件附件内容
            file_msg = self.get_attach_file_msg()

            if file_msg is not None:
                main_msg.attach(file_msg)

            # 得到格式化后的完整文本
            fullText = main_msg.as_string()

            # 发送邮件
            server.sendmail(self.msg_from, self.receiver, fullText)

        except Exception, e:
            print
            e

            exstr = traceback.format_exc()
            print
            exstr

            server.quit()
            exit()

    def get_main_msg(self):
        ' 生成邮件主体内容 '
        # 构造MIMEMultipart对象做为根容器
        main_msg = email.MIMEMultipart.MIMEMultipart()

        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        text_msg = email.MIMEText.MIMEText(self.msg_content, _charset="utf-8")
        main_msg.attach(text_msg)

        # 设置根容器属性
        main_msg['From'] = self.msg_from
        main_msg['To'] = self.msg_to
        main_msg['Subject'] = self.msg_subject
        main_msg['Date'] = self.msg_date

        return main_msg

    def get_attach_file_msg(self):
        ' 生成邮件附件内容 '
        if self.attach_file is not None and self.attach_file != "":
            try:
                self.validate_file_size()

                data = open(self.attach_file, 'rb')
                ctype, encoding = mimetypes.guess_type(self.attach_file)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
                file_msg.set_payload(data.read())
                data.close()

                email.Encoders.encode_base64(file_msg)  # 把附件编码

                ## 设置附件头
                basename = os.path.basename(self.attach_file)
                file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头

                return file_msg
            except Exception, e:
                print
                e
                return None

        else:
            return None

    def get_login_server(self):
        ' 登录SMTP服务器，验证授权信息 '
        server = smtplib.SMTP(self.smtp_server)
        server.login(self.server_username, self.server_pwd)  # 仅smtp服务器需要验证时

        return server

    def validate_file_size(self):
        ' 验证文件大小是否合法 '
        if getsize(self.attach_file) > self.MAX_FILE_SIZE:
            raise Exception(u'附件过大，上传失败')

    def __my_init(self):
        ' 配置初始化 '
        # 邮箱登录设置
        self.server_username = self.__get_cfg('server_username')
        self.server_pwd = self.__get_cfg('server_pwd')

        # 邮件内容设置
        self.receiver = self.__get_cfg('msg_to')

        self.msg_from = self.server_username
        self.msg_to = ','.join(self.__get_cfg('msg_to'))
        self.msg_subject = self.__get_cfg('msg_subject')
        self.msg_date = self.__get_cfg('msg_date')
        self.msg_content = self.__get_cfg('msg_content')

        # 附件
        self.attach_file = self.__get_cfg('attach_file', throw=False)

    def __get_cfg(self, key, throw=True):
        ' 根据key从**kw中取得相应的配置内容 '
        cfg = self.kw.get(key)
        if throw == True and (cfg is None or cfg == ''):
            raise Exception(unicode("配置不能为空！", 'utf-8'))

        return cfg


zip_manager.py
# coding=utf-8

'''
压缩文件夹，生成zip文件
'''

import os, zipfile
from os.path import join
from datetime import date
from time import time
import traceback

# 解决乱码问题
import sys

reload(sys)
SYS_ENCODING = 'cp936'  # 定义系统编码
sys.setdefaultencoding(SYS_ENCODING)  # 设置默认编码


class ZipManager:
    '''
    zip the given folder automatically
    '''

    def __init__(self):
        ' 构造函数 '
        pass

    @staticmethod
    def zip_dir(dirname, zipfilename):
        ' 压缩指定文件夹 '
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    # hard code，原有压缩文件跳过
                    if name.endswith('.zip'):
                        continue
                    # hard code end
                    filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            # print arcname
            zf.write(tar, arcname)
        zf.close()

    @staticmethod
    def unzip_file(zipfilename, unziptodir):
        ' 解压缩指定文件夹 '
        if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777)
        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            name = name.replace('\\', '/')

            if name.endswith('/'):
                os.mkdir(os.path.join(unziptodir, name))
            else:
                ext_filename = os.path.join(unziptodir, name)
                ext_dir = os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir): os.mkdir(ext_dir, 0777)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()


# 测试函数
if __name__ == "__main__":
    folder = r'D:\ruansz\code\python\codeManager\zipManager\test'
    filename = 'test.zip'
    dirbase = r'test'
    targetbase = 'D:' + '/'

    ZipManager.zip_folder(folder, filename, dirbase=dirbase)

run.py

# coding=utf-8

"""

codeManager，自动把本机指定目录下的文件夹打成压缩包，并且作为附件发邮件给指定邮箱，作为备份
2016-06-29 by ruansz

"""

# 解决乱码问题
import sys

reload(sys)
SYS_ENCODING = 'cp936'  # 定义系统编码
sys.setdefaultencoding(SYS_ENCODING)  # 设置默认编码

import email.MIMEBase
import time

# 自定义包导入
from zipManager import zip_manager
from emailManager import email_manager


# 定义一个log函数
def log(msg):
    print
    time.strftime('%Y-%m-%d %H:%M:%S'), ': ', msg


# run
if __name__ == '__main__':
    log(u'进入run函数')

    log(u'开始读取压缩配置参数')
    # 定义配置参数
    # 1、压缩配置
    timestr = time.strftime('%Y%m%d%H%M%S')  # 生成日期时间字符串，作为压缩文件的版本号
    folder = r'D:\mydev\python'  # 压缩目标文件夹
    target = r'D:\mydev\python\python_v' + timestr + r'.zip'  # 压缩后的名称

    log(u'压缩源文件夹：' + folder)
    log(u'压缩输出路径：' + target)

    log(u'开始生成压缩文件')
    zip_manager.ZipManager.zip_dir(folder, target)
    log(u'生成压缩文件结束')

    log(u'开始读取邮件发送配置参数')
    # 2、发送邮件配置
    mail_cfg = {
        # 邮箱登录设置，使用SMTP登录
        'server_username': '你的邮箱',
        'server_pwd': '你的邮箱密码',

        # 邮件内容设置
        'msg_to': ['papa0728@163.com', '762193719@qq.com', 'sizhe@staff.sina.com.cn'],  # 可以在此添加收件人
        'msg_subject': u'我的python代码备份' + timestr,
        'msg_date': email.Utils.formatdate(),
        'msg_content': u"我的python代码备份" + timestr,

        # 附件
        'attach_file': target
    }
    log(u'读取邮件发送配置参数：')
    log(u'server_username：' + str(mail_cfg.get('server_username')))
    log(u'server_pwd：' + str(mail_cfg.get('server_pwd')))
    log(u'msg_to：' + str(mail_cfg.get('msg_to')))
    log(u'msg_subject：' + str(mail_cfg.get('msg_subject')))
    log(u'msg_date：' + str(mail_cfg.get('msg_date')))
    log(u'msg_content：' + str(mail_cfg.get('msg_content')))
    log(u'attach_file：' + str(mail_cfg.get('attach_file')))

    # 实例化manager对象
    log(u'开始创建EmailManager')
    email_manager = email_manager.EmailManager(**mail_cfg)
    log(u'开始发送邮件')
    email_manager.run()
    log(u'发送完成')
    log(u'程序结束')