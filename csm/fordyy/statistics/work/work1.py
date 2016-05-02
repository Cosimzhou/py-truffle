#coding=GBK
from csm.fordyy.statistics.funcs import *

class Entry(object):
    def __init__(self):
        self.sex = 0
        self.id = 0
        self.age = 0
        self.T3 = 0
        self.T4 = 0
        self.cu = 0

data=[]
add=lambda x,y:x+y
def load():
    no = 0
    with open('E:/work/2014-2015.csv','r') as f:
        for l in f.readlines():
            if no:
                aa = l.split(',')
                person = Entry()
                person.id = int(aa[0])
                person.sex = 2-int(aa[1])
                person.age = int(aa[2])
                person.T3 = float(aa[3])
                person.T4 = float(aa[4])
                person.cu = float(aa[5])
                data.append(person)
            no+=1


if __name__ == '__main__':
    load()
    men=filter(lambda x:x.sex,data)
    women=filter(lambda x:x.sex==0,data)
    
    print "总人数：%d (%d,%d),男女比例：1:%f"%(len(data),len(men),len(women),float(len(women))/len(men))
    print "平均年龄：%.2f:%.2f (%.2f:%.2f,%.2f:%.2f)"%(avg(off('age',data)),sigma(off('age',data)), avg(off('age',men)),sigma(off('age',men)), avg(off('age',women)),sigma(off('age',women)))
    print "年龄范围：%d~%d=%d (%d~%d=%d,%d~%d=%d)"%(min(off('age',data)),max(off('age',data)),max(off('age',data))-min(off('age',data)),
                                             min(off('age',men)),max(off('age',men)),max(off('age',men))-min(off('age',men)),
                                             min(off('age',women)),max(off('age',women)),max(off('age',women))-min(off('age',women)))

    print mid(off('age',data)), mid(off('age', men)),mid(off('age', women))
    
    