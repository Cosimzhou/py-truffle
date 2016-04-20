#coding: UTF-8

CX, CY = 4, 5
NIL, WALL, CAO, VERT_SAT, HORI_SAT, PAWN = 0, 255, 1, 32, 64, 128 

class board(object):
    def __init__(self):
        self.board = [[0]*(CX+2) for _ in xrange(CY+2)]
        for i in xrange(len(self.board)):
            self.board[i][0] = self.board[i][-1] = WALL
        for i in xrange(len(self.board[0])):
            self.board[0][i] = self.board[-1][i] = WALL
            
    def set_board_by_string(self, string):
        if len(string) < 3: return
        plrs = [int(string[0]), int(string[1]), int(string[2])]
        idxs = VERT_SAT, PAWN, HORI_SAT, 0
        i, j, k = 3, 0, VERT_SAT
        while i < len(string):
            while j < 3 and plrs[j] == 0:
                j += 1
                k = idxs[j]
            
            x, y = int(string[i])+1, int(string[i+1])+1     
            i += 2           
            if j == 3:
                self.board[y][x] = CAO
                self.board[y+1][x] = CAO
                self.board[y][x+1] = CAO
                self.board[y+1][x+1] = CAO
                break
            
            plrs[j] -= 1
            if j == 0:
                self.board[y][x] = k
                self.board[y+1][x] = k
            elif j == 1:
                self.board[y][x] = k
            else:
                self.board[y][x] = k
                self.board[y][x+1] = k
            k += 1
            

    def __repr__(self):
        text = ""#"┌────────┐\n"
        for y in xrange(len(self.board)):
            for x in xrange(len(self.board[y])):
                if self.board[y][x] == CAO:
                    text += "X"
                elif self.board[y][x] == WALL:
                    text += "*"
                elif PAWN <= self.board[y][x] < WALL:
                    text += 'o'
                elif HORI_SAT <= self.board[y][x] < PAWN:
                    text += '='
                elif VERT_SAT <= self.board[y][x] < HORI_SAT:
                    text += 'H'
                else:
                    text += ' '
            text += '\n'
            
#         text += "└─┐    ┌─┘"
        return text
    
    def isChm(self, x, y):
        return CAO<= self.board[y][x] < WALL
    
    def opEnum(self):
        for y in xrange(1, CY):
            for x in xrange(1, CX):
                if self.board[y][x] == NIL:
#                     if self.isChm(y, x-1) and ((self.board[y-1][x-1] == self.board[y][x-1] and self.board[y-1][x-1]==NIL) or (self.board[y+1][x-1] == self.board[y][x-1] and self.board[y+1][x-1]==NIL)):
#                         yield (0)
#                         pass
#                     if self.isChm(y, x+1):
                        pass
        pass
            
class op(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    b = board()
    b.set_board_by_string("182000212223204142434032310")
    print b
    pass