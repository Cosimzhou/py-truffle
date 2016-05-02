#coding:UTF-8

'''
Created on 2016年4月16日

@author: zhouzhichao
'''

import re, sys

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
    return cmd

def tohz(txts):
    if txts[0] == '_':
        var = ''
        for i in xrange(0, len(txts), 3):
            var += chr(int(txts[i+1:i+3], 16))
        return var
    else:
        return None
    

exec tl('''万,登记费,核档费=10000.0, 80, 80
家装预算 = 0''')


# 利率 = 0.049 #4.75    4.90    2.75    3.25
# 
# #等额本息
# 每期还款额=借款本金*月利率*(1+1.0/((1+月利率)**还款月数-1))
# print 'benxi: ', 每期还款额
# print 每期还款额*还款期数+首付
# print
# 
# 已还本金 = 0
# #等额本金
# 
# 借款本金=float(借款本金)
# 已还本金,已还金额=0,0
# for i in xrange(还款期数):
#     已还本金 = i*借款本金/还款期数
#     每期还款额=借款本金/还款期数 + 月利率*(借款本金-已还本金)
# #     print '%d: '%i, 每期还款额
#     已还金额 += 每期还款额
# print 已还金额+首付



formulas={
'总价': '单价*面积',
'成交价格': '总价',
'中介费': '0.027*成交价格',
'印花税': '成交价格/2000.0',
'单价': '总价/面积',
'首付限': '0.3*总价',
'首付': '首付限',
'交易费': '3*面积',
'贷款总额': '总价-首付',
'契税': '总价*(0.01 if 面积<90 else 0.015)',
'初次支出': '首付+契税+印花税+登记费+核档费+交易费+家装预算+中介费',

'月利率': '利率 / 12',
'还款月数': '12*贷款年限',
'还款期数': '还款月数',


'每期还款额': '借款本金*月利率*(1+1.0/((1+月利率)**还款月数-1))',          
}

def showcalc(x):
    content, var = '', ''
    for c in x:
        if ord(c) < 128:
            if var:
                content += '%%(%s).2f(%s)'%(tl(var),var)
                var = ''
            content += c
        else:
            var += c

    if var:
        content += '%%(%s).2f(%s)'%(tl(var),var)

    dc = sys._getframe(1).f_locals
    dc.update(sys._getframe(1).f_globals)
    
    print content % dc
    
            
def solve(param):
    fpool, delidcs = formulas, True
    fpool.update(param)
    while delidcs:
        delidcs = []
        for k,v in fpool.items():
            try:
                if isdef(k):
                    delidcs.append(k)
                    continue
                cmd = "%s = %s"%(k,v)
                exec tl(cmd)
                showcalc(cmd)
                delidcs.append(k)
            except NameError as e:
                m = re.match(r"name \'(\w+)\' is not defined", e.message)
                if m:
                    pass
#                     print '-->需要"%s"才能计算"%s"'%(tohz(m.group(1)), fvars)
        
        for k in delidcs:
            del fpool[k]


    print '初次支出: %.2f'%eval(tl('初次支出'))
    

if __name__ == '__main__':
    solve({'总价':'245*万',
           '面积':'64',
           '贷款年限':'20',
           })
