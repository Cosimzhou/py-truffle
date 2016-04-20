

import StringIO, sys
from csm.ptry.config import Hallo, init
from csm.ptry import xx2#test 
init('Guten Morgen')

def kk():
    print Hallo['Hallo']
    

def k(a1='xxx', **kwargs):
    print a1
    print kwargs


if __name__ == '__main__':

    mod = xx2
    
    try:
        aa = 0
    except Exception as e:
        print str(e)
    
    for i in (mod,mod,mod):
        i.test()
        print i.__name__


    while True:
        try:
            pass
        except KeyboardInterrupt as e:
            break


#     kk()
#     test()   
    
#     buf = StringIO.StringIO()
#     tmp, sys.stdout = sys.stdout, buf
#     print 'test'
#     kk = buf.tell()
#     print 'auiuih\nrfu   ew\n289e\tw2\n4w'
#     sys.stdout = tmp
#     buf.seek(kk)
#     print "test:->(%s)"%buf.read()
# 
#     tmp, sys.stdout = sys.stdout, buf
#     print '[test]'
#     kk = buf.tell()
#     print '<>a4gf56uiuikkh\nrfu   ew\n289e\tw2\n4w'
#     sys.stdout = tmp
#     buf.seek(kk)
#     print "test:->(%s)"%buf.read()
#     sys.stdout = tmp
#     buf.seek(kk)    
#     buf.close() 

    for i in xrange(26):
        fmt = "%08"+chr(i+65)
        try:
            print fmt%38, fmt
        except:
            continue 

    
    
    print
