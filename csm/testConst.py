# -*- coding: utf-8 -*-

'''
Created on 2014年7月11日

@author: zhouzhichao
'''

import argparse, shutil

class ConstError(Exception): pass

class _const(object):
    def __setattr__(self, k, v): 
        if k in self.__dict__:
            raise ConstError
        else:
            self.__dict__[k] = v 

class a:
    def __init__(self):
        self.const = _const()
        self.const.kk = {}
    def getK(self):
        return self.const.kk
 
A=a()
print A.getK()

k=A.getK()

print k

k['ads'] = 30

print k
print A.getK()

# const = _const()


# [test_const.py]
# from const import const


# const.a = 3 
# const.b = "aa"
# const.a = 5 # will raise ConstError


def main(*wargs,**kwargs):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, epilog='__credit__')
    parser.add_argument('-c', '--keyfile', default='/opt/swift/config/rt_conf.conf', help=u'配置文件')
    parser.add_argument('-t', '--bites', default='agms', help=u'要处理的城市(已失效，在配置文件中设置)')
    parser.add_argument('files', nargs='*', help=u'要处理的城市(已失效，在配置文件中设置)')
    config = parser.parse_args()
    config.__dict__.update(kwargs)
    if wargs: config.files = wargs
    
    print wargs, kwargs
    
    print config
    
if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, epilog='__credit__')
#     parser.add_argument('-c', '--configfile', default='/opt/swift/config/rt_conf.conf', help=u'配置文件')
#     parser.add_argument('-t', '--types', default='agms', help=u'要处理的城市(已失效，在配置文件中设置)')
#     parser.add_argument('cities', nargs='*', help=u'要处理的城市(已失效，在配置文件中设置)')
#     config = parser.parse_args()
#     
#     print config
#     
#     main()
#     pass

    