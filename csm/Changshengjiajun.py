# coding: utf-8

pro, bro = 0.5, 0.5 
record = [0]*10+[pro**10]

def func(num):
    if num < 0:
        return 0
    if num < len(record):
        return record[num]
    func_1 = func(num-1)
    cfunc = 1-func(num-11)
    result = func_1+cfunc*bro*record[10]
        
    record.append(result)
    return result

def cmp4nh(x,y):
    xs=x.split(';')
    ys=y.split(';')
    ax, ay=int(xs[0]), int(ys[0])
    return ax - ay
def merge():    
    fnh = open('/Users/zhouzhichao/Documents/年号')
    lnh = fnh.readlines()[1:]
    fnh.close() 
    fnb = open('/Users/zhouzhichao/Documents/年表')
    lnb = fnb.readlines()[1:]
    fnb.close()
    
    split = lambda x:x.split()
    lnh = map(split, sorted(lnh, cmp=cmp4nh))
    lnb = map(split, sorted(lnb, cmp=cmp4nh))
    
    h = 0
    for i in lnb:
        
#         if i[0]<=lnh[h][0]<= i[0]+i
        print i
#     print lnb

def count(func, iters):
    sumcount = 0
    for i in iters:
        if func(i):sumcount+=1
    return sumcount

if __name__ == '__main__':
#     for i in xrange(10,10001,10):
#         print i,func(i)

#     headers = None
#     content = ''
#     with open('/Users/zhouzhichao/zg') as f:
#         for i in f.readlines():
#             if headers is None:
#                 headers = i.split('\t')
#                 continue
#             seccnt = count(lambda x:x=='\t',content)
#             if seccnt < len(headers):
#                 content += i
#                 continue
#             elif seccnt == len(headers):
#                 print content.replace('\n', '')
#                 content = i
#             else:
#                 print 'Bad!', i
#                 exit(1)
    pass


################################
k=["\200\200\200\200\200\200\200\200\200\200\200\200\001\200\200\200\200",
    "\200\200\200\200\200\200\200\200\200\200\200\002\003\200\200\200\200",
    "\200\200\200\200\200\200\200\200\200\200\004\005\006\200\200\200\200",
    "\200\200\200\200\200\200\200\200\200\007\010\011\012\200\200\200\200",
    "\200\200\200\200\013\014\015\016\017\020\021\022\023\024\025\026\027",
    "\200\200\200\200\030\031\032\033\034\035\036\037\040\041\042\043\200",
    "\200\200\200\200\044\045\046\047\050\051\052\053\054\055\056\200\200",
    "\200\200\200\200\057\060\061\062\063\064\065\066\067\070\200\200\200",
    "\200\200\200\200\071\072\073\074\075\076\077\100\101\200\200\200\200",
    "\200\200\200\102\103\104\105\106\107\110\111\112\113\200\200\200\200",
    "\200\200\114\115\116\117\120\121\122\123\124\125\126\200\200\200\200",
    "\200\127\130\131\132\133\134\135\136\137\140\141\142\200\200\200\200",
    "\143\144\145\146\147\150\151\152\153\154\155\156\157\200\200\200\200",
    "\200\200\200\200\160\161\162\163\200\200\200\200\200\200\200\200\200",
    "\200\200\200\200\164\165\166\200\200\200\200\200\200\200\200\200\200",
    "\200\200\200\200\167\170\200\200\200\200\200\200\200\200\200\200\200",
    "\200\200\200\200\171\200\200\200\200\200\200\200\200\200\200\200\200"]
xs,ys=[0]*122,[0]*122
i = 0
for l in k:
    j = 0
    for c in l:
        cc = ord(c)
        if cc < 128:
            xs[cc] = i
            ys[cc] = j
        j+=1
    i+=1
    
print ''.join(map(lambda x:('\\0'if x<8else '\\')+oct(x), xs))
print ''.join(map(lambda x:('\\0'if x<8else '\\')+oct(x), ys))