#coding: UTF-8

matrix={}
backmatrix={}
vector={}
# filePath='/Users/zhouzhichao/Documents/电子书/安娜·卡列尼娜.txt'
filePath='/Users/zhouzhichao/Documents/电子书/平凡的世界.txt'
# filePath='/Users/zhouzhichao/Documents/电子书/钟表馆幽灵.txt'

def add(x,y): 
    return x+y

def asCch(ch, cch):
#     return (ch-0xB0)*0x60 + cch-0xA0
    return ch*0x100 + cch

def mkCch(word):
#     sword = "".join([chr(0xB0+word/0x60), chr(0xA0+word%0x60)])    
    sword = "".join([chr(word/0x100), chr(word%0x100)])    
    return sword.decode('GBK').encode('UTF-8')

def isBigWordHead(word):
    entry = matrix.get(word)
    return reduce(add, map(lambda x:x[1], entry.items()))>100 if entry else False
        
def weightLink(prew, word):
    entry = matrix.get(prew)
    if entry:
        v = entry.get(word)
        return v if v else 0
    return 0

def addLink(root, word, mat):
    entry = mat.get(root)
    if entry is None: 
        mat[root] = entry = {}
    cntnum = entry.get(word)
    entry[word] = 1 if (cntnum is None) else (cntnum + 1)
    
def extract_data():
    with open(filePath, 'r') as f:
        for l in f.readlines():
            pword = 0
            for word in popWord(l):
                if word:
                    addLink(word, 0, matrix)
                if pword and word:
                    addLink(pword, word, matrix)
                    addLink(word, pword, backmatrix)
                pword = word

def add_longWord(word, dwn):
    num = dwn.get(word)
    dwn[word] = 1 if (num is None) else (num+1)
    
def extract_2word():
    with open(filePath, 'r') as f:
        for l in f.readlines():
            for word in popWord(l):
                
                pass

def extract_word():
    def addCurrentWord(curword, freqWord):
#         if len(curword) < 5: return
        add_longWord(''.join(map(mkCch, curword)), freqWord)
        
    freqWord = {}
    with open(filePath, 'r') as f:
        for l in f.readlines():
            preword, curword = 0, []
            for word in popWord(l):
                if word == 0:
                    preword = 0
                    if len(curword)>2:
                        addCurrentWord(curword, freqWord)
                    curword = []
                else:
                    wl = weightLink(preword, word)
                    if wl > 20:
                        if len(curword) >= 2:
                            curword.append(word)
                        elif len(curword) == 1:
                            if preword == curword[0]:
                                curword.append(word)
                            elif isBigWordHead(word):
                                curword = [word]
                        else:
                            if isBigWordHead(word): curword = [word]
                    else:
                        if len(curword)>2:
                            addCurrentWord(curword, freqWord)
                        elif len(curword)==0 and isBigWordHead(word): 
                            curword = [word]
                preword = word          

    arr=sorted(freqWord.items(), key=lambda x:x[1], reverse=True)
    for i in range(100):
        print arr[i][0],arr[i][1]



# 弹出一个UTF-8文本字符串中的每一个汉字的GBK内码
def popWord(iline):
    def readChar(line, i):
        return ord(line[i]), i+1
    line = iline.decode('UTF-8').encode('GBK')
    linelen, i, preword = len(line)-1, 0, 1
    while i < linelen:
        ch,i = readChar(line, i)
        if ch == 0xA1:
            cch,i = readChar(line, i)
            if cch == 0xA4:
                preword = asCch(ch, cch)
                yield preword
                continue
        elif 0x81 <= ch <= 0xA0 or 0xAA <= ch <= 0xFE:
            cch,i = readChar(line, i)
            if cch >= 0x40:
                preword = asCch(ch, cch)
                yield preword
                continue
        elif 0x80 <= ch:
            cch,i = readChar(line, i)
        if preword != 0: yield 0
        preword = 0
                
def char_count():
    for k,v in matrix.items():
        cnt = 0.0
        for _,vv in v.items():
            cnt += vv
        rate, mrate = 0, 0
        for _,vv in v.items():
            rate = vv/cnt
            if mrate < rate: mrate=rate
        
        vector[mkCch(k)] = mrate
        
def find_threshold():
    arr = []
    for _,v in matrix.items():
        for _,vv in v.items():
            arr.append(vv)
    arr.sort(reverse=True)
    return arr[len(arr)/10]

def get_word_by_threshold(threshold): 
    arr = []
    for k,v in matrix.items():
        for vk,vv in v.items():
            if vv > threshold:
                arr.append([''.join([mkCch(k),mkCch(vk)]), vv])
    arr.sort(key=lambda x:x[1], reverse=True)
    print len(arr)
    for i in arr[1:100]:
        print i[0], i[1]
        
#     print arr[0][0]

def output_matrix(mat):
    for k,v in mat.items():
        print "%s: {"%mkCch(k),
        for vk,vv in v.items():
            print "%s:%d, "%(mkCch(vk),vv),
        print "}"
        
if __name__ == '__main__':
    extract_data()
#     threshold=find_threshold()
#     get_word_by_threshold(threshold)
     
#     extract_word()
    
#     char_count()
#     print vector
    
    output_matrix(backmatrix)

#     for w in popWord('　　“也许他到走廊里去了；他刚才还在那里踱来踱去。那就是他，”门房说，指着一个蓄着鬈曲胡须、体格强壮、宽肩的男子，他没有摘下羊皮帽子，正在轻快而迅速地跑上石级磨损了的台阶。一个挟着公事包的瘦削官吏站住了，不以为然地望了望这位正跑上台阶的人的脚，又探问似地瞥了奥布隆斯基一眼。'):
#         print mkCch(w)
# 
#     print mkCch(1285)

#     a='况·'.decode('UTF-8').encode('GBK')
#     print asCch(ord(a[0]), ord(a[1]))