#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#coding : gbk
#LOG日志记录
import logging
import logging.config
from logging.handlers import RotatingFileHandler
CONF_LOG = "main.log"
# %(levelno)s: 打印日志级别的数值
# %(levelname)s: 打印日志级别名称
# %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
#   %(filename)s: 打印当前执行程序名
#   %(funcName)s: 打印日志的当前函数
# %(lineno)d: 打印日志的当前行号
#   %(asctime)s: 打印日志的时间
# %(thread)d: 打印线程ID
# %(threadName)s: 打印线程名称
# %(process)d: 打印进程ID
# %(message)s: 打印日志信息
logging.basicConfig(level=logging.DEBUG,
                    #format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    format='time:%(asctime)s py_name:%(filename)s def_Name:%(funcName)s [line:%(lineno)d]--%(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=CONF_LOG,
                    filemode='a+')
#def add_log(): #LOG输出
#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
Rthandler = RotatingFileHandler(CONF_LOG, maxBytes=10*1024*1024,backupCount=20)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)
#################################################################################################


if __name__ == "__main__":
    #add_log()
    logging.debug('This is debug message')
