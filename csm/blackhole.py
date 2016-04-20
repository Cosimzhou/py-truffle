# -*- coding: utf-8 -*-

'''
Created on 2014年6月24日

@author: zhouzhichao
'''


import argparse

def proc6174(*wargs):
    num = ''.join(map(str, wargs))
    if len(wargs) != 4 or type(eval(num)) is not int:
        return
    cnt, goon = 0, True
    while goon:
        maxval = int(''.join(sorted(num, reverse=True)))
        minval = int(''.join(sorted(num)))
        
        diff = maxval - minval
        if diff == 6174:
            goon = False
        num = ("0000%s"%diff)[-4:]    
        cnt += 1 
        print "No. %s:%s-%s=%s"%(cnt, maxval, minval, diff)

        
    
def proc123(num):
    if type(eval(num)) is not int:
        return
    
    cnt, goon = 0, True
    while goon:
        e, o, lng = 0, 0, len(num)
        for i in num:
            if i in '02468':
                e += 1
        o = lng - e
        
        cnt += 1
        print "No. %s:%s -> %s%s%s"%(cnt, num, e, o, lng)
        num = '%s%s%s'%(e, o, lng)
        if num == '123':
            goon = False
            
    
def test():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--configfile', help=u'配置文件')
    config = parser.parse_args()
    print config.configfile
    print config.__dict__


if __name__ == '__main__':
    proc6174(2,3,6,1)
    proc123('122545684326874')
    pass