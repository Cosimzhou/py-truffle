#coding:UTF-8

'''
Created on 2016年4月16日

@author: zhouzhichao
'''

import re, sys
form_list, formulas = [], {}

isdef = lambda x: sys._getframe(1).f_locals.get(x) is not None
def tl(txt):
    cmd, i = '', 0
    while i < len(txt):
        if ord(txt[i]) > 127:
            for k in 0,1,2: 
                cmd += '_%02X' % ord(txt[i+k])
            i += 3        
        else:
            cmd += txt[i]
            i += 1
    return cmd.replace('%','/100.0')

def al(txt):
    if '?' not in txt: return txt
    
    aa = txt.split('?')
    ar = []
    for a in aa:
        ar += a.split(':')
    for i in xrange(len(ar)):
        ar[i] = ar[i].strip(' \t')
    print ar
    
# def tohz(txts):
#     if txts[0] == '_':
#         var = ''
#         for i in xrange(0, len(txts), 3):
#             var += chr(int(txts[i+1:i+3], 16))
#         return var
#     else:
#         return None

exec tl('''万,登记费,核档费=10000.0, 80, 80
家装预算 = 0
错误='错误' ''')

# 利率 = 0.049 #4.75    4.90    2.75    3.25

def execAndShowCalc(cmd):
    def appendVar(cont, var):
        if var:
            if var == '万':
                cont = cont.rstrip(' x*\t') + '万'
            else:
                cont += '%s(%%(%s).2f)'%(var,tl(var))
        return cont 
    
    content, var = '', ''
    for c in cmd:
        if ord(c) < 128:
            content = appendVar(content,var)
            var = ''
            if c == '%': c='%%'
            elif c == '*': c='x'
            content += c
        else:
            var += c
    content = appendVar(content,var)

    dc = sys._getframe(1).f_locals
    dc.update(sys._getframe(1).f_globals)
    print content % dc
    
def solve(param):
    fpool, delidcs = formulas, True
    fpool.update(param)
    while delidcs:
        delidcs = []
#         for k in form_list:
#             v = fpool.get(k)
#             if v is None: continue
        for k,v in fpool.items():
            try:
                if isdef(k):
                    delidcs.append(k)
                    continue
                cmd = "%s = %s"%(k,v)
                exec tl(cmd)
                execAndShowCalc(cmd)
                delidcs.append(k)
            except NameError as e:
                m = re.match(r"name \'(\w+)\' is not defined", e.message)

        for k in delidcs:
            del fpool[k]

    print '初次支出: %.2f'%eval(tl('初次支出'))
    
def init():
    global formulas, form_list
    with open('fang.for', 'r') as f:
        for i in f.readlines():
            i = i.strip('\n\r \t')
            if i is None or len(i) < 1 or i[0] == '#': continue
            a = i.strip('\n\r \t').split('=')
            if len(a)>=2:
                form_list.append(a[0].strip(' \t'))
                formulas[form_list[-1]] = '='.join(a[1:])

if __name__ == '__main__':
    al('(1?2:3)?(4?5:6):(7?(8?9:0):A)')
    print '(5 if 4 else 6) if (2 if 1 else 3) else ((9 if 8 else 0) if 7 else A)'
#     exit(0)
    init()
    solve({'总价':'230*万',
           '面积':'54',
           '贷款年限':'20',
           '首付':'120*万',
           })
