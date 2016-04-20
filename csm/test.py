# -*- coding: utf-8 -*-

'''
Created on 2014年6月4日

@author: zhouzhichao
'''


a1Freq=440.0


class Tune(object):
    def __init__(self, key):
        self.key = 0
        pass
    
    def get(self, n):
        return n


#生成律
class NoteGen(object):
    def __init__(self):
        pass
    
    def produce(self):
        pass
    
    def getFreq(self):
        pass
    
    def getKeys(self):
        array = []
        KL = ["C","#C","D","#D","E","F","#F","G","#G","A","#A","B"]
        for i in range(2,0,-1):
            for j in KL:
                array.append('%s%s'%(j,i))
        
        for j in KL:
            array.append(j)
        for i in range(len(KL)):
            KL[i] = KL[i].lower()
        for j in KL:
            array.append(j)
            
        for i in range(1,6):
            for j in KL:
                array.append('%s%s'%(j,i))
                
        return array#[9:-11]
    
    def getTranstable(self):
        tab = {}
        arr = self.getKeys()
        for i in range(len(arr)):
            tab[arr[i]] = i
            
            tab['#'+arr[i]] = i+1   #
            if '#' in arr[i]:
                tab['%s%s'%('b', arr[i+1])] = i
            else:
                tab['##'+arr[i]] = i+2
                tab['bb'+arr[i]] = i-2
            
        return tab
        
        

class Avg12Gen(NoteGen):
    def __init__(self):
        super(Avg12Gen, self).__init__()
        self.tab = super(Avg12Gen, self).getTranstable()
        self.a1 = self.tab['a1']
        self.rate = 2.0**(1/12.0)
        self.freq = []
        self.produce()
        

    def produce(self):
        for i in range(self.tab['#b5']):
            self.freq.append(a1Freq * self.rate **(i - self.a1))
            
            
    def getFreq(self, ym):
        return self.freq[self.tab[ym]]



class TuneGen(NoteGen):
    def __init__(self):
        super(TuneGen, self).__init__()
        self.tab = super(TuneGen, self).getTranstable()
        self.a1 = self.tab['a1']
        self.produce()
        
        
    def produce(self):
        top = self.tab['#b5']
        tmp = [0 for i in range(top)]
        
        tmp[self.a1] = a1Freq
        tmpsize = top - 1
        s = self.a1
        stk = []
        while tmpsize:
            if s + 12 < top and tmp[s+12]==0:
                tmp[s+12] = 2*tmp[s]
                tmpsize -= 1
                stk.append(s+12)
            if s - 12 >= 0 and tmp[s-12]==0:
                tmp[s-12] = tmp[s]/2
                tmpsize -= 1
                stk.append(s-12)
            if s + 7 < top and tmp[s+7]==0:
                tmp[s+7] = 1.5*tmp[s]
                tmpsize -= 1
                stk.append(s+7)
            if s - 7 >= 0 and tmp[s-7]==0:
                tmp[s-7] = tmp[s]/1.5
                tmpsize -= 1
                stk.append(s-7)
            if len(stk)>0:
                s = stk.pop(0)
            else:
                break
        self.freq = tmp
        
    def getFreq(self, ym):
        return self.freq[self.tab[ym]]



if __name__ == '__main_1_':
    ng = NoteGen()
    ks = ng.getKeys()
    
    mp = ng.getTranstable()
    agg={}
  
    
    for k,v in mp.items():
        if agg.get(v) is None:
            agg[v] = [k] 
        else:
            agg[v].append(k)

#     for i in range(len(ks)):
#         print agg[i]
        
    print (2.0**(1/12.0))**7
    ag = Avg12Gen()
    for i in 'cdefgab':
        print ag.getFreq(i),
    print
#     print mp['a1'],mp['##g1'],mp['bbb1']
#     print mp['#c'],mp['##B']#,mp['']
    tg = TuneGen()
    for i in 'cdefgab':
        print tg.getFreq(i),
    print
    pass

class obj():
    def __init__(self):
        self.config = 'my config'
        self.fuck   = 'with U'
        self.sleep  = 'never'
    

if __name__ == '__main__':
    mdict={}#{'config': 'yours', 'fuck':'no way', 'slep': 'immediately'}
    a=obj()
    print a.__dict__
    a.__dict__.update(mdict)
    print "config:%s\nfuck:%s\nsleep:%s"%(a.config,a.fuck,a.sleep)
    print a.slep
    