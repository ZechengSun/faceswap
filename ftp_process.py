from ftplib import FTP
import os
import time
import math
import sys
import threading
from multiprocessing import Process
from multiprocessing import Pool


#---------------------------------------------------------------
#将文件分块，比如我们打算采用3个进程去下载同一个文件
# 需要将文件以二进制方式打开，平均分成3块，然后分别启用一个线程去下载一个块：
processList = []
filename="ftp_json.exe"

def downloadFileMultiThreads(threadIndex, remoteFilePath, localFilePath, beginPoint, blockSize, rest=None):
    """
    A sub thread used to download file
    """
    fp = open(localFilePath + filename + '_part.' + str(threadIndex), 'wb')
    callback = fp.write

    # another connection to ftp server, change to path, and set binary mode
    myFtp = FTP('132.232.220.146','ubuntu','jL2zM6ZtyGwww')
    myFtp.cwd(os.path.dirname(remoteFilePath))
    myFtp.voidcmd('TYPE I')

    finishedSize = 0

    # where to begin downloading
    setBeginPoint = 'REST ' + str(beginPoint)
    myFtp.sendcmd(setBeginPoint)

    # begin to download
    beginToDownload = 'RETR ' + os.path.basename(remoteFilePath)
    connection = myFtp.transfercmd(beginToDownload, rest)
    while 1:
        remainedSize = blockSize - finishedSize
        data = connection.recv(remainedSize)
        if not data:
            break

        finishedSize += len(data)

        # make sure the finished data no more than blockSize
        if finishedSize == blockSize:
            callback(data)
            break

        callback(data)

    connection.close()
    fp.close()

class MY_FTP:


    def __init__(self, host, username,password,port=21):
        """ 初始化 FTP 客户端
        参数:
                 host:ip地址

                 port:端口号
        """
        # print("__init__()---> host = %s ,port = %s" % (host, port))

        self.host = host
        self.port = port
        self.username=username
        self.password=password
        self.ftp = FTP()
        # 重新设置下编码方式
        self.ftp.encoding = 'gbk'
        # 0主动模式 1 #被动模式
        self.ftp.set_pasv(0)
        self.ftp.connect(self.host, self.port)
        self.ftp.login(username, password)


    def progress_bar(self,local_file, remote_file):
            total = self.ftp.size(remote_file)
            part = total / 50  # 2%数据的大小
            end_t = 0
            end_por = 0

            while (1):
                start_t = time.time()
                # portion = os.path.getsize(local_file)
                portion = 0

                for root, dirs, files in os.walk(local_file):
                    portion += sum([os.path.getsize(os.path.join(root, name)) for name in files])

                count = math.ceil(portion / part)
                sys.stdout.write('\r')
                v = (portion - end_por) / ((start_t - end_t) * 1000)
                end_por = portion
                #  [%:[      -50s:留50空格要填     %.2f:保留浮点数后两位   %%:%
                sys.stdout.write(('[%-50s]%.2f%%  %.2fkb/s  %.2fMB/%.2fMB' % (
                ('=' * count), portion / total * 100, v, portion / 1024 / 1024, total / 1024 / 1024)))
                sys.stdout.flush()
                end_t = time.time()
                time.sleep(0.5)
                if portion >= total:
                    sys.stdout.write('\n')
                    break





    def setupThreads(self, filePath, localFilePath, threadNumber = 3):


            remoteFileSize = self.ftp.size(filePath)
            blockSize = remoteFileSize // threadNumber
            rest = None
            #threads = []

            for i in range(0, threadNumber - 1):
                print(i)
                beginPoint = blockSize * i


                p1 = Process(target=downloadFileMultiThreads,args=(i, filePath, localFilePath, beginPoint, blockSize, rest,))
                processList.append(p1)


            #最后一块大小
            assigned = blockSize * threadNumber
            unassigned = remoteFileSize - assigned
            lastBlockSize = blockSize + unassigned
            beginPoint = blockSize * (threadNumber - 1)
            p2= Process(target=downloadFileMultiThreads,args = (threadNumber - 1, filePath, localFilePath, beginPoint, lastBlockSize, rest,))
            processList.append(p2)








#----------------------各个文件块进行合并--------------------------------

    def mergerFile(self, localFile, threadNumber):
        '''

            Meger all the sub parts of the file into 1 file
            another thread will be call to do this
        '''

        subThread = threading.Thread(target = self.mergerFileExecutor, args = (localFile, threadNumber,))
        subThread.start()
        # subThread.join()


    def mergerFileExecutor(self, localFile, threadNumber):

        fw = open(localFile+filename, 'wb')
        for i in range(0, threadNumber):
            fname = localFile+"tempfile\\"+ filename+'_part.' + str(i)

            if not os.path.exists(fname):
                break

            fr = open(fname, 'rb')
            data = fr.read()
            fr.close()
            fw.write(data)
            fw.flush()
            os.remove(fname)
        fw.close()
        print("下载%s完成"%filename)


    def sss(self,filePath,localFilePath):
        isExists = os.path.exists(localFilePath + "tempfile\\")
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(localFilePath + "tempfile\\")

        my_ftp.setupThreads(filePath, localFilePath + "tempfile\\", threadNumber=10)
        # 开始执行进程
        for p in processList:
            p.start()

        x = threading.Thread(target=self.progress_bar, args=(localFilePath + "tempfile\\", filePath,))
        x.start()

        for p in processList:
            p.join()

        my_ftp.mergerFile(localFilePath, threadNumber=10)
        my_ftp.ftp.quit()



if __name__ == '__main__':

    host = '132.232.220.146'
    port = 21
    username = 'ubuntu'
    password = 'jL2zM6ZtyGwww'
    my_ftp = MY_FTP(host,username,password)


    filename = "ftp_json.exe"
    filePath="/home/ubuntu/test/"+filename
    localFilePath=".\\"

    my_ftp.sss(filePath, localFilePath)
