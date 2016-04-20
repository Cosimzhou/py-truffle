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
    arr = [2]
    k = 1
    while n > len(arr):
        k += 2
        while not isPrime(k):
            k += 2
        arr.append(k)
    print arr
    return k

if __name__ == '__main__':
    print prime(98)
        