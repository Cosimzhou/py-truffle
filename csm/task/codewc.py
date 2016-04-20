#coding: UTF-8
"""
用于统计指定目录下的源文件行数
"""
import os, sys
import argparse
sourceTypeSet = set(('c', 'h', 'm', 'mm', 'py', 'sh'))

'''┣┗┃'''
def fileLineNum(file_name):
    if file_name and file_name.split('.')[-1] in sourceTypeSet:
        with open(file_name, 'r') as f:
            cnt, length = 0, 0
            for l in f.readlines():
                l = l.strip(' \t\n')
                if l: 
                    cnt += 1
                    length += len(l)
            return cnt,length
    return None
"""        
def countWorkspace(workspace_path):
    with open('/tmp/codewc', 'w') as tf:
        for root, _, filelist in os.walk(workspace_path):
            rootNoSource = True
            for f in filelist:
                file_path = '/'.join((root,f))
                cnt = fileLineNum(file_path)
                if cnt is not None:
                    if rootNoSource:
                        rootNoSource = False
                        tf.write(root+'\n')
                    tf.write('%s\t%d\t%d\n'%(file_path, cnt[0], cnt[1]))

#     ar = ('┣','┗','┃')
#     dirCnt = []
#     content = []
#     with open('/tmp/codewc', 'r') as tf:
#         with open('/tmp/codewc', 'w') as 
#         parentDir = ''
#         for l in tf.readlines():
#             arr = l.strip(' \t\n').split('\t')
#             if len(arr) == 1:
#                 if parentDir:
#                     if not arr[0].startswith(parentDir):
#                         k = '/'.join(map(lambda x:x[3],dirCnt))+'/'
#                         while not arr[0].startswith(k):
#                             dirCnt.pop()
#                             k = '/'.join(map(lambda x:x[3],dirCnt))+'/'
#                     
#                     dirs = arr[0][len(parentDir):].split('/')
#                     for d in dirs:
#                         dirCnt.append([0, 0, d])
#                 else:
#                     dirCnt.append([0,0,arr[0]+'/'])
#         
#                 parentDir = arr[0]+'/'
#                 content.append(arr[0])
#             elif len(arr) == 3:
#                 dirCnt[-1][0]+=int(arr[1])
#                 dirCnt[-1][1]+=int(arr[2])
#             else:
#                 sys.stderr.write('error:%s'+l.strip('\n'))
    return 0#wcsum
"""
def countWorkspace(workspace_path):
    buffers,stkDir = [], []
    slwp = len(workspace_path)
    for root, _, filelist in os.walk(workspace_path):
        root = '.'+root[slwp:]
        while stkDir and not root.startswith(buffers[stkDir[-1]][0]):
            if len(stkDir) >= 2: 
                buffers[stkDir[-2]][1]+=buffers[stkDir[-1]][1]
                buffers[stkDir[-2]][2]+=buffers[stkDir[-1]][2]
            stkDir.pop()

        rootNoSource = True
        for f in filelist:
            file_path = '/'.join((workspace_path,root,f))
            cnt = fileLineNum(file_path)
            if cnt is not None:
                if rootNoSource:
                    rootNoSource = False
                    stkDir.append(len(buffers))
                    buffers.append([root+'/',0,0])
                buffers.append([file_path, cnt[0], cnt[1]])
                buffers[stkDir[-1]][1]+=cnt[0]
                buffers[stkDir[-1]][2]+=cnt[1]
          
    while len(stkDir) >= 2: 
        buffers[stkDir[-2]][1]+=buffers[stkDir[-1]][1]
        buffers[stkDir[-2]][2]+=buffers[stkDir[-1]][2]
        stkDir.pop()      
    
    for i in xrange(0, len(buffers)-1):
        arr = buffers[i][0].split('/')
        char = '┗  'if buffers[i+1][0][-1]=='/' and len(buffers[i+1][0].split('/'))==len(buffers[i][0])+1 else'┣  '
        if arr[-1]:
            buffers[i][0] = '┃ '*(len(arr)-2) +char+ arr[-1]
        else:
            buffers[i][0] = '┃ '*(len(arr)-2) +char+ arr[-2]+'/' 
    arr = buffers[-1][0].split('/')
    char = '┗  '
    if arr[-1]:
        buffers[-1][0] = '┃ '*(len(arr)-2) +char+ arr[-1]
    else:
        buffers[-1][0] = '┃ '*(len(arr)-2) +char+ arr[-2]+'/' 
    
    
#     for i in xrange(0,len(buffers)-1):
#         for d in xrange(0,len(buffers[i][0]), 3):
#             if buffers[i][0][d:d+3] != '┃':
#                 buffers[i][0] = buffers[i][0][:d] +('┗''┣')+buffers
#     ar = ('┣','┗','┃')
#     parent, prow = buffers[0][0]+'/', [0]
#     for i in xrange(1, len(buffers)-1):
#         if buffers[i][0].startswith(parent):
#             buffers[i][0] = ('┣'if buffers[i+1][0].startswith(parent)else'┗')+buffers[i][0][len(parent):]
#             buffers[prow[-1]][1] += buffers[i][1]
#             buffers[prow[-1]][2] += buffers[i][2]
#         else:
#             arrparent = parent.split('/')[:-2]
#             while not buffers[i][0].startswith('/'.join(arrparent)+'/'):
#                 arrpent = arrparent[:-1]
#                 prow.pop()
            
    for l in buffers:
        print l[0],l[1],l[2]
    
    return buffers[0][1]#wcsum
#"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''统计代码行数''')
    parser.add_argument('directory', metavar='N', type=str, nargs='+', help='诗句的内容，每句以空格分隔')
#     parser.add_argument('--sourceCode', '-s', default='GBK', help='输入文件的编码方式，默认为“GBK”')
    args = parser.parse_args()
    
    for direct in args.directory:
        print "%s:%d"%(direct, countWorkspace(direct.rstrip('/')))