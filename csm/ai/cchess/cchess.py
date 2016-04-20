#coding: UTF-8


OUTRANGE, EMPTYPIT  = 0, 1
XBOUND, YBOUND = 9, 10

class board(object):
    def __init__(self):
        self.data = [[EMPTYPIT]*YBOUND for _ in xrange(XBOUND)]
        pass
    
    def cch(self, x, y):
        return self.data[x][y] if 0<=x<XBOUND and 0<=y<YBOUND else 0
    
    def move(self, x, y, ax, ay):
        if 0<=x<XBOUND and 0<=y<YBOUND and 0<=ax<XBOUND and 0<=ay<YBOUND:
            if self.data[x][y] == EMPTYPIT:
                print ""
            else:
                self.data[ax][ay] = self.data[x][y]
                self.data[x][y] = EMPTYPIT
        else:
            print ""
            
    
    def copy(self):
        b = board()
        for i in xrange(XBOUND):
            for j in xrange(YBOUND):
                b.data[i][j] = self.data[i][j]
                
         

class man(object):
    UBOUND, LBOUND = 16, 5
    KING, SHI, BISHOP, KNIGHT, ROOK, CANNON, PAWN = 5, 6, 7, 8, 9, 10, 11
    menTypes = (KING, SHI, BISHOP, KNIGHT, ROOK, CANNON, PAWN)
    texts = (('帅','士','相','马','车','炮','兵'),('将','仕','象','馬','車','砲','卒'))
    texts = ('gsbnrcp','GSBNRCP')    
    
    def __init__(self, a):
        self.value = a
    
    @staticmethod
    def chm(clr, mid):
        return clr*man.UBOUND + man.menTypes[mid]
    
    @property
    def type(self):
        return self.value%man.UBOUND
    
    @property
    def side(self):
        return int(self.value/man.UBOUND) if self.value> man.LBOUND else -1 
     
    def __repr__(self):
        return man.texts[int(self.value/man.UBOUND)][(self.value%man.UBOUND)-5]
     
class cch():
    def __init__(self):
        self.board = board()
        pass
    
    def isLegalMove(self, x, y, ax, ay):
        chm, achm = self.board.cch(x, y), self.board.cch(ax, ay)
        if chm == OUTRANGE or chm == EMPTYPIT or achm == OUTRANGE:
            return False
        tchm = man(chm).type
        
    def genMoveKing(self, x, y):
        if x < 3 or x>5 or 2<y<7 or y<0 or y>9: return 

        if x > 3: yield (x-1,y)
        if x < 5: yield (x+1,y)
        if y < 2 or 7<=y<9: yield (x,y+1)
        if y > 7 or 0<y<=2: yield (x,y-1)
    
    def genMoveShi(self, x, y):
        if x < 3 or x>5 or 2<y<7 or y<0 or y>9: return 
        if y < 3:
            if (x+y)%2 != 1: return
            if y == 1:
                yield (3,0)
                yield (3,2)
                yield (5,0)
                yield (5,2)
            else:
                yield (4,1)
        elif y > 6:
            if (x+y)%2 == 1: return
            if y == 8:
                yield (3,9)
                yield (3,7)
                yield (5,9)
                yield (5,7)
            else:
                yield (4,8)
        
    def genMoveBishop(self, x, y):
        if y <= 4:
            if x%2!=0 or y%2!=0 or (x+y)%4!=2: return
            
            if x >= 2:
                if y >= 2 or self.board.cch(x-1, y-1)==EMPTYPIT:
                    yield (x-2, y-2) 
                if y <= 2 or self.board.cch(x-1, y+1)==EMPTYPIT:
                    yield (x-2, y+2)
            if x <= 8:
                if y >= 2 or self.board.cch(x+1, y-1)==EMPTYPIT:
                    yield (x+2, y-2) 
                if y <= 2 or self.board.cch(x+1, y+1)==EMPTYPIT:
                    yield (x+2, y+2)
        elif y >= 5:
            if x%2!=0 or y%2!=1 or (x+y)%4!=3: return
            
            if x >= 2:
                if y >= 7 or self.board.cch(x-1, y-1)==EMPTYPIT:
                    yield (x-2, y-2) 
                if y <= 7 or self.board.cch(x-1, y+1)==EMPTYPIT:
                    yield (x-2, y+2)
            if x <= 8:
                if y >= 7 or self.board.cch(x+1, y-1)==EMPTYPIT:
                    yield (x+2, y-2) 
                if y <= 7 or self.board.cch(x+1, y+1)==EMPTYPIT:
                    yield (x+2, y+2)
        
        
    def genMoveKnight(self, x, y):
        if y>1 and self.board.cch(x, y-1):
            if x>0: yield (x-1, y-2)
            if x<8: yield (x+1, y-2)
        if y<8 and self.board.cch(x, y+1):
            if x>0: yield (x-1, y+2)
            if x<8: yield (x+1, y+2)
        if x>1 and self.board.cch(x-1, y):
            if y>0: yield (x-2, y-1)
            if y<9: yield (x-2, y+1)
        if x<7 and self.board.cch(x+1, y):
            if y>0: yield (x+2, y-1)
            if y<9: yield (x+2, y+1)

        
    def genMoveRook(self, x, y):
        flag, dfs = 4, [True]*4
        for i in xrange(1,11):
            if flag == 0: return
            if dfs[0]:
                if self.board.cch(x-i, y) == EMPTYPIT:
                    yield (x-i,y)
                else:
                    dfs[0] = False
                    flag -= 1
                    if x-i>=0: yield (x-i,y)
            if dfs[1]:
                if self.board.cch(x+i, y) == EMPTYPIT:
                    yield (x+i,y)
                else:
                    dfs[1] = False
                    flag -= 1
                    if x+i<=8: yield (x+i,y)
            if dfs[2]:
                if self.board.cch(x, y-i) == EMPTYPIT:
                    yield (x,y-i)
                else:
                    dfs[2] = False
                    flag -= 1
                    if y-i>=0: yield (x,y-i)
            if dfs[3]:
                if self.board.cch(x, y+i) == EMPTYPIT:
                    yield (x,y+i)
                else:
                    dfs[3] = False
                    flag -= 1
                    if y+i<=9: yield (x,y+i)
                    
            
    def genMoveCannon(self, x, y):
        flag, dfs = 4, [2]*4
        for i in xrange(1,11):
            if flag == 0: return
            if dfs[0]:
                if self.board.cch(x-i, y) == EMPTYPIT:
                    if dfs[0]==2: yield (x-i,y)
                else:
                    dfs[0] -= 1
                    if dfs[0]== 0: 
                        flag -= 1
                        if x-i>=0: yield (x-i,y)
            if dfs[1]:
                if self.board.cch(x+i, y) == EMPTYPIT:
                    if dfs[1]==2: yield (x+i,y)
                else:
                    dfs[1] -= 1
                    if dfs[1]== 0:
                        flag -= 1
                        if x+i<=8: yield (x+i,y)
            if dfs[2]:
                if self.board.cch(x, y-i) == EMPTYPIT:
                    if dfs[2]==2: yield (x,y-i)
                else:
                    dfs[2] -= 1
                    if dfs[2]== 0:
                        flag -= 1
                        if y-i>=0: yield (x,y-i)
            if dfs[3]:
                if self.board.cch(x, y+i) == EMPTYPIT:
                    if dfs[3]==2: yield (x,y+i)
                else:
                    dfs[3] -= 1
                    if dfs[3]== 0:
                        flag -= 1
                        if y+i<=9: yield (x,y+i)

            
             
    
    def isLegalMoveGeneral(self, x, y, ax, ay):
        pass
    def isLegalMoveRook(self, x, y, ax, ay):
        
        pass
    
aa=    """
┌┬┬┲┳┱┬┬┐
├┼┼╊╋╉┼┼┤
├┼┼╄╇╃┼┼┤
├┼┼┼┼┼┼┼┤
├┴┴┴┴┴┴┴┤
├┬┬┬┬┬┬┬┤
├┼┼┼┼┼┼┼┤
├┼┼╆╈╅┼┼┤
├┼┼╊╋╉┼┼┤
└┴┴┺┻┹┴┴┘

    """
if __name__ == '__main__':
    b = board()
    a= (0,1,2,3)
    b.move(*a)
    print aa
