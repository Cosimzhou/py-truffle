#coding: UTF-8

import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Coder transfer
    支持文本文件以GBK、UTF-8、base64、Big5、Shift_JIS及Unicode编码方式之间的互转
    """)
    parser.add_argument('--dest', '-d', default='UTF-8', help='输出文件的编码方式，默认为“UTF-8”')
    parser.add_argument('--source', '-s', default='gbk', help='输入文件的编码方式，默认为“gbk”')
    parser.add_argument('--output', '-o', default=None, help='输出文件路径')
    parser.add_argument('--file', '-f', default=None, help='输入的待转码文件')
    args = parser.parse_args()
    
    strout, strin, strerr = sys.stdout, sys.stdin, sys.stderr
    if args.file:
        strin = open(args.file, 'r')
        if args.output is None:
            args.output = args.file + '.txt'
            
    if args.output:            
        strout = open(args.output, 'w')
        
    if args.source.lower()=='unicode':
        for l in strin.readlines():
            try:
                ll = l.encode(args.destCode)
            except UnicodeDecodeError as e:
                strerr.write('this line occurred convert error!\n')
                continue
            strout.write(ll)
    else:
        for l in strin.readlines():
            try:
                ll = l.decode(args.source).encode(args.dest)
            except UnicodeDecodeError as e:
                strerr.write('this line occurred convert error!\n')
                continue
            strout.write(ll)
        
    strin.close()
