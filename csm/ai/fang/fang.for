总价=单价*面积
首付限=总价*30%
首付=首付限 if 首付<首付限 else 首付
成交价格=总价
中介费=成交价格*2.7%
印花税=成交价格*0.05%
单价=总价/面积

交易费=3*面积
贷款总额=总价-首付
契税=总价*(1% if 面积<90 else 1.5%)
初次支出=首付+契税+印花税+登记费+核档费+交易费+家装预算+中介费

上次网签价=原值
网签价下限=贷款总额/(80%)
网签价=网签价下限
货款上限=网签价*80%



月利率=利率 / 12
还款月数=12*贷款年限
还款期数=还款月数


每期还款额=借款本金*月利率*(1+1.0/((1+月利率)**还款月数-1))

营业税=0if 满五年 else 成交价*5.5%