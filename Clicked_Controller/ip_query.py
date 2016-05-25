#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
#coding : gbk
#IP调用物理位置
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import qqwry #调用IP纯真数据库
import geoip2.database
#geoip2   #查询数据
reader = geoip2.database.Reader('system/ip_db/GeoLite2-City.mmdb')  #City 文件为包含城市信息数据库，
def geoip2_ip_country(ip):  #查询IP对应的国家缩写
    try:
        response = reader.city(str(ip))
        country=response.country.iso_code  #CN  两个字符的ISO 3166-1α代码为国
        if country=="":
            return "except"
        return country
    except BaseException, e:
        return "except"

def geoip2_ip_Physical_information(ip):
    try:
        response = reader.city(str(ip))
        continent=response.continent.names['zh-CN'] #亚洲
        country=response.country.names['zh-CN']  #中国 一本字典，该字典的键是区域设置代码和值的名称。
        subdivisions=response.subdivisions.most_specific.names['zh-CN']  #江苏省 一本字典，该字典的键是区域设置代码和值的名称
        city=response.city.names['zh-CN']  #南京
        information=u"%s.%s.%s.%s"%(continent,country,subdivisions,city)
        #print information,len(information)
        if len(information)<3:
            information="except"
        h=qqwry.C_hoset()
        information="%s/%s"%(information,h.www_ip(str(ip)))
        return information
    except BaseException, e:
        try:
            h=qqwry.C_hoset()
            information="%s"%(h.www_ip(str(ip)))
            return information
        except BaseException, e:
            return "except"
        #return "except"
##########################################################################################

#ip纯真数据库
##返回物理位置
#def open_file(data): #格式化
#    ss = data.split("|")
#    #if len(ss)<=3:
#    return ss[0],ss[1]
#    #return 0

def www_wlwz(data): #物理位置
    h=qqwry.C_hoset()
    data=h.www_data(url_www(data))   #'IP/地理位置/网站标题'
    return data   #'IP/地理位置/网站标题'
#
import urllib
def url_www(url): #URL地址中提取网址  http://www.bizschool.cn/plus/90sec.php        www.bizschool.cn
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)
    return host

import socket
def www_ping_ip(WWW):  #域名转IP
    try:
        result = socket.getaddrinfo(WWW, None)
        return result[0][4][0]
    except:
        return 0

def url_www1(url): #URL地址中提取网址  http://www.bizschool.cn/plus/90sec.php        http://www.bizschool.cn
    try:
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        url += "/"      #data ="https://www.baidu.com/cache/sethelp/index.html"
        if url.find("http://") == 0:
            data = url[0:7]
        if url.find("https://") == 0:
            data = url[8:]  # 字符串删除
        return data+host
    except:
        return ""



#City 文件为包含城市信息数据库，
# Country 文件为国家信息数据库。
#http://dev.maxmind.com/zh-hans/geoip/geoip2/geolite2-%E5%BC%80%E6%BA%90%E6%95%B0%E6%8D%AE%E5%BA%93/
#http://geoip2.readthedocs.io/en/latest/
#http://geoip2.readthedocs.io/en/latest/#geoip2.records.country
if __name__ == "__main__":

    #reader = geoip2.database.Reader('GeoLite2-Country.mmdb')  #找不到调用方法
    #response = reader.enterprise('180.124.237.29')

    #########################################
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')  #City 文件为包含城市信息数据库，
    response = reader.city('180.124.237.29')
    print response.country.iso_code  #CN  两个字符的ISO 3166-1α代码为国
    print response.country.name   #China  基于区域的国家名单传递给构造函数。
    print response.country.names['zh-CN']  #中国 一本字典，该字典的键是区域设置代码和值的名称。
    print response.subdivisions.most_specific.name  #Jiangsu 基于区域细分的名单传递给构造函数。
    print response.subdivisions.most_specific.names['zh-CN']  #江苏省 一本字典，该字典的键是区域设置代码和值的名称
    print response.city.name  #Nanjing
    print response.city.names['zh-CN']  #南京
    print response.continent.name #Asia
    print response.continent.names['zh-CN'] #亚洲

    # print response.subdivisions.most_specific.iso_code  #32 这是一个长三个字符的字符串，包含了ISO 3166-2代码细分部分。
    # print response.postal.code  #None
    # print response.location.latitude  #32.0617
    # print response.location.longitude #118.7778
    reader.close()


