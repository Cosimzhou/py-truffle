#coding: UTF-8

import math

def isPrime(n):
    def ppn():
        yield 2
        for i in xrange(3, int(math.sqrt(n))+1, 2):
            yield i
    for i in ppn():
        if n % i == 0:
            return False
    return True

def prime(n):
    arr = [2]*(n+1)
    k, i = 1, 1
    while i < n:
        k += 2
        ksr = int(math.sqrt(k))+1
        isp = True
        for c in arr[:i]:
            if k % c == 0:
                isp = False
                break
            if ksr < c:
                break
        if isp:
            arr[i] = k
            i+=1
    return arr[i-1]

if __name__ == '__main__':
    print prime(98)
        