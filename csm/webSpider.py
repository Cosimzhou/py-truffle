#coding: UTF-8


import urllib, urllib2, cookielib

filelist = (
 "video.aspx?Cid=58090&type=1&free=1&TagTrue=1&SecTim=2014-06-23"
,"video.aspx?Cid=58091&type=1&free=1&TagTrue=1&SecTim=2014-08-07"
,"video.aspx?Cid=58092&type=1&free=2&TagTrue=1&SecTim=2014-08-07"
,"video.aspx?Cid=60283&type=1&free=0&TagTrue=1&SecTim=2014-08-07"
,"video.aspx?Cid=60284&type=1&free=2&TagTrue=1&SecTim=2014-08-07"
,"video.aspx?Cid=60285&type=1&free=0&TagTrue=1&SecTim=2014-08-07"
,"video.aspx?Cid=60286&type=1&free=2&TagTrue=1&SecTim=2014-08-07"
,"video.aspx?Cid=60287&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60288&type=1&free=2&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60289&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60290&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60291&type=1&free=2&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60292&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60293&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60294&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60295&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60296&type=1&free=0&TagTrue=1&SecTim=2014-08-08"
,"video.aspx?Cid=60297&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60298&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60299&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60300&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60301&type=1&free=2&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60302&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60303&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60304&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60305&type=1&free=0&TagTrue=1&SecTim=2014-08-09"
,"video.aspx?Cid=60306&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60307&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60308&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60309&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60310&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60311&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60312&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60313&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60314&type=1&free=0&TagTrue=1&SecTim=2014-08-10"
,"video.aspx?Cid=60315&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60316&type=1&free=2&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60317&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60318&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60319&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60320&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60321&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60322&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60323&type=1&free=0&TagTrue=1&SecTim=2014-08-11"
,"video.aspx?Cid=60324&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60325&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60326&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60327&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60328&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60329&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60330&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60331&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60332&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60333&type=1&free=0&TagTrue=1&SecTim=2014-08-12"
,"video.aspx?Cid=60334&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60335&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60336&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60337&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60338&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60339&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60340&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60341&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60342&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60343&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60344&type=1&free=0&TagTrue=1&SecTim=2014-08-13"
,"video.aspx?Cid=60374&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60375&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60376&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60377&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60378&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60379&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60380&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60381&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60382&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60383&type=1&free=0&TagTrue=1&SecTim=2014-08-14"
,"video.aspx?Cid=60384&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60385&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60386&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60387&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60388&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60389&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60390&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60391&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60392&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60393&type=1&free=0&TagTrue=1&SecTim=2014-08-15"
,"video.aspx?Cid=60394&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60395&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60396&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60397&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60398&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60399&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60400&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60401&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60402&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60403&type=1&free=0&TagTrue=1&SecTim=2014-08-16"
,"video.aspx?Cid=60404&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60405&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60406&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60407&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60408&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60409&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60410&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60411&type=1&free=0&TagTrue=1&SecTim=2014-08-17"
,"video.aspx?Cid=60495&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60496&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60497&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60498&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60499&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60500&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60501&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60502&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60503&type=1&free=0&TagTrue=1&SecTim=2014-08-18"
,"video.aspx?Cid=60504&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60505&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60506&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60507&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60508&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60509&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60510&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60511&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60512&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60513&type=1&free=0&TagTrue=1&SecTim=2014-08-19"
,"video.aspx?Cid=60514&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60515&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60516&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60517&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60518&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60519&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60520&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60521&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60522&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60523&type=1&free=0&TagTrue=1&SecTim=2014-08-20"
,"video.aspx?Cid=60524&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60525&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60526&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60527&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60528&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60529&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60530&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60531&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60532&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60533&type=1&free=0&TagTrue=1&SecTim=2014-08-21"
,"video.aspx?Cid=60534&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60535&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60536&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60537&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60538&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60539&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60540&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60541&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60542&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60543&type=1&free=0&TagTrue=1&SecTim=2014-08-22"
,"video.aspx?Cid=60544&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60545&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60546&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60547&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60548&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60549&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60550&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60551&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60552&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60553&type=1&free=0&TagTrue=1&SecTim=2014-08-23"
,"video.aspx?Cid=60554&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60555&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60556&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60557&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60558&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60559&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60560&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60561&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60562&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60563&type=1&free=0&TagTrue=1&SecTim=2014-08-24"
,"video.aspx?Cid=60564&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60565&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60566&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60567&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60568&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60569&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60570&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60571&type=1&free=0&TagTrue=1&SecTim=2014-08-25"
,"video.aspx?Cid=60572&type=1&free=0&TagTrue=1&SecTim=2014-08-26"
,"video.aspx?Cid=60573&type=1&free=0&TagTrue=1&SecTim=2014-08-26"
,"video.aspx?Cid=60574&type=1&free=0&TagTrue=1&SecTim=2014-08-26"
,"video.aspx?Cid=60575&type=1&free=0&TagTrue=1&SecTim=2014-08-26"
,"video.aspx?Cid=60576&type=1&free=0&TagTrue=1&SecTim=2014-08-26"
,"video.aspx?Cid=60577&type=1&free=0&TagTrue=1&SecTim=2014-08-26"
            )

print "downloading with urllib2"
url = 'http://user.wangxiao.cn/usercenter/'


def loginInWebSite():
    cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    urllib2.urlopen('http://user.wangxiao.cn').read()
    
    postdata=urllib.urlencode({
        'txtUsername':'zz_wzh',
        'txtPassword':'180932ava',
        'x':'33',
        'y':'14'
    })
    
    req = urllib2.Request(
        url = 'http://users.wangxiao.cn/LoginBarJSON.aspx',
        data = postdata
    )
    result = urllib2.urlopen(req).read()
    print result

loginInWebSite()

for i in range(len(filelist)):
    data = urllib2.urlopen(url+filelist[i]).read() 

    urlset = set()  
    for l in str(data).split("\n"):
        if ".mp4" in l:
            start = l.index('"http://')+1
            end = l.index('.mp4"')
            fileurl = l[start:end+4]
            urlset.add(fileurl)
    
    if len(urlset)>0:
        print "%d : %s"%(i,urlset.pop())
    else:
        print i
