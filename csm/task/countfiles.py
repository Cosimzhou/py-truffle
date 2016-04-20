#coding: UTF-8

"""
    用于遍历文件夹，计算文件中各目录文件占用大小
"""
import os  
from os.path import join, getsize  
from datetime import datetime
  
def getdirsize(dirpath):  
    size = 0L
    read = False  
    for root, dirs, files in os.walk(dirpath):
        if root == dirpath:
            try:  
                size = sum([getsize(join(root, name)) for name in files])
            except OSError as _:
                continue
            read = True  
            break
        elif read:
            break
        else:
            continue
        
    xx = [getdirsize(join(root, name)) for name in dirs] if dirs else [0]   
    size += sum(xx)
    if size == 0:
        return 0
    print "%10d: %s"%(size, root)
    n = 0 
    for i in dirs:
        print ">>%3.3f%%: %s/%s"%(100.0*xx[n]/size, root, i)
        n+=1
    return size



def s():
    tm = datetime.strptime('2014-10-1', "%Y-%m-%d")
    st = os.stat('/Users/zhouzhichao/eisd.plist').st_mtime
    print st, #tm.date.seconds

def readfile(rootpath, recordfile):
    level = rootpath.split('/')
    with open(recordfile, "r") as f:
        for l in f.readlines():
            d = l.split(':')
            if rootpath in d[1]:
                loc = d[1].split('/')
                if loc == level+1:
                    pass
    pass

# stk, sti, stj, sct = [None] * 100, 0, 0, [0]*100
# with open('/home/zhouzhichao/dusm') as f:
#     for l in f.readlines():
#         larr = l.split(':')
#         if len(larr) != 1: 
#             continue
#         
#         parr = larr[1].split('/')
#         if stk[sti] == '/'.join(parr[:-1]):
#             sct[sti]+=int(larr[0])
#         elif larr[1][:len(stk[sti])] == stk[sti]:
#             sti += 1
#             stk[sti] = larr[1]
#             sct[sti] = int(larr[0])
#         else:
#             


if __name__ == '__main__':  
    s()
#     print int("  35 ")
#     filesize = getdirsize(r'/Users/zhouzhichao/workspace')
#     filesize = getdirsize('/data', 0)    
#     print 'There are %.3f' % (size/1024/1024), 'Mbytes in c:\\windows'  
"""   
def fileLineNum(file_name):
    if file_name:
        ext = file_name.split('.')[-1]
        if ext in sourceTypeSet:
            f = open(file_name, 'r')
            cnt = 0
            for l in f.readlines():
                if l:
                    cnt += 1
            return cnt
    return -1
        
def countWorkspace(workspace_path):
    sum, rootsum = 0, 0
    for root, dirlist, filelist in os.walk(workspace_path):
        rootsum = 0
        rootNoSource = True
        for f in filelist:
            file_path = '/'.join((root,f))
            cnt = fileLineNum(file_path)
            if cnt >= 0:
                if rootNoSource:
                    rootNoSource = False
                    print root
                print file_path, cnt
                rootsum += cnt
        if not rootNoSource:
            sum += rootsum
            print root, '=>', rootsum
    print 'total lines:', sum
    return sum

if __name__ == '__main__':
    countWorkspace('/Users/zhouzhichao/workspace/tigerknows-iphone')
"""