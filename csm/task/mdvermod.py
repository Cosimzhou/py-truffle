#coding: UTF-8

def a():
    pass

if __name__ == '__main__':
    df = open("/Users/zhouzhichao/Downloads/jinan.dat", "rb")
    a = df.read(12)[6:]
    df.close()
    print "%d.%d.20%d%2d%2d"%(ord(a[0]), ord(a[1]), ord(a[2])*256+ord(a[3]), ord(a[4]), ord(a[5]))
    