#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
# IP显示物理位置

##############################
# import geoip2.database
# #City 文件为包含城市信息数据库，
# # Country 文件为国家信息数据库。
# #http://dev.maxmind.com/zh-hans/geoip/geoip2/geolite2-%E5%BC%80%E6%BA%90%E6%95%B0%E6%8D%AE%E5%BA%93/
# #http://geoip2.readthedocs.io/en/latest/
# #http://geoip2.readthedocs.io/en/latest/#geoip2.records.country
# if __name__ == "__main__":
#     #reader = geoip2.database.Reader('GeoLite2-Country.mmdb')  #找不到调用方法
#     #response = reader.enterprise('180.124.237.29')
#     #########################################
#     reader = geoip2.database.Reader('system/ip_db/GeoLite2-City.mmdb')  #City 文件为包含城市信息数据库，
#     response = reader.city('180.124.237.29')
#     print response.country.iso_code  #CN  两个字符的ISO 3166-1α代码为国
#     print response.country.name   #China  基于区域的国家名单传递给构造函数。
#     print response.country.names['zh-CN']  #中国 一本字典，该字典的键是区域设置代码和值的名称。
#     print response.subdivisions.most_specific.name  #Jiangsu 基于区域细分的名单传递给构造函数。
#     print response.subdivisions.most_specific.names['zh-CN']  #江苏省 一本字典，该字典的键是区域设置代码和值的名称
#     print response.city.name  #Nanjing
#     print response.city.names['zh-CN']  #南京
#     print response.continent.name #Asia
#     print response.continent.names['zh-CN'] #亚洲
#
#     # print response.subdivisions.most_specific.iso_code  #32 这是一个长三个字符的字符串，包含了ISO 3166-2代码细分部分。
#     # print response.postal.code  #None
#     # print response.location.latitude  #32.0617
#     # print response.location.longitude #118.7778
#     reader.close()



##############################


##############################
####################################################################
from struct import *
import urllib2
import string
import re
import sys
import socket
def ip2string( ip ):
    a = (ip & 0xff000000) >> 24
    b = (ip & 0x00ff0000) >> 16
    c = (ip & 0x0000ff00) >> 8
    d = ip & 0x000000ff
    return "%d.%d.%d.%d" % (a,b,c,d)

def string2ip( str ):
    ss = string.split(str, '.')
    ip = 0L
    for s in ss: ip = (ip << 8) + string.atoi(s)
    return ip

class IPSearch:
    def __init__(self,ip_file):
        self.ipdb=open(ip_file,'rb')
        str=self.ipdb.read(8)
        self.first_index ,self.last_index =unpack("II",str)

    def getIPLocation(self,ip):
        IP=string2ip(ip)
        #print IP
        count=(self.last_index-self.first_index)/7+1
        left=0
        right=count
        middle=(right-left)/2+left
        while True:
            if right-left==1:
                #print 'result:%s'%left
                return left
            offset=self.first_index+middle*7
            self.ipdb.seek(offset)
            temp=unpack("I",self.ipdb.read(4))[0]
            #print 'left:%s right:%s middle:%s value:%d' %( left,right,middle,temp  )
            if IP<temp:
                right=middle
            elif IP>temp:
                left=middle
            else:
                return middle
            middle=(right-left)/2+left
    def readpos(self,seek):
        self.ipdb.seek(seek)
        num=self.ipdb.read(3)
        (h,l)=unpack("HB",num)
        return (l<<16)+h

    def find(self,ip):
        ipIndex=self.getIPLocation(ip)
        offset=self.first_index+ipIndex*7+4
        pos_num=self.readpos(offset)
        #print pos_num
        return self.getArea(pos_num+4,True)


    def getString(self,offset):
        self.ipdb.seek(offset)
        result=''
        i=0
        word=unpack("B",self.ipdb.read(1))[0]
        while word!=0:
            i+=1
            word=unpack("B",self.ipdb.read(1))[0]
        self.ipdb.seek(offset)
        result=self.ipdb.read(i)
        #print result
        return result
    def getArea(self,offset,deep):
        self.ipdb.seek(offset)
        area1=''
        area2=''
        str=self.ipdb.read(1)
        firstw=unpack("B",str)[0]
        if firstw==1 and deep:
            return self.getArea(self.readpos(self.ipdb.tell()),True)
        elif firstw==2  and deep:
            area1=self.getArea(self.readpos(self.ipdb.tell()),False)
            area2=self.getArea(offset+4,False)
            return (area1,area2)
        elif firstw==2 and  not deep:
            return self.getArea(self.readpos(offset+1),False)
        else:
            if deep:
                area1=self.getString(self.ipdb.tell()-1)
                area2=self.getString(self.ipdb.tell())
                return (area1,area2)
            else:
                area1=self.getString(self.ipdb.tell()-1)
                return area1

class C_hoset():
    def __init__(self):
        self.tt=IPSearch('system/ip_db/QQWry.dat')

    def www_data(self,www):   #'IP/地理位置/网站标题'
        data=u""
        try:
            ip=self.www_ping_ip(www)  #ping域名转IP
            data+=str(ip)+u"/"
            dlwz=self.www_ip(ip)  #显示IP地理位置
            data+=dlwz.decode('utf-8')
            #data+=u"%s/%s/%s" % (ip, dlwz.decode('utf-8'),title.decode('utf-8'))
            return data
        except:
            return data

    def www_ip(self,IP):   #显示IP地理位置
        try:
            (area1,area2)=self.tt.find(IP)
            return "%s-%s"%(area1.decode('gb2312').encode('utf-8'),area2.decode('gb2312').encode('utf-8'))
        except:
            return 0

    def www_ping_ip(self,WWW):  #域名转IP
        try:
            result = socket.getaddrinfo(WWW, None)
            return result[0][4][0]
        except:
            return 0
####################################################################

# if __name__=='__main__':
#        h=C_hoset()
#        data=h.www_data(url_www("http://www.bizschool.cn/plus/90sec.php"))   #'IP/地理位置/网站标题'
#        print data   #'IP/地理位置/网站标题'

    #    data=""
    #    s0,s1=open_file(data)
    #    print s0,"---",s1




