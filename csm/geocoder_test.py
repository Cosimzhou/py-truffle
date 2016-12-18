#!/usr/bin/python
#coding:utf-8
'''
Created on 2014年6月16日

@author: zhouzhichao
'''
import datetime
import argparse
import urllib2
import math
import csv

ip='192.168.11.181'
port=8081
key='dGlnZXJtYXAK'
#e.g. http://192.168.11.181:8081/?city=北京市&key=dGlnZXJtYXAK&name=老虎宝典&addr=中关村北大街116号
urlPattern = "http://%s:%s/?city=%%(city)s&key=%s&name=%%(name)s&addr=%%(addr)s" 
radiusEarth=6371004 # meters
cons = math.pi/180 # use to transfer unit system from degree to radian

def distanceCalc(x1,y1,x2,y2):
    """
    地球曲面距离
    """
    rlon1, rlat1, rlon2, rlat2 = float(x1) * cons, float(y1) * cons, float(x2) * cons, float(y2) *cons
    vcos = math.cos(rlat1) * math.cos(rlat2) * math.cos(rlon1 - rlon2) + math.sin(rlat1) * math.sin(rlat2)
    vcos = 1.0 if vcos > 1.0 else (vcos if vcos > -1.0 else -1.0)
    return math.acos(vcos) * radiusEarth

def axisLonlat(x1,y1,x2,y2):
    """
    地球曲面距离
    """
    rlon1, rlat1, rlon2, rlat2 = float(x1) * cons, float(y1) * cons, float(x2) * cons, float(y2) *cons
    vcos = math.cos(rlat1) * math.cos(rlat2) * math.cos(rlon1 - rlon2) + math.sin(rlat1) * math.sin(rlat2)
    vcos = 1.0 if vcos > 1.0 else (vcos if vcos > -1.0 else -1.0)
    vsin = math.sqrt(1-vcos**2)
    sx1, sy1, sz1 = math.cos(rlat1)*math.cos(rlon1), math.cos(rlat1)*math.sin(rlon1), math.sin(rlat1)
    sx2, sy2, sz2 = math.cos(rlat2)*math.cos(rlon2), math.cos(rlat2)*math.sin(rlon2), math.sin(rlat2)
    rolat = math.asin((sx1*sy2-sx2*sy1) / vsin)
    rolon = 0
    
    return (rolat,rolon)

def check(arg1, arg2, stat):
    stat['total'] += 1
    if arg2.get('level') is None:
        return
    
    lblLevel = 'level%s' % arg2['level'] 
    if stat.get(lblLevel):
        nlevel = stat[lblLevel]
    else:
        nlevel = {'total':0, 'good':0}
    
    nlevel['total'] += 1
    dist = distanceCalc(arg1['lon'], arg1['lat'], arg2['lon'], arg2['lat'])
    
    if dist <= float(arg1['limit']):
        stat['good'] += 1
        nlevel['good'] += 1
    
    stat[lblLevel] = nlevel

def sendRequest(args):
    typelist = ['city', 'name', 'addr']
    local_args = {}
    for i in typelist:
        local_args[i] = urllib2.quote(args.get(i))
    url = urlPattern % local_args
    
    retMap = {'code': 200}
    try:
        strjson = urllib2.urlopen(url).read()
        retMap.update(eval(strjson))
    except urllib2.HTTPError as e:
        retMap['code'] = e.code
    except urllib2.URLError as e:
        retMap['code'] = e.reason
        retMap['info'] = str(e)
    
    return retMap

def worker(cityname, filepath):
    mapToIndex=None
    inputFile=open(filepath,'r')
    csvReader=csv.reader(inputFile, quoting=csv.QUOTE_MINIMAL)
    
    
    statistics = {'total':0, 'good':0}
    # {total:xx, good:xx, leveln:{total:xx, good:xx}}
    
    timeStart = datetime.datetime.now()
    for i in csvReader:
        if mapToIndex is None:
            mapToIndex = {}
            for ii in range(len(i)):
                mapToIndex[i[ii]] = ii
            if mapToIndex.get('lon') is None:
                mapToIndex = {'id':0,   'name':1,
                              'addr':2, 'lon':3,
                              'lat':4,  'limit':5}
        else:
            argument = {'name': i[mapToIndex['name']], 
                        'addr': i[mapToIndex['addr']],
                        'lat':  i[mapToIndex['lat']],
                        'lon':  i[mapToIndex['lon']],
                        'limit':i[mapToIndex['limit']],
                        'city': cityname}
#             print argument
            geoResult = sendRequest(argument)
#             print geoResult
            
            check(argument, geoResult, statistics)
        
    inputFile.close()
    timeEnd = datetime.datetime.now()
    timeDue = timeEnd-timeStart
    
    print cityname, str(timeDue.days*24.0*60.*60.0 + timeDue.seconds + timeDue.microseconds/1000000.0) + "sec."
    print statistics
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Geocoder test.')
    parser.add_argument('--server', '-s', default=None, help='geocoder服务的IP')
    parser.add_argument('--port', '-p', default=None, help='geocoder服务的端口')
    parser.add_argument('--key', '-k', default=None, help='geocoder服务的使用的key')
    parser.add_argument('--city', '-c', default=None, help='进行定位的城市')
    parser.add_argument('--list', '-l', default=None, help='进行定位的城市的对比结果文件')
    args = parser.parse_args()
    
    if args.server:
        ip = args.server
    if args.port:
        port = args.port
    if args.key:
        key = args.key
    
    urlPattern = urlPattern%(ip,port,key)
    
    if args.list is not None and args.city is not None:
        worker(args.city, args.list)
    else:
        print '不可缺少输入城市和对比文件'

        
    
#     worker('北京市', '/home/zhouzhichao/下载/beijing_test.csv')
#     worker('杭州市', '/home/zhouzhichao/下载/hangzhou_test.csv')
#     worker('上海市', '/home/zhouzhichao/下载/shanghai_test.csv')
#     worker('乌鲁木齐市', '/home/zhouzhichao/下载/wlmq_test.csv')
#     worker('郑州市', '/home/zhouzhichao/下载/zhengzhou_test.csv')

    pass