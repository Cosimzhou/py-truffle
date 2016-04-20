#coding: UTF-8

import wave, struct, math

class wavSounder(object):
    def __init__(self):
        self.seconds = 1
        self.sample = 44100
        self.amplitude = 128
        self.file = '/Users/zhouzhichao/test.wav'
        self.wavwrt = None
    
        self.scheme = None
    
    def assembleSoundSample(self):
        samples = []
        length = self.sample * self.seconds
        amp = self.amplitude / 7.0
        maxamp = reduce(lambda x,y:x+y, map(lambda x:x[1], self.scheme), 0)
        
        for i in range(length):
            t = float(i) / self.sample  # t表示当下滴时间
            sample = 0
            for e in self.scheme:
                sample += e[1]*math.sin(t * e[0] * 2 * math.pi)  # 就根据sin wave的方程得到当下的amplitude啦，这里生成频率为256的音高哟，可以随便改。
            sample *= amp/maxamp
            # print i, t, sample     # show some generated values. comment out for speed.
            packed_sample = struct.pack('h', sample)  # 转换成16进制的string
            print packed_sample, sample
            samples.append(packed_sample) 
        return ''.join(samples)
            
if '__main__' == __name__:
    print wave.__dict__.get('Wave_reader')
    wavwrt = wave.open('/Users/zhouzhichao/test.wav', 'wb')
    wavwrt.setparams((1, 1, 44100, 0, 'NONE', 'not compressed'))

    ws = wavSounder()
    ws.scheme = ((440,1),(554.3652619537443,1),(659.2551138257401,1))
    data = ws.assembleSoundSample()

    wavwrt.writeframes(data)
    wavwrt.close()
    pass