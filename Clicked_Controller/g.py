#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#公用文件  常用函数
import sys,os
#from Clicked_Controller \
import threadpool #线程操作
from Clicked_Controller import log #日志记录

def id_webx(script):  #根据ID判断 网站类型
    try:
        #print script
        if str(script)=="1":
            script="PHP"
        elif str(script)=="2":
            script="ASP"
        elif str(script)=="3":
            script="ASPX"
        else:
            #str(script)=="4":
            script="Customize"
        # if int(script)==1:
        #     script="PHP"
        # elif int(script)==2:
        #     script="ASP"
        # elif int(script)==3:
        #     script="ASPX"
        # else:
        #     script="Customize"
        return script
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))


import re
def re_string_index(data,file_data): #正则查找内容是否存在
    try:
        p = re.compile( r'%s'%(str(file_data)))
        sarr = p.findall(data)
        if len(sarr):
            return 1
        else:
            return 0
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return 0

def if_os(Info):  #判断操作系统
    try:
        #print Info
        Rpath = Info.split('\t')  #分割返回的信息
        #print Rpath
        #OS_data=""  #操作系统
        try:
            if Rpath[2]:
                data=str(Rpath[2]).lower()  #转换成小写
                colours = ["windows","linux","unix"]
                for i in range(0, len(colours)):
                    file_data=colours[i]
                    if re_string_index(data,file_data):
                        #OS_data=file_data
                        #break #跳出
                        return file_data
        except BaseException, e:
            pass

        try:
            #if OS_data=="":  #操作系统
            data=str(Info).lower()  #转换成小写
            colours = ["windows","linux","unix"]
            for i in range(0, len(colours)):
                file_data=colours[i]
                if re_string_index(data,file_data):
                    #OS_data=file_data
                    #break #跳出
                    return file_data
        except BaseException, e:
            pass

        try:
            if Rpath[0]:
                data=str(Rpath[0]).lower()  #转换成小写
                if data=="/" or data=="\\":#判断是不是linux
                    return "linux"
                else:
                    return "windows"
        except BaseException, e:
            pass
        return ""
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return ""


pathx=None
#获取脚本文件的当前路径
def cur_file_dir():
    try:
        #获取脚本路径
        global pathx
        #print "cccccc",pathx
        #path = sys.path[0]
        #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(pathx):
            return pathx
        elif os.path.isfile(pathx):
            return os.path.dirname(pathx)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def GetExt(get_name):#输入路径地址  转换路径
    try:
        get_name=get_name.replace("\r\n","")
        get_name=get_name.replace("\n","")
        if str(get_name).rfind("/"):
            get_name=str(get_name).replace("/", "\\")  #当前路径
        if str(get_name).rfind("\\\\"):
            get_name=str(get_name).replace("\\\\", "\\")  #当前路径
        if not get_name[len(get_name)-1:len(get_name)]=="\\":
            get_name=str(get_name)+"\\"
        if get_name[0:1]=="/" or get_name[0:1]=="\\":#判断是不是linux
            #linux
            get_name=get_name.replace("\\","/")
            get_name=get_name.replace("//","/")
        else:
            #win
            get_name=get_name.replace("/","\\")
        return get_name
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def file_GetExt(get_name):#输入路径地址  转换路径
    try:
        get_name=get_name.replace("\r\n","")
        get_name=get_name.replace("\n","")
        if str(get_name).rfind("/"):
            get_name=str(get_name).replace("/", "\\")  #当前路径
        if str(get_name).rfind("\\\\"):
            get_name=str(get_name).replace("\\\\", "\\")  #当前路径
        if not get_name[len(get_name)-1:len(get_name)]=="\\":
            get_name=str(get_name)+"\\"
        if get_name[0:1]=="/" or get_name[0:1]=="\\":#判断是不是linux
            #linux
            get_name=get_name.replace("\\","/")
            get_name=get_name.replace("//","/")
            if "." in get_name:
                get_name=get_name[0:len(get_name)-1]
        else:
            #win
            get_name=get_name.replace("/","\\")
            if "." in get_name:
                get_name=get_name[0:len(get_name)-1]
        return get_name
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def path_name(path):  #通过路径获取文件名
    try:
        if path[0:1]=="/":#判断是不是linux
            #/homedocs/caches/caches_linkage/caches_data/3397.cache.php
            nPos =path.rfind('/') #查找字符  从尾部查找
            sStr1 = path[nPos+1:len(path)] #复制指定长度的字符
            return sStr1
        else:
            #C:\Program Files (x86)\EasyPHP-5.3.6.0\www\123.txt
            nPos =path.rfind('\\') #查找字符  从尾部查找
            sStr1 = path[nPos+1:len(path)] #复制指定长度的字符
            return sStr1
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return ""

# 模式 	字符表示 	说明
# 0477 	-r--rwxrwx 	所有者仅可读（4），其他及组可读写执行（7）
# 0677 	-rw-rwxrwx 	所有者仅可读写（6），其他及组可读写执行（7）
# 0444 	-r--r--r-- 	所有均仅可读（4）
# 0666 	-rw-rw-rw- 	所有均仅可读写（6）
# 0400 	-r-------- 	所有者仅可读（4），组及其他无任何权限（0）
# 0600 	-rw------- 	所有者仅可读写（6），组及其他无任何权限（0）
# 0470 	-r--rwx--- 	所有者仅可读，组可读写执行，其他则无任何权限
# 0407 	-r-----rwx 	所有者仅可读，其他可读写执行，组则无任何权限
# 0670 	-rw-rwx--- 	所有者仅可读写，组可读写执行，其他则无任何权限
# 0607 	-rw----rwx 	所有者仅可读写，其他可读写执行，组则无任何权限
#######
# 0 = 普通文件。没有设置任何属性。
# 1 = 只读文件。可读写。
# 2 = 隐藏文件。可读写。
# 4 = 系统文件。可读写。
# 16 = 文件夹或目录。只读。
# 32 = 上次备份后已更改的文件。可读写。
# 1024 = 链接或快捷方式。只读。
# 2048 = 压缩文件。只读。
def file_root(root): #根据属性判断文件权限
    try:
        #print root
        root=int(root)
        #ASP 特殊
        if root==0:
            return u"%s/普通文件"%(str(root))
        elif root==1:
            return u"%s/可读写"%(str(root))
        elif root==2:
            return u"%s/可读写.隐藏文件"%(str(root))
        elif root==4:
            return u"%s/可读写.系统文件"%(str(root))
        elif root==16:
            return u"%s/文件夹.只读"%(str(root))
        elif root==32:
            return u"%s/可读写"%(str(root))
        elif root==1024:
            return u"%s/快捷方式.只读"%(str(root))
        elif root==2048:
            return u"%s/压缩文件.只读"%(str(root))
        #
        if root==477:
            return u"0%s/仅可读"%(str(root))
        elif root==677:
            return u"0%s/仅可读写"%(str(root))
        elif root==444:
            return u"0%s/仅可读"%(str(root))
        elif root==555:
            return u"0%s/文件夹.只读"%(str(root))
        elif root==666:
            return u"0%s/仅可读写"%(str(root))
        elif root==400:
            return u"0%s/可读"%(str(root))
        elif root==600:
            return u"0%s/可读写"%(str(root))
        elif root==470:
            return u"0%s/仅可读写执行"%(str(root))
        elif root==407:
            return u"0%s/仅可读"%(str(root))
        elif root==670:
            return u"0%s/可读写执行"%(str(root))
        elif root==607:
            return u"0%s/可读写"%(str(root))

        return u"0%s/null"%(str(root))
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return u"0%s/except"%(str(root))

def run_start_new_thread(name_api):
    try:
        t_h_Thread = threadpool.ThreadPool(1)   #创建多线程  线程池
        t_h_Thread.push("%s"%(name_api)) #self.ShowFileManage_data.thread_Upload_files,self.Upload_files
        t_h_Thread.wait_for_idel(1)
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

if __name__=="__main__":
    print GetExt("C:\Users\Administrator\Desktop\\1111111.asp")
    print GetExt("C:/Users\Administrator\Desktop.html")