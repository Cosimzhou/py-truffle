#coding: UTF-8

import argparse,random

args=None
GameOver=False

WIN_VAL, LOSE_VAL, WALL = float('Inf'), 1e+307, -127
ROW_NUM = 15
ROW_TOP = ROW_NUM+1
ROW_RNG = ROW_NUM+2

LINE_PATTERNS=('┌','┬','┐','├','┼','┤','└','┴','┘','─','│')
CHM_PATTERNS=('─','●','○')
REPR_SIMPLE = False

class GomokuBoard(object):
    DIR_DELTA=((1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1))
    def __init__(self):
        self._board = [[WALL]*ROW_RNG]+[[WALL]+[0]*ROW_NUM+[WALL]for _ in xrange(ROW_NUM)]+[[WALL]*ROW_RNG]
        self._lastPut=None
        self.side = 1
        self.chCount=[0,0,0]
        
    def clean(self):
        self._board = [[WALL]*ROW_RNG]+[[WALL]+[0]*ROW_NUM+[WALL]for _ in xrange(ROW_NUM)]+[[WALL]*ROW_RNG]
        self._lastPut=None
    def __getitem__(self, idx): return self._board[idx]    
    def __repr__(self):
        text = '  '
        if REPR_SIMPLE:
            text += ' '.join(map(lambda x:'%X'%(x+1), xrange(ROW_NUM)))+'\n'
            for y in xrange(1,ROW_TOP):
                text += '%X'%y
                if self._lastPut and self._lastPut[1]==y:
                    for x in xrange(1,ROW_TOP):
                        text += '[' if self._lastPut[0]==x else (']'if self._lastPut[0]+1==x else' ')
                        text += '_XO'[self._board[x][y]]
                    if self._lastPut[0]==ROW_NUM: text += ']'
                else:
                    for x in xrange(1,ROW_TOP):
                        text += ' %s'%'_XO'[self._board[x][y]]
                text += '\n'
        else:
            def lp(y,x):
                if x==1:
                    if y==1:return LINE_PATTERNS[0]
                    if y==ROW_NUM:return LINE_PATTERNS[2]
                    return LINE_PATTERNS[1]
                if x==ROW_NUM:
                    if y==1:return LINE_PATTERNS[6]
                    if y==ROW_NUM:return LINE_PATTERNS[8]
                    return LINE_PATTERNS[7]
                if y==1:return LINE_PATTERNS[3]
                if y==ROW_NUM:return LINE_PATTERNS[5]
                return LINE_PATTERNS[4]
                
            
            text += ' '.join(map(lambda x:'%X'%(x+1), xrange(ROW_NUM)))+'\n'
            for y in xrange(1,ROW_TOP):
                text += '%X'%y
                if self._lastPut and self._lastPut[1]==y:
                    for x in xrange(1,ROW_TOP):
                        text += '[' if self._lastPut[0]==x else (']'if self._lastPut[0]+1==x else (CHM_PATTERNS[0]if x>1else' '))
                        text += CHM_PATTERNS[self._board[x][y]] if self._board[x][y] else lp(x,y)
                    if self._lastPut[0]==ROW_NUM: text += ']'
                else:
                    for x in xrange(1,ROW_TOP):
                        if self._board[x][y]:
                            text += '%s%s'%(' 'if x==1 else CHM_PATTERNS[0], CHM_PATTERNS[self._board[x][y]])
                        else:
                            text += (' 'if x==1else LINE_PATTERNS[9]) + lp(x,y)
                text += '\n'
        return text

    
    
    def setchm(self, s, *pos):
        if len(pos) == 1:
            if type(pos[0]) in (list, tuple) and len(pos[0])==2:
                x,y = pos[0]
            else:
                raise "bad"
        elif len(pos)==2:
            x,y= pos
        else: raise "bad ll"
    
    def put(self,x,y):
        if self._board[x][y]: return
        self._lastPut = x,y
        self._board[x][y] = self.side
        self.chCount[self.side] += 1
        self.chCount[0] += 1
        self.side = 3-self.side
    
    def forbid(self):
        kk = []
        for i in xrange(1,ROW_TOP):
            for j in xrange(1,ROW_TOP):
                if self._board[i][j]!=0:continue
                huo = 0
                for d in GomokuBoard.DIR_DELTA:
                    n = 0
                    while True:
                        n += 1
                        ch = self._board[i+d[0]*n][j+d[1]*n]
                        if ch != self.side:
                            if ch == 0 and n>2: huo+=1
                            break
                if huo > 1:
                    kk.append((i,j))
        return kk

    def isGameOver(self):
#         for x in xrange(1,ROW_TOP):
#             for y in xrange(1,ROW_TOP):
#                 if self._board[x][y]==0: continue
#                 ids=[0]*4
#                 for 
        old, cnt = 0, 0
        for d in range(4):
            for p in row(d):
                if p is None:
                    if cnt == 4:return True
                    old, cnt=0,0
                    continue
                c = self._board[p[0]][p[1]]
                if c==old:
                    if c > 0: cnt+=1
                else:
                    if cnt == 4: return True
                    old, cnt = c, 0
        return False

board=GomokuBoard()


def row(drc=0):
    if drc == 0:
        for i in xrange(1,ROW_TOP):
            for j in xrange(1,ROW_TOP):
                yield i,j
            yield None 
    elif drc == 1:
        for i in xrange(1,ROW_TOP):
            for j in xrange(1,ROW_TOP):
                yield j,i 
            yield None
    elif drc == 2:
        for i in xrange(6,27):
            for j in (xrange(1,i)if i<17 else xrange(i-15,16)):
                yield j,i-j
            yield None
    elif drc == 3:
        for i in xrange(-10,11):
            for j in (xrange(1, 16+i)if i<=0 else xrange(i+1,16)):
                yield j,j-i
            yield None
    
def isGameOver():
    old, cnt = 0, 0
    for d in range(4):
        for p in row(d):
            if p is None:
                if cnt == 4:return True
                old, cnt=0,0
                continue
            c = board[p[0]][p[1]]
            if c==old:
                if c > 0: cnt+=1
            else:
                if cnt == 4: return True
                old, cnt = c, 0
    return False

def scan():
    if isGameOver():
        global GameOver
        GameOver = True
    else:
        evaluate()
    
def evaluate():
    score = [[0]*ROW_RNG for _ in xrange(ROW_RNG)]
    
    old, cnt, lastnp =None,0,None
    for d in range(4):
        for p in row(d):
            if p is None:
                if lastnp:
                    if 0<cnt<4:
                        score[x][y]+=50.0*cnt**2
                    elif cnt==4:
                        score[lastnp[0]][lastnp[1]] = WIN_VAL if old == args.side else LOSE_VAL 
                old, cnt,lastnp=None,0,None
                continue
            
            x,y = p
            c = board[x][y]
            if c==old:
                if c > 0: cnt+=1
            else:
                if 0<cnt<5:
                    if c==0:
                        if cnt == 4:
                            score[x][y] = WIN_VAL if old == args.side else LOSE_VAL
                            if lastnp:
                                score[lastnp[0]][lastnp[1]] = WIN_VAL if old == args.side else LOSE_VAL
                        elif 0<cnt<5:
                            score[x][y]+=50.0*cnt**2
                            if lastnp:
                                score[lastnp[0]][lastnp[1]] += 50.0*cnt**2
                    elif lastnp:
                        if cnt == 4:
                            score[lastnp[0]][lastnp[1]] = WIN_VAL if old == args.side else LOSE_VAL
                        else:    
                            score[lastnp[0]][lastnp[1]] += 50.0*cnt**2
                        lastnp = None

                old,cnt=c,(1if c else 0)
            if c == 0: 
                lastnp = p
                
    maxv,maxp=0,[]
    text=''
    for y in xrange(ROW_RNG):
        for x in xrange(ROW_RNG):
            s = score[x][y]
            if s > maxv: 
                maxv = s
                maxp = [(x,y)]
            elif s==maxv:
                maxp.append((x,y))
            if 0<board[x][y]<3:
                text+= '        %s'%'_XO'[board[x][y]]
            else:
                text+=' %8.2G'%s
        text+='\n'
    print text
    
    if board.chCount[0]>0:
        board.put(*random.choice(maxp))
    else:
        board.put(8,8)
    isGameOver()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''五子棋AI''')
    parser.add_argument('board', type=str, nargs='?', help='目前棋局表示')
    parser.add_argument('--side', '-s', default='X', type=str, help='AI立场')
    parser.add_argument('--quiet', '-q', action='store_true', help='不输出棋局细节')
    parser.add_argument('--game', '-g', action='store_false', help='是否一次决策后退出')
    args = parser.parse_args()
    
    if args.board and len(args.board)<=225:
        i = -1
        for c in args.board:
            i += 1
            if c == '_': continue
            if c not in 'XO':
                print "bad expression for board, which should only be '_', 'X' or 'O'."
                exit(1)
            x,y = i%15+1, i/15+1
            board[x][y] = c = 1 if c=='X' else 2
            board.chCount[c] += 1
        if board.chCount[1] == board.chCount[2] or board.chCount[1] == board.chCount[2]+1:
            pass
        else:
            print ""
            exit(0)
            
    if args.side:
        if args.side not in ('X','O'): 
            print "bad expression for side, which should only be 'X' or 'O'."
            exit(1)
        board.side = args.side = 1 if args.side=='X' else 2
    
    if args.game:
        if (board.chCount[1]==board.chCount[2]) == (args.side==1):
            scan()
        while not GameOver:
            print board
            xxx = raw_input().split(',')
            if len(xxx)==1:
                x,y = int(xxx[0][0],16),int(xxx[0][1],16)
            elif len(xxx)==2:
                x,y = map(int, xxx)
            else:
                continue
            if 1<=x<=ROW_NUM and 1<=y<=ROW_NUM and board[x][y]==0: 
                board.put(x, y)# = 3-args.side
                scan()
        print board