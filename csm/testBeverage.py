# -*- coding: utf-8 -*-

'''
Created on 2014年7月17日

@author: zhouzhichao
'''
"""
    Nazonzao #1  Begin
"" "

def f(n, m):
    if n>0 and m>1:
        return sum([f(i, m-1) for i in xrange(n+1)])
    else:
        return 0 if n<0 or m<0 else 1 

# f(n, m) <==> (n+m-1)! / [(m-1)! n!]

def ni(n):
    rst = 1
    for i in xrange(1,n+1):
        rst *= i
    return rst

def smp(n, m):
    if n<=0 or m<=0:
        return 1
    rst = 1
    for i in xrange(1,m):
        rst *= n+i
    for i in xrange(1,m):
        rst /= i
    return rst

if __name__ == '__main__':
    n, m = 15, 9
    print "result: %s" % f(n, m)
    
    
    print smp(n,m)
"" "
    Nazonzao #1  End
"""
    
"""
    Nazonzao #2  Begin
"""

def f(n, m):
    if n>0 and m>1:
        return sum([f(i, m-1) for i in xrange(n+1)])
    else:
        return 0 if n<0 or m<0 else 1 

def ni(n):
    rst = 1
    for i in xrange(1,n+1):
        rst *= i
    return rst

def smp(n, m):
    if n<=0 or m<=0:
        return 1
    rst = 1
    for i in xrange(1,m):
        rst *= n+i
    for i in xrange(1,m):
        rst /= i
    return rst

if __name__ == '__main__':
    n, m = 15, 9
    print "result: %s" % f(n, m)
    
    
    print smp(n,m)
"""
    Nazonzao #2  End
"""
