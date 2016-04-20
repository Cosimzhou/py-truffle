#coding: UTF-8

import random


SIZE_CONFIG = 4

def log(num):
    cnter = 0
    while num > 1:
        num >>= 1
        cnter +=1
    return cnter

class board(object):
    def __init__(self):
        self._data = [0]*(SIZE_CONFIG**2)
        self._newp = -1
        
    def clone(self):
        cln = board()
        cln._data = map(lambda x:x, self._data)
        return cln
        
    def __repr__(self):
        strtxt = '' 
        for i in xrange(len(self._data)):
            if i and i % SIZE_CONFIG == 0:
                strtxt += '\n'
            strtxt += (" %4d " if i != self._newp else '[%4d]')%self._data[i]
        return strtxt
    
    def put(self, n, p):
        if p<0 or p>=len(self._data) or n not in (2,4):
            return
        if self._data[p]:
            return
        self._data[p] = n
        self._newp = p
    
    def produceInfo(self):
        maxv, minv, sumv = 0, 2049, 0
        cnter = {0:0} 
        for x in self._data:
            if maxv < x: maxv = x
            if minv > x and x > 0: minv = x
            cnter[x] = cnter.get(x, 0) + 1
            sumv += x 
        cnter['max'] = maxv
        cnter['min'] = minv
        cnter['sum'] = sumv
        return cnter
        
    def moveableup(self):
        for x in xrange(SIZE_CONFIG):
            y0, ana, first = x, False, True
            for y in xrange(x, SIZE_CONFIG*4, SIZE_CONFIG):
                if self._data[y]:
                    if ana:
                        return True
                    if not first and self._data[y] == self._data[y0]:
                        return True
                    y0 = y
                else:
                    ana = True
                first = False
        return False
    def moveup(self):
        for x in xrange(SIZE_CONFIG):
            y0, first = x, True
            for y in xrange(x, SIZE_CONFIG*4, SIZE_CONFIG):
                if self._data[y]:
                    num, self._data[y] = self._data[y], 0
                    if self._data[y0] == num:
                        self._data[y0] *= 2
                        y0 += SIZE_CONFIG
                    else:
                        if not first and self._data[y0]: 
                            y0 += SIZE_CONFIG
                        self._data[y0] = num
                    first = False
        return True
        
    def moveabledown(self):
        for x in xrange(SIZE_CONFIG):
            x = len(self._data)-1-x
            y0, ana, first = x, False, True
            for y in xrange(x, -1, -SIZE_CONFIG):
                if self._data[y]:
                    if ana:
                        return True
                    if not first and self._data[y] == self._data[y0]:
                        return True
                    y0 = y
                else:
                    ana = True
                first = False
        return False
    def movedown(self):
        for x in xrange(SIZE_CONFIG):
            x = len(self._data)-1-x
            y0, first = x, True
            for y in xrange(x, -1, -SIZE_CONFIG):
                if self._data[y]:
                    num, self._data[y] = self._data[y], 0
                    if self._data[y0] == num:
                        self._data[y0] *= 2
                        y0 -= SIZE_CONFIG
                    else:
                        if not first and self._data[y0]: 
                            y0 -= SIZE_CONFIG
                        self._data[y0] = num
                    first = False
        return True
        
    def moveableleft(self):
        for y in xrange(SIZE_CONFIG):
            y *= SIZE_CONFIG
            x0, ana, first = y, False, True
            for x in xrange(SIZE_CONFIG):
                x += y
                if self._data[x]:
                    if ana:
                        return True
                    if not first and self._data[x] == self._data[x0]:
                        return True
                    x0 = x
                else:
                    ana = True
                first = False
        return False
    def moveleft(self):
        for y in xrange(SIZE_CONFIG):
            y *= SIZE_CONFIG
            x0, first = y, True
            for x in xrange(SIZE_CONFIG):
                x += y 
                if self._data[x]:
                    num, self._data[x] = self._data[x], 0
                    if self._data[x0] == num:
                        self._data[x0] *= 2
                        x0 += 1
                    else:
                        if not first and self._data[x0]: 
                            x0 += 1
                        self._data[x0] = num
                    first = False
        return True                    
                    
    def moveableright(self):
        for y in xrange(SIZE_CONFIG):
            y = (y+1)*SIZE_CONFIG-1
            x0, ana, first = y, False, True
            for x in xrange(SIZE_CONFIG):
                x = y-x
                if self._data[x]:
                    if ana:
                        return True
                    if not first and self._data[x] == self._data[x0]:
                        return True
                    x0 = x
                else:
                    ana = True
                first = False
        return False
    def moveright(self):
        for y in xrange(SIZE_CONFIG):
            y = (y+1)*SIZE_CONFIG-1
            x0, first = y, True
            for x in xrange(SIZE_CONFIG):
                x = y-x 
                if self._data[x]:
                    num, self._data[x] = self._data[x], 0
                    if self._data[x0] == num:
                        self._data[x0] *= 2
                        x0 -= 1
                    else:
                        if not first and self._data[x0]: 
                            x0 -= 1
                        self._data[x0] = num
                    first = False
        return True
    
    def move(self, direct):
        direct %= 4
        if direct == 0 and self.moveableup():
            self.moveup()
        elif direct == 1 and self.moveableleft():
            return self.moveleft()
        elif direct == 2 and self.moveabledown():
            return self.movedown()
        elif direct == 3 and self.moveableright():
            return self.moveright()
        self._newp = -1
        return False
    def getNil(self, idx):
        if idx <= 0:
            idx = 1
        inidx = idx
        while idx:
            for i in xrange(len(self._data)):
                if not self._data[i]:
                    idx -= 1
                    if not idx:
                        return i
         
            if inidx == idx:
                return -1
    def genNil(self):
        for i in xrange(len(self._data)):
            if self._data[i] == 0:
                yield i
            
    def data(self, x, y=None):
        if y is None:
            if 0 <= x < len(self._data):
                return self._data[x]
        else:
            if 0 <= x < SIZE_CONFIG and 0 <= y < SIZE_CONFIG:
                return self._data[x+y*SIZE_CONFIG]
        #raise Exception('subscript out of range.')
    
    @staticmethod
    def deltaDir(direction):
        return (-SIZE_CONFIG,-1,SIZE_CONFIG,1)[direction]
    
    def moveWithinBounds(self, direction, start, end):
        if 0 <= end < len(self._data):
            if direction % 2:
                return end/SIZE_CONFIG != start/SIZE_CONFIG
            else:
                return True
        return False
    
    def findFarthestPosition(self, cell, direction):
        # Progress towards the vector direction until an obstacle is found
        vector = board.deltaDir(direction)
        while True:
            previous = cell;
            cell     = previous + vector
            if not (self.moveWithinBounds(direction, previous, cell) and self._data[cell]):
                break
        
        return cell
        
    def smoothness(self):
        smoothness = 0
        for x in xrange(SIZE_CONFIG):
            for y in xrange(SIZE_CONFIG):
                content = self.data(x, y) 
                if content:
                    value = log(content)
                    for direction in (0,1): 
#                         var vector = this.getVector(direction);
                        targetCell = self.findFarthestPosition(x+y*SIZE_CONFIG, direction);
                        target = self.data(targetCell)
                        if target:
                            targetValue = log(target)
                            smoothness -= abs(value - targetValue)
                        
        return smoothness


    def monotonicity(self):
        highestValue = 0
        highestCell = 0
        for i in xrange(len(self._data)):
            if self._data[i] and self._data[i] > highestValue:
                highestValue = self._data[i]
                highestCell = i
            
        marked, queued= [False]*len(self._data), [False]*len(self._data)
        queued[highestCell] = True
        markList, cellQueue= [highestCell], [highestCell]
        markAfter, increases = 1, 0# only mark after all queued moves are done, as if searching in parallel
        
        def markAndScore(cell):
            markList.append(cell)
            value = self._data[cell]
            if (value):
                value = log(value)
            
            for direction in [0,1,2,3]:
                vector = board.deltaDir(direction)
                target = cell + vector

                if self.moveWithinBounds(direction, cell, target) and not marked[target]:
                    targetValue = log(self._data[target])
                    if targetValue:
                        if targetValue > value:
                            increases += targetValue - value;
                      
                    if not queued[target.x][target.y]:
                        cellQueue.append(target)
                        queued[target] = True
                 
            
            if markAfter == 0:
                while markList.length > 0:
                    cel = markList.pop()
                    marked[cel] = True
                markAfter = cellQueue.length
            
        
        
        while cellQueue.length > 0:
            markAfter -=1
            markAndScore(cellQueue.shift())
        
        return -increases;



    def monotonicity2(self):
        totals = [0, 0, 0, 0]
        
        # up/down direction
        for x in xrange(SIZE_CONFIG):
            current = 0
            next = current+1
            while next < SIZE_CONFIG:
                while next < 4 and not self.data(x, next): 
                    next +=1
                
                if next>=4: next -= 1
                currentValue = log(self.data(x, current)) 
                nextValue = log(self.data(x, next)) 
                if currentValue > nextValue:
                    totals[0] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[1] += currentValue - nextValue
                current = next
                next += 1
    
        
        # left/right direction
        for y in xrange(SIZE_CONFIG):
            current, next = 0, current+1
            while next<SIZE_CONFIG:
                while next < 4 and not self._data(next, y):
                    next += 1
    
                if next >= SIZE_CONFIG: next -= 1
                currentValue = log(self.data(current, y))
                nextValue = log(self.data(next, y)) 
                if currentValue > nextValue:
                    totals[2] += nextValue - currentValue;
                elif nextValue > currentValue:
                    totals[3] += currentValue - nextValue;
    
                current = next
                next += 1
    
        return max((totals[0], totals[1])) + max((totals[2], totals[3]))

            
nmb = board()
def gameRound():
    print nmb
    aih = AIhint(nmb)
    if aih < 0:
        print 'Game over'
        return False
    print 'AI suggestion is %s'% ('▲','◀︎','▼','►')[aih]
    
    
    manual = 0#True
    if manual:
        d = raw_input('xxx:')
        try:
            d = int(d)
        except:
            d = aih
            print 'accepted suggestion', d
            d = aih
    else:
        d = aih
        
    if not nmb.move(d):
        return True
    
    np = nmb.getNil(random.randint(0,16))
    if np >= 0:
        num = random.choice([2, 4])
        nmb.put(num, np)
    elif not nmb:
        return False
    return True

def AIhint(mb):
    maxv, gooddir = float('-INF'), -1
    for i in xrange(4):
        back = mb.clone()
        if back.move(i):
            #eval it
            val = evalBoard(back)
            if val > maxv:
                maxv = val
                gooddir = i
            elif val == maxv:
                if random.random()>=0.5:
                    maxv = val
                    gooddir = i
    return gooddir
    
    
def evalBoard(bd):
    info = bd.produceInfo()
    if info[0] > SIZE_CONFIG**2/2:
        return leastNum(bd)*100
    elif info[0] > SIZE_CONFIG**2/4:
        worst = float('INF')
        for p in bd.genNil():
            for n in (2, 4):
                tbd = bd.clone()
                tbd.put(n, p)
                ln = leastNum(tbd)
                if ln < worst:
                    worst = ln
        return worst*100
    else:
        inf = float('INF')
        return alpha_beta(bd, 3, -inf, inf)
        
def alpha_beta(bd, level, best, worst):
    for p in bd.genNil():
        for n in (2, 4):
            tbd = bd.clone()
            tbd.put(n, p)
            if level <= 0:
                v = leastNum(tbd)*100
                if v > best: best = v 
            else:
#                 best = float('-INF')
                for d in xrange(4):
                    dbd = tbd.clone()
                    dbd.move(d)
                    v = alpha_beta(dbd, level-1, best, worst)
                    if v > best:
                        best = v
                    if v >= worst:
                        break
            if best < worst:
                worst = best
                            
    return worst
    
def leastNum(bd):
    maxv = 0
    for i in range(4):
        tbd = bd.clone()
        if tbd.move(i):
            nil = tbd.produceInfo()[0]
            if nil > maxv:
                maxv = nil
    return maxv
        
        
        
def neighbourInfo(bd):
    for x in xrange(SIZE_CONFIG):
        epn = [0, 0]
        prn = [x, x*SIZE_CONFIG]
        for y in xrange(SIZE_CONFIG):
            sp = [x+y*SIZE_CONFIG, x*SIZE_CONFIG+y]
            for i in (0, 1):
                if bd._data[prn[i]]:
                    if sp[i] != prn and bd._data[sp[i]] == bd._data[prn[i]]:
                        epn[i] += 1
                        
                    prn[i] = sp[i] 

if __name__ == '__main__':
    b = nmb
    b.put(random.choice([2, 4]), random.randint(0,len(b._data)-1))
    b.put(random.choice([2, 4]), b.getNil(random.randint(0,16)))
    while gameRound():
        pass
 
    
    
    
    
    
    