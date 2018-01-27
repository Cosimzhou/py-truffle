#! /usr/bin/python
# -*- coding: UTF-8 -*-
"""
用于统计指定目录下的源文件行数
"""
import os, sys
import argparse
sourceTypeSet = set(('c', 'cpp', 'cc', 'hpp', 'h', 'm', 'mm', 'py', 'sh', 'java'))
args = None

def fileLineNum(file_name):
	if file_name and file_name.split('.')[-1] in sourceTypeSet:
		with open(file_name, 'r') as f:
			cnt, length = 0, 0
			for l in f.readlines():
				l = l.strip(' \t\r\n')
				if l: 
					cnt += 1
					length += len(l)
			return [cnt,length]
	return None

def countWorkspace(workspace_path):
	def getCDInfo(buf, root):
		md, v = buf, None
		for d in root.split('/'):
			if d in md:
				v = md[d]
			else:
				v = md[d] = [0, 0, {}]
			md = v[2]
		return v
	def updateCDInfos(cdinfos):
		if len(cdinfos) == 3:
			l,b = 0,0
			useless=[]
			for k,v in cdinfos[2].items():
				v[0:2] = updateCDInfos(v)
				if v[0] == 0:
					useless.append(k)
				else:
					l +=v[0]
					b +=v[1]
			for k in useless:
				del cdinfos[2][k]
			return l,b
		else:
			return cdinfos
	
	def outputResult(buff, depth=0, before=None):
		if before is None: before = [False]*100
		if len(before) <= depth: before.append(False)
		dirs, n = sorted(buff.keys()), 0
		for d in dirs:
			cdinfo = buff[d]
			n += 1
			if n <len(dirs):
				before[depth], anchor =True, '├'
			else:
				before[depth], anchor =False, '└'
				
			prefix = ''
			for i in xrange(depth-1):
				prefix += '│' if before[i+1] else ' '
			if depth: 
				prefix+=anchor
				prefix+='┬'if len(cdinfo) == 3 else'─'
			sys.stdout.write('%s%s:  %d, %d\n'%(prefix, d, cdinfo[0], cdinfo[1]))
			if len(cdinfo) == 3:
				outputResult(cdinfo[2], depth+1, before)
	
	suml, mbuffer = 0, {}
	slwp = len(workspace_path)
	if not args.quiet: 
		for root, _, filelist in os.walk(workspace_path):
			root = '.'+root[slwp:]
			cdinfo = getCDInfo(mbuffer, root)
			for f in filelist:
				cnt = fileLineNum('/'.join((workspace_path,root,f)))
				if cnt is not None:
					cdinfo[2][f] = cnt 
		mbuffer['.'][0:2] = updateCDInfos(mbuffer['.'])
		outputResult(mbuffer)
		suml = mbuffer['.'][0]
	else:
		for root, _, filelist in os.walk(workspace_path):
			root = '.'+root[slwp:]
			for f in filelist:
				cnt = fileLineNum('/'.join((workspace_path,root,f)))
				if cnt is not None: suml += cnt[0] 
	return suml

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='''统计代码行数''')
	parser.add_argument('directory', metavar='N', type=str, nargs='+', help='需要统计的目录')
	parser.add_argument('--quiet', '-q', action='store_true', help='不输出各文件细节')
	args = parser.parse_args()
	
#	 cy,cx=map(int,os.popen('stty size').readlines()[0].strip('\n').split(' '))
	
	for direct in args.directory:
		sys.stdout.write("%s:%d\n"%(direct, countWorkspace(direct.rstrip('/'))))
		if not args.quiet:sys.stdout.write('-------------------------------\n')
