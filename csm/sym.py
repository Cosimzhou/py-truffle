with open('/Users/zhouzhichao/sym2img', 'r') as f:
    for l in f.readlines():
        ll = l.split(' => ')
        print "print %s #%s"%(ll[0],l)
#         print ll[0].replace('"',''), l