#coding: UTF-8
#! /usr/bin/python
import re, argparse, random, math
"""
    ItemList is a dict which infers items to its quantity map.
"""

ProcPath='/Users/zhouzhichao/.simcity'

itemDict = {}   #""" str => Item """
shopDict = {}   #""" str => Shop """
ADD=lambda x,y:x+y

class Item(object):
    def __init__(self):
        self.idx = 0
        self.name = None
        self.materializable = True
    def add(self, key, value):
        if re.match(r"\d+$", value):
            value = int(value)
        tmp = self.__dict__.get(key)
        if tmp is None:
            tmp = value
        elif type(tmp) is list:
            tmp.append(value)
        else: 
            tmp = [tmp, value]
        self.__dict__[key]=tmp
        self.idx += 1
    def allAlias(self):
        return self.alias.split(',')
    def materials(self):
        return ItemList(self.material)
    def materialsFromFactory(self):
        maters, primater = self.materials(), ItemList()
        while maters:
            item = maters.__iter__().next()
            num = maters[item]
            if item.material:
                maters.add(item.materials())
            else:
                primater.add({item:num})
            del maters[item]
        return primater
    def costs(self):
        return self.materials().price()
    def __repr__(self):
        return self.name
    def info(self):
        cost = self.costs()
        benefit = self.price-cost
        mt = ('need (%s) '% self.material) if self.material else ''
        return '''%s $%d %s %scost %d mins & $%d. Benefit $%d; appreciate $%.2f perminute.'''   \
                % (self.name, self.price, self.shop, mt, self.time, cost, benefit, float(benefit)/self.time)

"""
    Item => int
"""
class ItemList(dict):
    def __init__(self, arg=None):
        if not arg:
            pass
        elif type(arg) in (list, tuple, dict):
            self.update(dict(arg))
            self.check()
        elif type(arg) is ItemList:
            self.update(arg)
        elif type(arg) is str:
            ItemList.parseToList(arg, self)
        elif type(arg) is Item:
            self[arg] = 1
        else:
            print 'invalid arguments to init ItemList.'
            exit(1)
    def __repr__(self):
        return ','.join(map(lambda x:'%s*%d'%x, self.items()))
    def __len__(self):
        return self.count()
    def check(self):
        unexpected = True
        while unexpected:
            unexpected = False
            for k in self:
                if type(k) is not Item:
                    item = itemDict[k]
                    if item is None:
                        print 'unexpected item name:%s'%k
                        exit(1)
                    v = self[k]
                    self[item] = v
                    del self[k]
                    unexpected = True
                    break
    @staticmethod
    def parseToList(goodslist, itemlist):
        for n in goodslist.split(','):
            tmparr=n.split('*')
            name, num = n, 1
            if len(tmparr) == 2: 
                name, num = tmparr
            elif len(tmparr) != 1:
                print 'items should follow format "itemName*count"'
                exit(0)
            item = itemDict.get(name)
            if type(item) is not Item:
                print 'wrong item name input: %s'%name
                exit(0)
            count = itemlist.get(item)
            if count is None: count = 0
            itemlist[item] = count + int(num)
    @staticmethod
    def parse(goodslist):
        itemlist = ItemList()
        ItemList.parseToList(goodslist, itemlist)
        return itemlist
    def price(self):
        itemlist = self.items()
        return reduce(ADD, map(lambda x:x[0].price*x[1], itemlist), 0)
    def count(self):
        return reduce(ADD, self.values(), 0)
    def add(self, adder, cap=None):
        if type(adder) is not ItemList:
            adder = ItemList(adder)
        if cap:
            num, anum = self.count(), adder.count()
            if cap <num+anum:
                print "can't add %s to %s, because there is no much more capacity %d/%d"%(adder, self, num, cap)
                exit(0)
        for i in adder:
            tmp = self.get(i)
            if tmp is None:
                self[i] = adder[i]
            else:
                self[i] = adder[i]+tmp
    def substract(self, adder):
        if type(adder) is not ItemList:
            adder = ItemList(adder)
        for i in adder:
            tmp, num = self.get(i), adder[i]
            if tmp is None:
                print 'there is no %s in storage' % i
                exit(0)
            elif tmp < num:
                print 'there is no enough %s in storage, only %d but %d in need.' % (i, tmp, num)
                exit(0)
            elif tmp == num:
                del self[i]
            else:
                self[i] = tmp-num
    def lack(self, need):
        if type(need) is not ItemList:
            need = ItemList(need)
        ret = ItemList()
        for i in need:
            tmp, num = self.get(i), need[i]
            if tmp is None:
                ret[i] = num
            elif tmp < num:
                ret[i] = num-tmp
        return ret    
    def filt(self, proc):
        return ItemList(filter(proc, self.items()))
        
class Shop(object):
    StarEffects=(1,0.9,0.85,0.8)
    def __init__(self, name):
        self.name = name
        self.proactive = False
        self.goods = [] # Item list
        self.star = 0
    def __repr__(self):
        return self.name
    def addGoods(self, goods):
        self.goods.append(goods)
    def info(self):
        return "%s could produce:%s"%(self.name, ','.join(map(lambda x:x.name, self.goods)))
    def makeableGoods(self, store):
        return filter(lambda x:len(store.lack(x.materials()))==0, self.goods) if self.name != '工厂' else self.goods
    def getMaxAppraciator(self):
        mag, maxv = None, 0
        for g in self.goods:
            if g.time:
                va = (g.price - g.costs())/g.time
                if va > maxv: mag, maxv = g, va
        return mag

class Worker(object):
    WorkerNo = 0
    def __init__(self, shop):
        self.no = Worker.WorkerNo
        self.shop = shop if type(shop) is Shop else shopDict[shop]
        self.goods = None
        self.ftime = -1
        Worker.WorkerNo += 1
    def takeGoods(self):
        ret = ItemList(self.goods.name) if self.goods else None
        self.goods, self.ftime = None, -1
        return ret
    def assignGoods(self, goods, starttime):
        self.goods = goods
        self.ftime = int(math.ceil(60*goods.time*Shop.StarEffects[self.shop.star] + starttime))
    
    
class Simulator(object):
    def __init__(self):
        self.storehouse = None
        self.storecap = 250
        self.factoryNumber = 45
        self.shops = None 
        self.datapath = ProcPath
        
        self.resttimes = ((0,8*60),(22*60,32*60))
        self.starttime = 12*60*60
    def simulate(self, time):
        workers = [Worker('工厂') for _ in xrange(self.factoryNumber)] + \
             map(lambda x:Worker(x), filter(lambda x:x.proactive and x.name !='工厂', shopDict.values()))
        time *= 60
        cursor, cash = 0, 0
        while cursor < time:
            if len(self.storehouse) >= self.storecap:
                cash += self.sellGoodsInSimulating(cursor)
            nexthop = time
            for w in workers:
                goods_get, goods_pro = None, None
                if 0 < w.ftime <= cursor+0.5 and len(self.storehouse) < self.storecap:
                    goods_get = w.goods
                    self.storehouse.add(w.takeGoods())
                    
                if w.goods is None:
                    gs = w.shop.makeableGoods(self.storehouse)
                    if gs:
                        goods_pro = random.choice(gs)
                        w.assignGoods(goods_pro, cursor) 
                        self.storehouse.substract(goods_pro.materials())
                if goods_get or goods_pro:
                    print "@%s sh:%s%s %s%s"%(self.timeformat(cursor), w.shop, ("-%03d"%w.no if w.no <self.factoryNumber else ''), 
                                           ('get:%s '%goods_get if goods_get else ''), ('pr:%s'%goods_pro if goods_pro else ''))
                
                if w.ftime >= cursor and nexthop > w.ftime: 
                    nexthop = w.ftime
            
            cursor = self.skipRestTimeForSimulating(nexthop)
        for w in workers:
            if w.goods: print "%s left %d mins"%(w.goods,(w.ftime-cursor)/60)
        if cursor == time:
            print "simulating finish"
        else:
            print 'simulating stopped at %s' % self.timeformat(cursor)
        print "%d/%d => $%d + cash: $%d"%(len(self.storehouse), self.storecap, self.storehouse.price(), cash)
        print self.storehouse
    def skipRestTimeForSimulating(self, hop):
        tsecond = self.starttime+hop
        tmin = tsecond / 60
        ctime = tmin % 1440
        for a in self.resttimes:
            if a[0]<=ctime<a[1]:
                ctime = a[1]
                return ctime*60 + int(tmin/1440)*1440*60 -self.starttime      
        return hop
    def sellGoodsInSimulating(self, cursor):
        funcs = (lambda x:not x[0].materializable,
                 lambda x:not x[0].price>160,
                 lambda x:not x[0].price>50,
                 lambda x:True
                 )
        sg, phase = None, 0
        while phase < len(funcs) and not sg:
            sg = self.storehouse.filt(funcs[phase])
            phase += 1
        price = sg.price()
        print "@%s cash +%d sell goods: %s"%(self.timeformat(cursor), price, sg)
        self.storehouse.substract(sg)
        return price
    def timeformat(self, cursor):
        ctime = int(self.starttime+cursor)/60
        day = int(ctime / 1440)
        ctime %= 1440
        hour = int(ctime/60)
        mins, secs = ctime%60, ctime%60
        return "%d-%d:%02d:%02d"%(day, hour, mins, secs)
    def initData(self):
        self.storehouse = ItemList()
        csvfile = '%s/%s'%(self.datapath,'storehouse')
        with open(csvfile, 'r') as f:
            lineNo = 0
            for l in f.readlines():
                l = l.strip(' \n')
                if lineNo == 0:
                    self.storecap = int(l)
                else: 
                    self.storehouse.add(ItemList.parse(l))
                lineNo += 1
    def saveData(self):
        csvfile = '%s/%s'%(self.datapath,'storehouse')
        with open(csvfile, 'w') as f:
            f.write('%d\n'%self.storecap)
            for i in self.storehouse:
                count = self.storehouse[i]
                f.write('%s*%d\n'%(i, count))

    def storageUpgradeCheck(self):
        if self.storecap >= 350: return
        ndnum = self.storecap/10-3 if self.storecap < 340 else 35
        need = {x:ndnum for x in filter(lambda x:x.startswith('仓库'), map(lambda x:x[0], itemDict.items()))}
        lack = self.storehouse.lack(need)
        
        if len(lack):
            print 'need "%s" to upgrade storehose capacity, which value $%d in total.'%(lack, lack.price())

 
def globalDataInitialize(path):
    global itemDict
    
    vectorTitles = []
    terminalPros = set()
    titled = False
    csvfile = '%s/%s'%(path,'items.csv')
    with open(csvfile, 'r') as f:
        for l in f.readlines():
            l, item = l.strip(' \n'), Item()
            if l.startswith('#'): continue
            for w in l.split(';'):
                w = w.strip(' ')
                if titled:
                    item.add(vectorTitles[item.idx], w)
                else:
                    vectorTitles.append(w)
            if titled:
                shop = shopDict.get(item.shop)
                if shop is None:
                    shopDict[item.shop] = shop = Shop(item.shop)
                    shop.proactive = (item.time!=0)
                shop.addGoods(item)
    
                itemDict[item.name] = item
                terminalPros.add(item)
                for a in item.allAlias():
                    if a: itemDict[a] = item
            titled = True   
    
    for i in itemDict.values():
        for m in i.materials():
            if m in terminalPros:
                terminalPros.remove(m)
    for i in terminalPros:
        i.materializable = False
            
    csvfile = '%s/%s'%(path,'shops.csv')
    with open(csvfile, 'r') as f:
        for l in f.readlines():
            arr = l.strip(' \n').split(';')
            shop = shopDict.get(arr[0])
            if shop is None:
                print 'unknown shop %s in shops.csv'%arr[0]
                exit(1)
            shop.star = int(arr[1])
              
    Item.__setattr__ = None
    Shop.__setattr__ = None

if __name__ == '__main__':
    globalDataInitialize(ProcPath)
    S = Simulator()
    S.initData()
    
    parser = argparse.ArgumentParser(description="""simcity""")
    parser.add_argument('--item', '-i', help='输出产品相关信息')
    parser.add_argument('--console', '-c', help='进入产品相关的控制台')
    parser.add_argument('--list', '-l', help='物品清单')
    parser.add_argument('--factory', '-f', help='工厂同时生产的栏位数')
    parser.add_argument('--storehouse', '-s', help='设置仓库中存放的物品,clear用于清空仓库')
    args = parser.parse_args()
    
    if args.factory:
        S.factoryNumber = args.factory
              
    if args.item:
        item = itemDict.get(args.item)
        if item: 
            mff = item.materialsFromFactory()
            print item.info()
            print '%s price: $%d'%(mff, mff.price())
    
    if args.list:
        goodsList = ItemList.parse(args.list)
        print goodsList 
        print "price: $%d"%goodsList.price()
        
    if args.storehouse:
        if args.storehouse == 'clear':
            S.storehouse = ItemList()
        elif args.storehouse == 'check':
            print "Used/capacity: %d / %d\t Goods value: $%d"%(len(S.storehouse), S.storecap, S.storehouse.price())
            print S.storehouse
            S.storageUpgradeCheck()
        elif args.storehouse.startswith('cap:'):
            S.storecap = int(args.storehouse[4:])
        else:
            S.storehouse.add(ItemList.parse(args.storehouse))
      
#     args.console = 1  
    if args.console:
        S.storecap = 340
        S.storehouse = ItemList()
        S.simulate(1440*3)
        
        for s in shopDict.values():
            print "%s:%s"%(s,s.getMaxAppraciator())
    
    S.saveData()