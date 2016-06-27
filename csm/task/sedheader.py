#! /usr/bin/python 
# -*- coding: UTF-8 -*-

import os, time, re
Env = os.environ
COMMENT = """/*@({
    这里是用于测试自动去源文件内部内容的说明
 
    //@rm@           用于剔除单行的隐藏代码，可用于行后注释
    //@if@           条件开关，用于接描述条件，以‘#’分隔语句后的注释
    //@elif@         else if，必须跟随在if之后的条件开关，elif的条件与if的条件要求相同
    //@else@         不满足之前的条件时展开，必须在if语句之后
    //@endif@        if条件开关的结束，endif必须与if匹配
    //@rm@           删除本行内容
    @......@         标签替换，替换必须与注释保留空格分隔
 *      @private@    删除本行内容
    / *@({...})@* /  用于剔除多行的隐藏信息
 
 })@*/
"""

strtime=time.localtime(time.time())
DEFAULT_DICT={'private':0,
    'YEAR': time.strftime('%Y',strtime),
    'DATE':time.strftime('%Y-%m-%d',strtime),
    'TIME':time.strftime('%Y-%m-%d %H:%M:%S',strtime)
}

class IfState: (Unmarked, Marked, Closed) = range(3)
class HeaderFileTrimmer(object):
    def __init__(self):
        self.initSed()
        self.sedInitFlag()
    
    # initialize 'sed' process environment
    def initSed(self):
        preDealDict = Env.get('PREDEAL_DICT')
        if preDealDict is not None:
            preDealDict = eval(preDealDict)
            if type(preDealDict) is dict:
                DEFAULT_DICT.update(preDealDict)
        
        self.keywordPattern = re.compile('/@([a-z]+)@')
        self.privateDict = DEFAULT_DICT
        DICT_KEYS = ['%s@'%i for i in self.privateDict]
        self.sedKeywords = {
            '/': ('*@({', '/@if@', '/@elif@', '/@else@', '/@endif@', '/@rm@'), # '/': ('**api<',),
            '@': DICT_KEYS,
            '}': (')@*/',)
        }
        
    def sedInitFlag(self):
        self.sedCommented = False
        self.sedCondition = False
        self.IfStack = []
    #
    def findExceptKeyword(self, c):
        return None if c == '>' and not self.sedCommented else self.sedKeywords.get(c)
    
    def sed(self, line):
        parsed, seks, sc, i = '', None, 0, 0
        for c in line:
            i += 1
            if seks is None:  # keyword is not found now
                seks, sc = self.findExceptKeyword(c), 0
            else:   # remove unmatched item from seks list
                seks = filter(lambda e:len(e)>sc and c==e[sc], seks)
                if seks:  # there is still some items in seks list
                    sc += 1
                    if len(seks) == 1 and len(seks[0]) == sc:
                        word = seks[0]
                        if not self.sedCommented:
                            parsed = parsed[0:-len(word)]
                            if word == '*@({':
                                self.sedCommented = True
                            elif word[-1] == '@':
                                if word[0] == '/':
                                    retw = self.ifelif(word, line[i:])
                                    if type(retw) is str: return retw
                                else:
                                    sedw = self.privateDict.get(word[:-1])
                                    if type(sedw) is str: parsed += sedw
                                    elif sedw == 0: return ''
                        elif word == ')@*/':
                            self.sedCommented = False
                        seks = None
                        continue
                else: 
                    seks = self.findExceptKeyword(c)
            if not self.sedCommented: parsed += c
        if not self.IfStack or self.IfStack[-1] == IfState.Marked:
            return parsed
        else: return ''
    
    def ifelif(self, word, line):
        m = self.keywordPattern.match(word)
        if m and m.groups():
            word = m.groups()[0]
        else: return ''
        if word == 'if':
            ret = eval(line)
            self.IfStack.append(IfState.Marked if ret else IfState.Unmarked)
        elif word == 'elif':
            if self.IfStack:
                if self.IfStack[-1] == IfState.Marked:
                    self.IfStack[-1] = IfState.Closed
                elif self.IfStack[-1] == IfState.Unmarked:
                    ret = eval(line)
                    self.IfStack[-1] = IfState.Marked if ret else IfState.Unmarked
            else: exit(1)
        elif word == 'else':
            if self.IfStack:
                self.IfStack[-1] = IfState.Marked if self.IfStack[-1] == IfState.Unmarked else IfState.Closed
            else: exit(1)
        elif word == 'endif':
            if self.IfStack:
                self.IfStack.pop()
            else: exit(1)
        elif word == 'rm':
            pass
        else:
            return None
        return ''

    def sedAFile(self, filename, ofilename = None):
        self.sedInitFlag()
        ofn = ofilename if ofilename else filename+'-mid'
        f, of = open(filename, 'r'), open(ofn, 'w')
        for line in f.readlines():
            of.write(self.sed(line))
        f.close(); of.close()
        if ofilename is None:
            os.renames(ofn, filename)
        
if __name__ == '__main__':
    Env['PREDEAL_DICT']="""{'AUTHOR':'Cosim','COMPANY':'Sestall Studio','DELEGATE':'sbcehui'}"""
    
    hft = HeaderFileTrimmer()
    hft.sedAFile('/Users/zhouzhichao/tmp/exam.h', '/Users/zhouzhichao/tmp/rest.h')
    pass