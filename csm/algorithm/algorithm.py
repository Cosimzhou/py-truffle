# coding: gbk

def xbin(value, bit=0):
    return ('0'*bit+bin(int(value))[2:])[-bit:]



class polynome(object):
    def __init__(self, **kwargs):
        order = kwargs.get('order')
        value = kwargs.get('value')
        if not order or order < 0: order = 0
        if type(value) is str:
            self.assign(value)
        elif type(value) is int:
            self.assign(bin(value)[2:])
        else:
            self.rates = [False]*order
    def assign(self, value):
        if type(value) is int: value = bin(value)[2:]
        self.rates = map(lambda x: x != '0', value)
        self.rates.reverse()
    def order(self):
        if len(self.rates) <= 0:
            return 0
        for i in xrange(len(self.rates)):
            if self.rates[-1-i]:
                return len(self.rates)-i
        return 0
    def mul(self, poly):
        result = polynome(order=self.order()+poly.order()-1)
        for i in xrange(poly.order()):
            if poly.rates[i]:
                for j in xrange(self.order()):
                    result.rates[i] ^= self.rates[j]
                    i += 1 
        return result
    def clone(self):
        poly = polynome()
        poly.rates = map(lambda x:x, self.rates)
        return poly
    def mod(self, poly):
        if type(poly) is not polynome:
            if type(poly) is not int :
                data = eval('0b'+''.join(map(lambda x: '0' if not x or x=='0' else '1', poly)))
            if data == 0:
                raise Exception('polynome divided by zero')
            data = bin(data)[::-1][:-2]
            poly = polynome(value=data)
        sord, pord = self.order(), poly.order()
        if pord == 0:
            raise Exception('polynome divided by zero')
        if sord < pord:
            return self.clone()
        memory = map(lambda x: x, self.rates[:sord])
        
        assert memory[-1]
        top, genlen = sord, pord

        while top >= genlen:
            for i in xrange(genlen):
                memory[top-i-1] ^= poly.rates[genlen-i-1]
            
            for i in xrange(1,sord):
                if memory[-i]:
                    top = sord-i+1
                    break
            if not memory[top-1]:
                break
        
        for i in xrange(len(memory)):
            if memory[-1-i]:
                top = len(memory)-i
                break
        return polynome(value=''.join(map(lambda x: '1' if x else '0', memory[:top][::-1])))
    def getValue(self):
        value, key = 0, 1
        for i in xrange(len(self.rates)):
            if self.rates[i]:
                value += key
            key *= 2
        return value

    def printf(self, **format):
        return (''.join(map(lambda x: '1' if x else '0', self.rates)))[::-1]

class GaloisField(object):
    def __init__(self, bottom, exp=1):
        self.top = bottom**exp
        self.gtop = self.top - 1
        self.gen = 1
        self.module = 2
        self.ord2val = {}
        self.val2ord = {}
    def generate(self, gen, module):
        self.gen = gen % self.top
        a, c = polynome(value=gen), polynome(value=gen)
        m = polynome(value=module)
        a2n = {0:1}        
        order = 0
        while order != len(a2n) and len(a2n) < self.gtop:
            order = (order + 1) % self.gtop
            a2n[order] = c.getValue()
            c = a.mul(c).mod(m)
        self.ord2val = a2n
        self.val2ord = {v:k for k, v in a2n.items()}
        self.val2ord[0] = self.val2ord.get(self.gtop) 
    def getOrder(self, value):
        return self.val2ord.get(value%self.gtop)
    def getValue(self, order):
        return self.ord2val.get(order%self.gtop)
    def mod(self, value):
        return value % self.gtop
    def mul(self, a, b):
        oa, ob = self.getOrder(a), self.getOrder(b)
        so = (oa+ob) % self.gtop
        return self.getValue(so)
    def add(self, a, b):
        return (a^b)%self.gtop

#Galois field    
def getRates(pn, GF):
    def add(a, b):
        va, vb = GF.getValue(a), GF.getValue(b)
        if va is None or vb is None:
            print a,b
        vab = va ^ vb
        return GF.getOrder(vab)
    if pn <1: return    
    result = [0]*(pn+1)

    for k in xrange(1, pn):
        for i in xrange(k, 0, -1):
            result[i] = add(result[i]+k, result[i-1])
        result[0] += k
    result[0]  = GF.mod(result[0])
    return result        

if __name__ == '__main__':
#     # gen, module = 0x9d, 0x11d
# #     gen, module = '10011101', '100011101' #'100011011'
#     gen, module = '1011', '100011101' #'100011011'
#     for gen in (0x2,0x4,0x10,0x4c,0x85,0x9d):#xrange(1, 256):
#         a = polynome(value=gen)
#         b = polynome(value=gen)
# #         print "a=",
# #         a.printf()
# #         print "b=",
# #         print "gen=%s, mod=%s"%(hex(eval('0b'+gen)), hex(eval('0b'+module)))
#         b.printf()
#         a2n = {0:1,1:gen}
#         m = polynome(value=module)
#         c = a.mul(b)
#         sss = set([])
#         oldsize = -1
#         n = 2
#         while oldsize != len(sss):
#             oldsize = len(sss)
#             c = c.mod(m)
#             val= c.printf()
#             ival=eval('0b'+val)
#             a2n[n] = ival
#             n += 1
# #             print hex(ival)
#             sss.add(ival)
#             c = a.mul(c)
#             
#         if len(sss) < 255:
#             continue
#         print 'Gen: %s'%hex(gen)
#         n2a = {v:k for k, v in a2n.items()}
#         n2a[0] ='Nan'
#         
# #         #102
# #         val = reduce(lambda x,y:x^y, map(lambda x: a2n[21-x], range(7))) 
# #         print val, n2a[val], hex(a2n[len(a2n)-1]),hex(a2n[0])
# #         
# #         #32      
# #         val = reduce(lambda x,y:x^y, map(lambda x: a2n[45-x], range(10))) 
# #         print val, n2a[val], hex(a2n[len(a2n)-1]),hex(a2n[0])
# # 
# #         #140
# #         val = reduce(lambda x,y:x^y, map(lambda x: a2n[78-x], range(13))) 
# #         print val, n2a[val], hex(a2n[len(a2n)-1]),hex(a2n[0])
# #         
# #         #35
# #         val = reduce(lambda x,y:x^y, map(lambda x: a2n[(780-x)%255], range(40))) 
# #         print val, n2a[val], hex(a2n[len(a2n)-1]),hex(a2n[0])
#         #238
#         Nr = [40,87,0]
#         Nr[2] = Nr[0]*(Nr[0]-1)/2
#         aarr = [(x, 0) for x in xrange(Nr[0])]# for y in xrange(x+1,Nr[0])]
#         val = reduce(lambda x,y:x^y, map(lambda x: a2n[((x[0]))%255], aarr)) 
#         print val, n2a[val], hex(a2n[len(a2n)-1]),hex(a2n[1])
#         
#         
# #         b = polynome(value='10111110')
# #         c = a.mul(b)
# #         c = c.mod(m)
# #         print hex(eval('0b'+c.printf()))
#     
    k = 10
    gf = GaloisField(2,8)
    gf.generate(0x9d, 0x11d)  #GB = 0x9d 0x11d
    rates = map(lambda x: gf.getValue(x), getRates(k,gf))
    data = '00010000001000000000110001010110011000011000000011101100000100011110110000010001111011000001000111101100000100011110110000010001'
    buf, arrdata = [0] * k, []
    ldata = len(data) / 8
#     for i in xrange(ldata):
#         text = eval('0b'+data[8*i: 8*i+8])
#         arrdata.append(text)
#      
#     for i in xrange(ldata-k):
#         hai = arrdata[i]
#         if hai == 0: continue
#         for j in xrange(k+1):
#             arrdata[i+j] ^= gf.mul(hai, rates[-1-j])
#     
#     chkcode = ''
#     for i in xrange(k):
#         chkcode = xbin(arrdata[-1-i], 8) +chkcode 
                
    buffer = 0
    for i in xrange(ldata):
        text = eval('0b'+data[8*i: 8*i+8])    
        xxoo = buffer ^ text
        buffer = buf[-1]
        for j in xrange(k):
#             j = k-1-j
            tmp = gf.mul(xxoo, rates[j])
            if j > 0:
                buf[j] = buf[j-1] ^ tmp
            else:
                buf[j] = tmp 
     
    chkcode = ''
#     for i in xrange(k):
#         chkcode += xbin(buf[-1], 8) 
#         for j in xrange(k):
#             tmp = gf.mul(0, rates[j])
#             if j > 0:
#                 buf[j] = buf[j-1] ^ tmp
#             else:
#                 buf[j] = tmp
#         print buf#[-1]         
      
    print gf.mul(1, 112)
    for i in xrange(k):
        chkcode = xbin(buf[i], 8) +chkcode
     
#         
#     rates.reverse()
#     print rates

    print chkcode
    print data+chkcode#+('0'*7)

    pass