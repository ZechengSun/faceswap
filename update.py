#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ftplib import FTP
import os
import time
import socket
import json
import tkinter.messagebox
import sys
import math
import threading
import ftp_threading



tkinter.Tk().withdraw()
class MyFTP:

    def __init__(self, host, port=21):
        """ 初始化 FTP 客户端
        参数:
                 host:ip地址

                 port:端口号
        """
        # print("__init__()---> host = %s ,port = %s" % (host, port))

        self.host = host
        self.port = port
        self.ftp = FTP()
        # 重新设置下编码方式
        self.ftp.encoding = 'gbk'
        self.log_file = open("log.txt", "a")
        self.file_list = []

    def login(self, username, password):
        """ 初始化 FTP 客户端
            参数:
                  username: 用户名

                 password: 密码
            """
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            # 0主动模式 1 #被动模式
            self.ftp.set_pasv(1)
            # 打开调试级别2，显示详细信息
            # self.ftp.set_debuglevel(2)

            #self.debug_print('开始尝试连接到 %s' % self.host)
            self.ftp.connect(self.host, self.port)
            #self.debug_print('成功连接到 %s' % self.host)

            #self.debug_print('开始尝试登录到 %s' % self.host)
            self.ftp.login(username, password)
            #self.debug_print('成功登录到 %s' % self.host)

            #self.debug_print(self.ftp.welcome)
        except Exception as err:
             tkinter.messagebox.showinfo("服务器停运了", "555~Ely养不起服务器，所以停运了。\n离线状态软件任然可以正常使用，有问题邮箱联系吧!\n错误描述为：%s" % err)
             my_ftp.close()


    def size(self,local_file, remote_file):
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:
            self.debug_print("错误：%s" % err)
            remote_file_size = 0

        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as err:
            self.debug_print("错误：%s" % err)
            local_file_size = 0
        return  local_file_size, remote_file_size


    def is_same_size(self, local_file, remote_file):
        """判断远程文件和本地文件大小是否一致

           参数:
             local_file: 本地文件

             remote_file: 远程文件
        """

        local_file_size, remote_file_size = self.size(local_file, remote_file)

       # self.debug_print('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
        if local_file=="temp.json":
            return 0
        if local_file=="update.json":
            return 0
        if remote_file_size == local_file_size:
            return 1
        else:
            return 0



    def progress_bar(self,local_file, remote_file):
        total = self.ftp.size(remote_file)
        part = total / 50  # 2%数据的大小
        end_t=0
        end_por = 0
        while(1):
            start_t=time.time()
            portion = os.path.getsize(local_file)
            count = math.ceil(portion / part)
            # print(portion, total, part, count)
            sys.stdout.write('\r')
            v=(portion-end_por)/((start_t-end_t)*1000)
            end_por = portion
            #  [%:[      -50s:留50空格要填     %.2f:保留浮点数后两位   %%:%
            sys.stdout.write(('[%-50s]%.2f%%  %.2fkb/s  %.2fMB/%.2fMB' % (('=' * count),portion / total * 100,v,portion/1024/1024,total/1024/1024)))
            sys.stdout.flush()
            end_t = time.time()
            time.sleep(0.5)


            if portion >= total:

                sys.stdout.write('\n')
                break



    def download_file(self, local_file, remote_file,i):
        """从ftp下载文件
            参数:
                local_file: 本地文件

                remote_file: 远程文件
        """
        method = ["wb", "ab+"]
        if self.is_same_size(local_file, remote_file):
            if local_file!="temp.json":
                if local_file!="update.json":
                    self.debug_print('%s 无更新，无需下载' % local_file)
                    return

        else:
            if local_file != "temp.json":
                self.debug_print("download_file()---> local_path = %s ,remote_path = %s" % (local_file, remote_file))
            try:
                if local_file != "temp.json":
                    self.debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % local_file)
                    t = threading.Thread(target=self.progress_bar, args=(local_file, remote_file,))
                    t.start()
                buf_size = 1024
                file_handler = open(local_file, method[i])
                local_file_size = os.path.getsize(local_file)
                self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size,local_file_size)
                file_handler.close()
            except Exception as err:
                self.debug_print('下载文件出错，出现异常：%s ' % err)
                return




    def download_file_tree(self, local_path, remote_path,i):
        """从远程目录下载多个文件到本地目录
                       参数:
                         local_path: 本地路径

                         remote_path: 远程路径
                """
        print("download_file_tree()--->  local_path = %s ,remote_path = %s" % (local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.debug_print('远程目录%s不存在，继续...' % remote_path + " ,具体错误描述为：%s" % err)
            return

        if not os.path.isdir(local_path):
            self.debug_print('本地目录%s不存在，先创建本地目录' % local_path)
            os.makedirs(local_path)

        self.debug_print('切换至目录: %s' % self.ftp.pwd())

        self.file_list = []
        # 方法回调
        self.ftp.dir(self.get_file_list)

        remote_names = self.file_list
        self.debug_print('远程目录 列表: %s' % remote_names)
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            local = os.path.join(local_path, file_name)

            if file_type == 'd':

                print("download_file_tree()---> 下载目录： %s" % file_name)
                self.download_file_tree(local, file_name,i)
                self.ftp.cwd("..")
                self.debug_print('返回上层目录 %s' % self.ftp.pwd())

            elif file_type == '-':

                print("download_file()---> 下载文件： %s" % file_name)
                self.download_file(local, file_name,i)



        return True


    def close(self):
        """ 退出ftp
        """
        self.debug_print("close()---> FTP退出")
        self.ftp.quit()
        self.log_file.close()

    def debug_print(self, s):
        """ 打印日志
        """
        self.write_log(s)

    def deal_error(self, e):
        """ 处理错误异常
            参数：
                e：异常
        """
        log_str = '发生错误: %s' % e
        self.write_log(log_str)
        sys.exit()

    def write_log(self, log_str):
        """ 记录日志
            参数：
                log_str：日志
        """
        time_now = time.localtime()
        date_now = time.strftime('%Y-%m-%d', time_now)
        format_log_str = "%s ---> %s \n " % (date_now, log_str)
        print(format_log_str)
        self.log_file.write(format_log_str)

    def get_file_list(self, line):
        """ 获取文件列表
            参数：
                line：
        """
        file_arr = self.get_file_name(line)
        # 去除  . 和  ..
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_file_name(self, line):
        """ 获取文件名
            参数：
                line：
        """
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr

def get_json(content):
    # 获取服务器版本信息
    with open("temp.json", 'r', encoding='utf-8') as f:
        r_content = json.loads(f.read())

    # 对比版本信息
    updated = True
    if content['version'] < r_content['version']:
        updated = False
    return updated



with open("update.json", 'r', encoding='utf-8') as f:
    content = json.loads(f.read())

my_ftp = MyFTP(content["ip"])
my_ftp.login(content["username"], content["keyword"])

#下载单个文件(替换当地文件)
my_ftp.download_file("temp.json", "./faceswap/temp.json",0)

if not get_json(content):
    qa = tkinter.messagebox.askyesno("新版本faceswap", "Ely熬夜赶进度推出新版本faceswap了!是否更新？")
    #关闭faceswap进程
    try:
        os.system(r'taskkill /F /IM faceswap.exe')
    except Exception as e:
        print(":%s"%e)
    if qa:
        my_ftp.download_file("update.json", "./faceswap/update.json", 0)
        # 下载目录
        # my_ftp.download_file_tree(".\\", "./test/",0)
        my_ftp.download_file_tree(".\\", "./faceswap/", 0)
        # 打开faceswap
        os.system('faceswap.exe')
        my_ftp.close()
else:

        # my_ftp.download_file_tree(".\\", "./test/",1)
        my_ftp.download_file_tree(".\\", "./faceswap/",1)
        with open("update.json", 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        print("欢迎使用最新版本faceswap%s" % content["version"])


