#coding: UTF-8

#coding: UTF-8

from math import pi as TK_PI
from math import sqrt, asin, acos, sin, cos, tan, log, exp, fabs

TK_MERCATOR_MAX=24
TK_RADIUS_EARTH=6371004 # meters
TK_RADIAN_PER_DEGREE=TK_PI / 180 # use to transfer unit system from degree to radian
TK_TOP_RANGE=3686400.0

g_casm = None
class tk_casm(object):
    def __init__(self, w_lng=0, w_lat=0):
        self.t1 = 0
        self.t2 = 0

        self.rr = 0.3
        self.x1 = w_lng
        self.y1 = w_lat
        self.x2 = w_lng
        self.y2 = w_lat
        self.f = 3
        
    def random_yj(self):
    #     int t
    #     int casm_a 
    #     int casm_c 
    #     casm_a = 314159269
    #     casm_c = 453806245
    #     self.rr = casm_a * self.rr + casm_c 
    #     t = self.rr / 2 
    #     self.rr = self.rr - t * 2
    #     self.rr = self.rr / 2 
        return self.rr        


def _tk_gps_yj_sin2(x):
    ff = False
    if x < 0:
        x = -x
        ff = True
     
    cc = int(x / 6.28318530717959)
    tt = x - cc * 6.28318530717959
    if tt > TK_PI:
        tt -= TK_PI
        ff = not ff
 
    ss = s2 = x = tt
    tt = tt * tt
    s2 = s2 * tt
    ss = ss - s2 * 0.166666666666667
    s2 = s2 * tt
    ss = ss + s2 * 8.33333333333333E-03
    s2 = s2 * tt
    ss = ss - s2 * 1.98412698412698E-04
    s2 = s2 * tt
    ss = ss + s2 * 2.75573192239859E-06
    s2 = s2 * tt
    ss = ss - s2 * 2.50521083854417E-08
    return -ss if ff else ss
 
def _tk_gps_yj5(x, y):
    tt = 300 + 1 * x + 2 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(sqrt(x * x))
    tt = tt + (20 * _tk_gps_yj_sin2(6*TK_PI * x) + 20 * _tk_gps_yj_sin2(2*TK_PI * x)) * 0.6667
    tt = tt + (20 * _tk_gps_yj_sin2(TK_PI * x) + 40 * _tk_gps_yj_sin2(TK_PI/3 * x)) * 0.6667
    tt = tt + (150 * _tk_gps_yj_sin2(TK_PI/12 * x) + 300 * _tk_gps_yj_sin2(TK_PI/30 * x)) * 0.6667
    return tt
 
def _tk_gps_yjy5(x, y):
    tt = -100 +  2 * x + 3 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(sqrt(x*x))
    tt = tt + (20 * _tk_gps_yj_sin2(6*TK_PI * x) + 20 * _tk_gps_yj_sin2(2*TK_PI * x)) * 0.6667
    tt = tt + (20 * _tk_gps_yj_sin2(TK_PI * y)+ 40 * _tk_gps_yj_sin2(TK_PI/3 * y)) * 0.6667
    tt = tt + (160 * _tk_gps_yj_sin2(TK_PI/12 * y) + 320 * _tk_gps_yj_sin2(TK_PI/30 * y)) * 0.6667
    return tt
 
def _tk_gps_jy5(x, xx):
    a = 6378245
    e = 0.00669342
    n = sqrt(1 - e * _tk_gps_yj_sin2(x * TK_RADIAN_PER_DEGREE) * _tk_gps_yj_sin2(x * TK_RADIAN_PER_DEGREE))
    n = (xx * 180) / (a / n * cos(x * TK_RADIAN_PER_DEGREE) * TK_PI) 
    return n
 
def _tk_gps_jyj5(x , yy):
    a = 6378245
    e = 0.00669342
    mm = 1 - e * _tk_gps_yj_sin2(x * TK_RADIAN_PER_DEGREE) * _tk_gps_yj_sin2(x * TK_RADIAN_PER_DEGREE)
    m = (a * (1 - e)) / (mm * sqrt(mm))
    return (yy * 180) / (m * TK_PI)
 
def _tk_gps_wgtochina_lb(wg_lng, wg_lat):
    x_l, y_l = wg_lng, wg_lat
    x_l /= 3686400.0# 3600<<10
    y_l /= 3686400.0
     
    global g_casm
    if g_casm is None:
        g_casm = tk_casm(wg_lng, wg_lat)
        return (0x00000000, wg_lng, wg_lat)
     
    g_casm.t2 = 0
    t1_t2 = (g_casm.t2 - g_casm.t1) / 1000.0
    if t1_t2 <= 0:
        g_casm.t1 = g_casm.t2 
        g_casm.f += 1
        g_casm.x1 = g_casm.x2
        g_casm.f += 1
        g_casm.y1 = g_casm.y2
        g_casm.f += 1
    else:
        if t1_t2 > 120:
            if g_casm.f == 3:
                g_casm.f = 0
                g_casm.x2 = wg_lng
                g_casm.y2 = wg_lat
                x1_x2 = g_casm.x2 - g_casm.x1
                y1_y2 = g_casm.y2 - g_casm.y1
                casm_v = sqrt(x1_x2 * x1_x2 + y1_y2 * y1_y2 ) / t1_t2
                if (casm_v > 3185):
                    return (0xFFFF95FF,0,0)
                 
            g_casm.t1 = g_casm.t2
            g_casm.f += 1
            g_casm.x1 = g_casm.x2
            g_casm.f += 1
            g_casm.y1 = g_casm.y2
            g_casm.f += 1
         
    x_add = _tk_gps_yj5(x_l - 105, y_l - 35)
    y_add = _tk_gps_yjy5(x_l - 105, y_l - 35)
 
    x_add = x_add + _tk_gps_yj_sin2(0) + g_casm.random_yj()
    y_add = y_add +  _tk_gps_yj_sin2(0) + g_casm.random_yj()
     
    return (0x00000000,
            ((x_l + _tk_gps_jy5(y_l, x_add)) * 3686400),
            ((y_l + _tk_gps_jyj5(y_l, y_add)) * 3686400))

 

 
def tk_gps_latlon_transform(lon, lat):
    global g_casm
    wg_lng = int(lon * TK_TOP_RANGE)
    wg_lat = int(lat * TK_TOP_RANGE)
    
    if g_casm is None:
        _tk_gps_wgtochina_lb(wg_lng, wg_lat)

    ret, china_lng, china_lat = _tk_gps_wgtochina_lb(wg_lng, wg_lat)
    if 0 == ret:
        return (china_lng / TK_TOP_RANGE,
                china_lat / TK_TOP_RANGE)
    else:
        return 0.0,0.0
 
def _tk_gps_wgtochina_lb_simple(wg_lng, wg_lat):
    x_l = wg_lng / TK_TOP_RANGE
    y_l = wg_lat / TK_TOP_RANGE

    x_add = _tk_gps_yj5(x_l - 105, y_l - 35) + g_casm.random_yj()
    y_add = _tk_gps_yjy5(x_l - 105, y_l - 35) + g_casm.random_yj()
    
    return (0,
            ((x_l + _tk_gps_jy5(y_l, x_add)) * TK_TOP_RANGE),
            ((y_l + _tk_gps_jyj5(y_l, y_add)) * TK_TOP_RANGE))
     
def tk_gps_latlon_transform_simple(lon, lat):    
    wg_lng = int(lon*TK_TOP_RANGE)
    wg_lat = int(lat*TK_TOP_RANGE)

    ret, china_lng, china_lat = _tk_gps_wgtochina_lb_simple(wg_lng, wg_lat)
    return (china_lng/TK_TOP_RANGE, china_lat/TK_TOP_RANGE) if ret==0 else (0,0)
    
def tk_gps_latlon_transform_reverse(lon, lat):
    if lon < 72.004 or lon > 137.8347 or lat < 0.8293 or lat > 55.8271:
        return lon,lat
    a = 6378245.0
    ee = 0.00669342162296594323
    x = lon - 105.0
    y = lat - 35.0
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(fabs(x))
    dLat += (20.0 * sin(6.0 * x * TK_PI) + 20.0 * sin(2.0 * x * TK_PI)) * 2.0 / 3.0
    dLat += (20.0 * sin(y * TK_PI) + 40.0 * sin(y / 3.0 * TK_PI)) * 2.0 / 3.0
    dLat += (160.0 * sin(y / 12.0 * TK_PI) + 320 * sin(y * TK_PI / 30.0)) * 2.0 / 3.0
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(fabs(x))
    dLon += (20.0 * sin(6.0 * x * TK_PI) + 20.0 * sin(2.0 * x * TK_PI)) * 2.0 / 3.0
    dLon += (20.0 * sin(x * TK_PI) + 40.0 * sin(x / 3.0 * TK_PI)) * 2.0 / 3.0
    dLon += (150.0 * sin(x / 12.0 * TK_PI) + 300.0 * sin(x / 30.0 * TK_PI)) * 2.0 / 3.0
    radLat = lat / 180.0 * TK_PI
    magic = sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * TK_PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * TK_PI)
    out_lat = lat - dLat
    out_lon = lon - dLon
    return out_lon, out_lat


def tk_lonlat_to_mercxy(lon, lat, lv):
    if lv <= 0 or lv > 23 or lon < -180.0 or  \
        lon > 180.0 or lat < -85 or lat > 85:
        return 0,0
    
    multiplyFactor = 1L << (lv + 8)
    merc_x = int(round(lon + 180.0) / 360.0 * multiplyFactor)
    siny = sin(lat * TK_PI / 180.0)
    merc_y = int(round((0.5 - log((1 + siny) / (1 - siny)) / 4.0 / TK_PI)) * multiplyFactor)
    return merc_x, merc_y


#define TK_MERCATOR_MAX ((1LL << 31) - 1)
def tk_mercxy_to_lonlat(merc_x, merc_y, lv):
    if lv <= 0 or lv > 23 or merc_x < 0 or merc_x > TK_MERCATOR_MAX \
        or merc_y < 0 or merc_y > TK_MERCATOR_MAX:
        return 0.0, 0.0
    
    multiplyFactor = 1 << (lv + 8)
    return  (merc_x * 360.0 / multiplyFactor - 180.0,
        asin(1.0 - 2.0 / (1 + exp(2.0 * TK_PI * (1 - merc_y / multiplyFactor * 2)))) / TK_PI * 180.0)

def tk_distance_between_lonlats(lon1, lat1, lon2, lat2):
    """
    地球曲面距离
    """
    rlon1, rlat1, rlon2, rlat2 = float(lon1) * TK_RADIAN_PER_DEGREE, float(lat1) * TK_RADIAN_PER_DEGREE, float(lon2) * TK_RADIAN_PER_DEGREE, float(lat2) *TK_RADIAN_PER_DEGREE
    vcos = cos(rlat1) * cos(rlat2) * cos(rlon1 - rlon2) + sin(rlat1) * sin(rlat2)
    vcos = 1.0 if vcos > 1.0 else (vcos if vcos > -1.0 else -1.0)
    return acos(vcos) * TK_RADIUS_EARTH

class GaussProjection(object):
    def __init__(self):
        self.a = 0
        self.f = 0
        self.ZoneWide = 6
    def setXian80(self):
        self.a = 6378140.0
        self.f = 1.0 / 298.257
    def setWGS84(self):
        self.a = 6378137.0
        self.f = 1.0 / 298.257223563
    def setBj54(self):
        self.a = 6378245.0
        self.f = 1.0 / 298.3
    
    # WGS => XIAN
    def PrjCalculate(self, lon, lat):
        #ZoneWide = 6; //6度带宽 
        ZoneWide = 3
        ProjNo = int(lon / ZoneWide)
        #ProjNo = ProjNo >= 38 ? ProjNo - 1 : ProjNo;
        #longitude0 = ProjNo * ZoneWide + ZoneWide / 2;
        longitude0 = ProjNo * ZoneWide #js修改
        #longitude0 = ProjNo * ZoneWide + ZoneWide;//js修改
        longitude0, latitude0 = longitude0 * TK_RADIAN_PER_DEGREE, 0
        longitude1, latitude1 = lon * TK_RADIAN_PER_DEGREE, lat * TK_RADIAN_PER_DEGREE
        #经度转换为弧度, 纬度转换为弧度
    
        e2 = 2 * self.f - self.f * self.f
        ee = e2 * (1.0 - e2)
        NN = self.a / sqrt(1.0 - e2 * sin(latitude1) * sin(latitude1))
        T = tan(latitude1) * tan(latitude1)
        C = ee * cos(latitude1) * cos(latitude1)
        A = (longitude1 - longitude0) * cos(latitude1)
        M = self.a * ((1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256) * latitude1 - (3 * e2 / 8 + 3 * e2 * e2 / 32 + 45 * e2 * e2 * e2 / 1024) * sin(2 * latitude1) + (15 * e2 * e2 / 256 + 45 * e2 * e2 * e2 / 1024) * sin(4 * latitude1) - (35 * e2 * e2 * e2 / 3072) * sin(6 * latitude1))
        xval = NN * (A + (1 - T + C) * A * A * A / 6 + (5 - 18 * T + T * T + 72 * C - 58 * ee) * A * A * A * A * A / 120)
        yval = M + NN * tan(latitude1) * (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * A * A * A * A / 24 + (61 - 58 * T + T * T + 600 * C - 330 * ee) * A * A * A * A * A * A / 720)
        X0 = 1000000L * (ProjNo + 1) + 500000L
        Y0 = 0
        return (round((xval + X0) * 100) / 100.0,round((yval + Y0) * 100) / 100.0)
        

    def PrjInvCalculate(self, X, Y):
        ProjNo = int(X / 1000000L)#查找带号
        #longitude0 = (ProjNo - 1) * ZoneWide + ZoneWide / 2;
        longitude0 = ProjNo * self.ZoneWide#js修改
        longitude0 = longitude0 * TK_RADIAN_PER_DEGREE#中央经线
        X0 = ProjNo * 1000000L + 500000L
        Y0 = 0
        xval = X - X0
        yval = Y - Y0#带内大地坐标
        e2 = 2 * self.f - self.f * self.f
        e1 = (1.0 - sqrt(1 - e2)) / (1.0 + sqrt(1 - e2))
        ee = e2 / (1 - e2)
        M = yval
        u = M / (self.a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))
        fai = u + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * sin(2 * u) + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * sin(4 * u)+ (151 * e1 * e1 * e1 / 96) * sin(6 * u) + (1097 * e1 * e1 * e1 * e1 / 512) * sin(8 * u)
        C = ee * cos(fai) * cos(fai)
        T = tan(fai) * tan(fai)
        NN = self.a / sqrt(1.0 - e2 * sin(fai) * sin(fai))
        R = self.a * (1 - e2) / sqrt((1 - e2 * sin(fai) * sin(fai)) * (1 - e2 * sin(fai) * sin(fai)) * (1 - e2 * sin(fai) * sin(fai)))
        D = xval / NN
        #计算经度(Longitude) 纬度(Latitude)
        longitude1 = longitude0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / cos(fai)
        latitude1 = fai - (NN * tan(fai) / R) * (D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)
        return (longitude1 / TK_RADIAN_PER_DEGREE, latitude1 / TK_RADIAN_PER_DEGREE)



if __name__ == '__main__':
    lon = 105.87542;
    lat = 21.38413;
    
    out_lon, out_lat = tk_gps_latlon_transform(lon,lat)
    s_lon, s_lat = tk_gps_latlon_transform_simple(lon,lat)
    rlon, rlat = tk_gps_latlon_transform_reverse(out_lon, out_lat)
    
    print lon,lat, out_lon, out_lat, rlon, rlat, tk_distance_between_lonlats(lon,lat, rlon, rlat)
    print out_lon, out_lat
    print s_lon, s_lat

    gp = GaussProjection()
    gp.setXian80()
    lonlat=gp.PrjCalculate(lon, lat)
    gp.setWGS84()
    
    print gp.PrjInvCalculate(*lonlat)
    print lonlat
    
    print tk_gps_latlon_transform_reverse(119.97437,31.8132)
    

