#coding: UTF-8

class pt(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class block(object):
    def __init__(self):
        self.linearr = []
        self.code = None
        
    def __len__(self):
        return len(self.linearr)
    
class tile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = []
    def __len__(self):
        return len(self.blocks)
    
class tilemap(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.data = [[None]*x for _ in xrange(y)]
    
    def __getitem__(self, i):
        return self.data[i]