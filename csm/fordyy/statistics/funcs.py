#coding:GBK
from math import sqrt

__all__ = ['sigma','avg','off','mid']

def sigma(iters):
    avg = float(sum(iters))/len(iters)
    return sqrt(sum(map(lambda x:(x-avg)**2, iters))/len(iters))

def avg(iters):
    return float(sum(iters))/len(iters)

def off(var,iters):
    return map(lambda x:x.__dict__.get(var), iters)

def mid(iters):
    array = sorted(iters)
    lenarr= len(array)
    if lenarr == 0:
        return None
    return array[lenarr/2] if lenarr%2 else (array[lenarr/2]+array[lenarr/2-1])/2.0



