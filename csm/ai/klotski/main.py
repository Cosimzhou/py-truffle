#! /usr/bin/python
# -*- coding: UTF-8 -*-

#########################################################################
# File Name: man.py
# Author: cosim
# mail: cosimzhou@hotmail.com
# Created Time: 一  5/15 15:12:23 2015
#########################################################################

class Const():
    """
           3
           ^
           |
      1 <--+--> 0
           |
           V
           2
    """

    CX, CY = 4, 5
    UX, UY = CX+1, CY+1
    WX, WY = CX+2, CY+2
    U2X, U2Y = UX<<1, UY<<1
    ALL_LEN = UX*WY+1
    NIL, WALL, CAO, VERT_SAT, HORI_SAT, PAWN = 0, 0xff, 0x01, 0x20, 0x40, 0x80
    BEGIN, END = WX, UY*UX
    DIR_DIFF = (1, -1, UX, -UX, 2, -2, U2X, -U2X)
    HORI_DOUBLE = set((VERT_SAT, CAO))
    HORI_SINGLE = set((HORI_SAT, PAWN))
    VERT_DOUBLE = set((HORI_SAT, CAO))
    VERT_SINGLE = set((VERT_SAT, PAWN))

    @staticmethod
    def type(v):
        return Const.CAO if v == Const.CAO else (v & 0xe0)

data = \
(
    (94,3, "鱼游春水", "14402202131122213042400"),
    (126,4, "数字系列之7", "34231223320302113021400"),
    (71,3, "伏羲八卦:天雷无妄", "14400223223330203042410"),
    (28,0, "比翼横空", "14433032304240001022220"),
    (50,2, "一字长蛇", "24301033031121322232410"),
    (22,0, "近在咫尺4", "44100100212203021312223"),
    (99,3, "暗渡陈仓", "24330010010203203231411"),
    (46,1, "四橫定式B", "14402001012130122232420"),
    (19,0, "伏羲八卦:风山渐", "0642333041424340102220320"),
    (60,2, "齐头并进", "44100300333021222321310"),
    (96,3, "颠倒96(陽)", "34231223310031304201401"),
    (62,2, "围而不歼", "44100021323303132331210"),
    (73,3, "伏羲八卦:火泽睽", "14400223203130223042410"),
    (38,1, "六兵", "26100300212223203331310"),
    (101,4, "高厦101", "24320023031323312131400"),
    (65,2, "三军联防", "24320300333043402221300"),
    (94,3, "歧路亡羊", "34210223300013204020320"),
    (62,2, "三羊开泰1", "24302320030013112131410"),
    (135,4, "小兵探路", "24330122003041422232400"),
    (40,1, "一橫定式C", "44130132333202103042200"),
    (53,2, "四面八方", "24302320131043410111412"),
    (126,4, "数字系列之3", "24331130030020412232410"),
    (73,3, "双将挡路", "34200023230310434121310"),
    (54,2, "背水列阵", "24300301121033310042412"),
    (103,4, "小燕出巢", "24300300333043402221310"),
    (61,2, "砝码", "24302320010203011042412"),
    (49,1, "二橫定式B", "34202233330311213220400"),
    (42,1, "一橫定式D", "44132031323203022342100"),
    (53,2, "四橫定式A", "14410002030010203042422"),
    (103,4, "瓮中之鳖", "24300300333043402221310"),
    (47,2, "雨声淅沥", "44100023213303104341210"),
    (87,3, "兵挡将阻", "24330020001323312131410"),
    (69,2, "层层设防3", "24330320001020312131410"),
    (87,3, "入地无门", "14400303102321203231410"),
    (73,3, "勿入歧途", "44100300233122214241310"),
    (80,3, "伏羲八卦:风泽中孚", "14400223204140203232410"),
    (90,3, "穷途末路", "34231233321021222030400"),
    (38,1, "一橫定式B", "44100032333303113142210"),
    (99,3, "数字系列之8", "34200300210202112042422"),
    (79,3, "伏羲八卦:天水讼", "14400223224340203230410"),
    (72,3, "六将之步步高2", "4123021120320232400"),
    (81,3, "云遮雾障", "34200300232330434121310"),
    (54,2, "牛气冲天", "24302320030043401211412"),
    (131,4, "虚与为蛇", "24330132002030422232400"),
    (40,1, "罂粟", "281003002320313233304341210"),
    (51,2, "二橫定式A", "34202123330312324220400"),
    (28,0, "伏羲八卦:火火离", "0640001031323330222042410"),
    (102,4, "列队欢送", "34200102030312232020323"),
    (109,4, "冯京马涼2", "24302330030312422130410"),
    (107,4, "山在虚无缥缈间", "34210023200300131042412"),
    (89,4, "伏羲八卦:地泽临", "34200031302122232232410"),
    (30,1, "伏羲八卦:水雷屯", "182000212223223330414032410"),
    (86,3, "伏羲八卦:天山遯", "14423000133340222030410"),
    (45,1, "一横定式A", "44100022232303112132410"),
    (40,1, "伏羲八卦:山泽损", "083013122320313041402232410"),
    (95,3, "伏羲八卦:雷山小过", "34200021223332434220410"),
    (63,2, "六将守关2", "4123021031330232401"),
    (109,4, "拳头", "34230233300010212220310"),
    (70,3, "匹马嘶风", "44103132333203021310200"),
    (133,4, "数字系列之4", "24300221132333402031420"),
    (75,3, "夹道藏兵", "14430202104340222032300"),
    (108,4, "水浒聚义", "34200203010033233042412"),
    (62,2, "六将之近在咫尺A", "224011121310020222303"),
    (81,3, "六将守关3", "4120030031320232411"),
    (58,2, "一路进军", "44100021222303132331410"),
    (62,2, "插翅难飞", "34200033330312232021310"),
    (101,4, "孤雁难飞", "24300300212033422130410"),
    (97,3, "横行之将", "14413203022032102232400"),
    (99,3, "伏羲八卦:地火明夷", "34200031302122333222410"),
    (100,4, "古堡藏龙", "34220303200100111042402"),
    (128,4, "虚与为蛇2", "34231223320302104031400"),
    (81,3, "三橫定式B", "24302333031120422131400"),
    (75,3, "六将守关1", "4122131031330232401"),
    (93,3, "欲罢不能", "44130023213010424341210"),
    (100,4, "百花盛开", "34200103020212232030423"),
    (82,3, "伏羲八卦:地天泰", "24303130131021222232410"),
    (66,2, "四路进兵2", "14400021222320323042410"),
    (32,1, "捷足先登", "44103132333003001311210"),
    (22,0, "伏羲八卦:风地观", "083223223330414243401020320"),
    (130,4, "数字系列之9", "24300331022320402131420"),
    (73,3, "马首是瞻", "14412203002240001230421"),
    (84,3, "乱石崩云", "44130011233000323042210"),
    (39,1, "四将连关", "24302122333043420212200"),
    (32,1, "伏羲八卦:雷泽归妹", "1630002122232031323042410"),
    (24,0, "伏羲八卦:火雷噬嗑", "083000102122232041403232410"),
    (102,4, "数字系列之0", "24301320030310313042410"),
    (112,4, "前后夹攻", "34210300220011213042422"),
    (35,1, "伏羲八卦:泽泽兑", "0640131021222320323042410"),
    (70,3, "指挥若定", "44100300333023213231210"),
    (39,1, "一路顺风", "44100023223303113141210"),
    (79,3, "水泄不通", "14400303104340222032310"),
    (64,2, "一夫当关", "44100102030033324340412"),
    (34,1, "兵临曹营", "44102321323003001311210"),
    (42,1, "伏羲八卦:雷风恒", "083013102120313243422230410"),
    (100,4, "三羊开泰3", "24301310030142412032310"),
    (121,4, "数字系列之5", "24301320030043412131410"),
    (27,0, "紫罗兰", "380003002122232132333043410"),
    (99,3, "列队欢送2", "34210203002122232232403"),
    (102,4, "层层设防", "24300300232033312131410"),
    (40,1, "阻塞要道", "24302120030013122231410"),
    (62,2, "伏羲八卦:雷地豫", "44102122232013124340410"),
    (108,4, "伏羲八卦:山雷颐", "34200031322322333022410"),
    (107,4, "陈兵西陲", "34230322300010203120410"),
    (54,2, "左右步兵", "44102122232003001311410"),
    (77,3, "四路进兵", "14402003001312223042410"),
    (49,2, "扰敌之策", "44122320313303102122410"),
    (138,4, "峰回路转", "34230213200102014132401"),
    (39,1, "伏羲八卦:风水涣", "1630022320414243402032310"),
    (70,3, "伏羲八卦:地山谦", "44103132333000102122210"),
    (109,4, "小汽车", "34200110310201334231421"),
    (83,3, "伏羲八卦:火山旅", "24323330001031302220410"),
    (42,1, "前挡后阻", "34221021231322333201400"),
    (41,1, "气势汹汹", "24322320414243400010220"),
    (111,4, "单身的小兵", "34220313310302203131401"),
    (90,3, "三羊开泰2", "24301310030122203231410"),
    (74,3, "左兵右将", "44120302333021203132200"),
    (81,3, "异地同心", "14411203001230003042421"),
    (36,1, "五将逼宫", "24301310333043400201311"),
    (96,3, "颠倒96    (陰)", "34230213200011114102402"),
    (104,4, "离而不坎", "24300303203133402230410"),
    (40,1, "奖杯", "24301310414243400201311"),
    (99,3, "守口如瓶2", "34201311200300333042410"),
    (68,2, "井底之蛙", "24301310030033310131411"),
    (131,4, "数字系列之1", "34231223310202104031401"),
    (32,1, "伏羲八卦:水山骞", "182000212233304142434220310"),
    (98,3, "层峦叠嶂", "24300300232043412032310"),
    (72,3, "兵分三路", "44101310333003013231210"),
    (120,4, "层层设防2", "24301310030033312131410"),
    (24,0, "伏羲八卦:天地否", "0642232233324340102030420"),
    (27,0, "伏羲八卦:泽地萃", "182000212223223332434030410"),
    (100,4, "相看两不厌", "34200103002320333042412"),
    (70,3, "伏羲八卦:风雷益", "24322320001041402032410"),
    (99,3, "以退为进", "34221312310203033030401"),
    (71,3, "屯兵东路", "44120300313223223330200"),
    (33,1, "四橫定式E", "14402001012132001232421"),
    (19,0, "伏羲八卦:山山艮", "083031323330414243401022220"),
    (63,2, "节节高升", "44100112233020313240420"),
    (76,3, "殊途同归", "44100100333022214241320"),
    (29,0, "伏羲八卦:山火贲", "083000103132333041402222410"),
    (88,3, "獨闢蹊徑", "24302132021311222232400"),
    (50,2, "星罗棋布", "24301310030033310111412"),
    (105,4, "近在咫尺3", "34210012120303112030423"),
    (106,4, "数字系列之6", "24320033002123422231400"),
    (46,2, "雪花莲", "3610030023213233304341210"),
    (63,2, "六将之步步高1", "4123021120302231400"),
    (15,0, "似远实近", "34203133322322324202100"),
    (88,3, "大渡桥横铁索寒", "24301333132030412131410"),
    (62,2, "互不相让", "14400100232332013042411"),
    (81,3, "守口如瓶", "34200301202320333042410"),
    (83,3, "横马当关", "34200301303330434022210"),
    (38,1, "四橫定式D", "14400101121312002030422"),
    (19,0, "单兵种的没落", "54000102131232030331402"),
    (65,2, "三橫定式A", "24302333031122422130400"),
    (42,1, "伏羲八卦:水火既济", "083013102122333041422032410"),
    (122,4, "冯京马涼", "24302333021311222130400"),
    (50,2, "一字长蛇2", "24321232030313202030400"),
    (28,0, "蝴蝶花", "4600030023212221323043410"),
    (56,2, "四面楚歌", "44100300332102002341311"),
    (85,3, "伏羲八卦:泽山咸", "24323330131021222030410"),
    (81,3, "横刀立马", "44100300232132304341210"),
    (44,1, "六将之近在咫尺B", "4120030112102102303"),
    (100,4, "伏羲八卦:地风升", "34200031302122434222310"),
    (121,4, "数字系列之2", "24331020030043412131410"),
    (96,3, "伏羲八卦:山水蒙", "34200031322322434022310"),
    (125,4, "琼瑶敲碎", "24331033001133402231410"),
    (72,3, "胡马窥江", "14430023204340003231411"),
    (77,3, "逆时风车", "34230022332333413120400"),
    (72,3, "将拥曹营", "44101122231033324340410"),
    (63,2, "插翅难飞2", "24301310030033310042411"),
    (106,4, "花车", "24301310414243412032310"),
    (95,3, "困於赤绂", "24300302002041403232411"),
    (44,1, "四橫定式C", "14401111213140022232420"),
    (98,3, "近在咫尺", "34210203000012232020323"),
    (97,3, "伏羲八卦:雷水解", "34200021222322434230410"),
    (24,0, "伏羲八卦:水泽节", "083000102122232041403232410"),
    (26,0, "伏羲八卦:水水坎", "182000212223204142434032310"),
    (87,3, "顺时风车", "34230220321323334021400"),
    (70,3, "桃花园中", "44101311222003003331410"),
    (105,4, "近在咫尺2", "34200102120303132020323"),
    (90,3, "行百里者半九十", "34220313330011103000412")
)


class Board(object):
    def __init__(self):
        self.clear()

    def __repr__(self):
        #return self.printOutMemory()
        return self.printGraphic()
        return self.printPosIndex()

    @staticmethod
    def encode_pos(x, y):
        return (y+1)*Const.UX + (x+1)
    @staticmethod
    def decode_pos(pos):
        return  (pos%Const.UX)-1, (pos//Const.UX)-1

    def clear(self):
        self.__board = [0]*Const.ALL_LEN
        self.__pieces = {} #piece positions, CC is in the first pit
        self.__pits = {i for i in xrange(Const.ALL_LEN)}
        self.set_wall()

    def set_wall(self):
        top = Const.UX*Const.UY
        for i in xrange(Const.UX):
            self.__board[i] = Const.WALL
            self.__board[i+top] = Const.WALL
            self.__pits.remove(i)
            self.__pits.remove(i+top)
        for i in xrange(1, Const.UY):
            self.__board[i*Const.UX] = Const.WALL
            self.__pits.remove(i*Const.UX)
        self.__board[-1] = Const.WALL
        self.__pits.remove(len(self.__board)-1)

    def get_string_from_board(self):
        dic = {}
        for k, v in self.__pieces.items():
            k = Const.type(k)
            if k not in dic:
                dic[k] = ''
            dic[k] += "%d%d"%Board.decode_pos(v)
        text = "%d%d%d"%(len(dic.get(Const.VERT_SAT))/2,len(dic.get(Const.PAWN))/2,len(dic.get(Const.HORI_SAT))/2)
        text+= "".join((dic.get(Const.VERT_SAT, ""), dic.get(Const.PAWN, ""), dic.get(Const.HORI_SAT, ""), dic.get(Const.CAO, "")))
        return text

    def set_board_by_string(self, string):
        if len(string) < 3:
            return
        self.clear()
        occupy = set()
        plrs = [int(string[0]), int(string[1]), int(string[2])]
        idxs = Const.VERT_SAT, Const.PAWN, Const.HORI_SAT, 0
        i, man, man_id = 3, 0, Const.VERT_SAT
        while i < len(string):
            while man < 3 and plrs[man] == 0:
                man += 1
                man_id = idxs[man]

            pos = Board.encode_pos(int(string[i]), int(string[i+1]))
            i += 2
            if man == 3:
                self.__board[pos] = \
                self.__board[pos+1] = \
                self.__board[pos+Const.UX] = \
                self.__board[pos+Const.WX] = Const.CAO
                self.__pieces[Const.CAO] = pos
                occupy.add(pos)
                occupy.add(pos+1)
                occupy.add(pos+Const.UX)
                occupy.add(pos+Const.WX)
                break

            plrs[man] -= 1
            self.__pieces[man_id] = pos
            self.__board[pos] = man_id
            occupy.add(pos)
            if man == 0:
                self.__board[pos+Const.UX] = man_id
                occupy.add(pos+Const.UX)
            elif man == 1:
                pass
            else:
                self.__board[pos+1] = man_id
                occupy.add(pos+1)
            man_id += 1
        self.__pits -= occupy
        assert len(self.__pits) == 2

    def printGraphic(self):
        text = "┌────────────┐\n"
        line1 = "│"
        line2 = "│"
        x, end = Const.BEGIN, Const.END
        while x <= end:
            if self.__board[x] == Const.WALL:
                if x % Const.UX:
                    raise Exception("unexpected wall appears in inner area(%d,%d)."%(y,x))
                line1 += "│"
                line2 += "│"
                text += '%s\n%s\n'%(line1, line2)
                line1 = "│"
                line2 = "│"
            elif self.__board[x] == Const.NIL:
                line1 += "   "
                line2 += "   "
            elif self.__board[x] == Const.CAO:
                if self.__board[x-Const.UX] != self.__board[x]:
                    line1 += "┌────┐"
                    line2 += "│ \/ │"
                else:
                    line1 += "│ /\ │"
                    line2 += "└────┘"
                x += 1
            elif Const.PAWN <= self.__board[x] < Const.WALL:
                line1 += "┌─┐"
                line2 += "└─┘"
            elif Const.HORI_SAT <= self.__board[x] < Const.PAWN:
                line1 += "┌────┐"
                line2 += "└────┘"
                x += 1
            elif Const.VERT_SAT <= self.__board[x] < Const.HORI_SAT:
                if self.__board[x-Const.UX] != self.__board[x]:
                    line1 += "┌─┐"
                    line2 += "│ │"
                else:
                    line1 += "│ │"
                    line2 += "└─┘"
            else:
                raise Exception("unknown block(%d)."%x)
            x += 1

        text += "└──┐      ┌──┘"
        return text
# """
# ┌─┬┐
# │
# ├┼┤
# └┴┘
# """

    def printMemory(self):
        text = ""
        for i, c in enumerate(self.__board):
            text += "%02x"%c
            if i % Const.UX < Const.CX:
                continue
            text += '\n'
        text += " "*(Const.CX*2)
        return text

    def printPosIndex(self):
        text = ""
        for i, _ in enumerate(self.__board):
            text += "%02d "%i
            if i % Const.UX < Const.CX:
                continue
            text += '\n'
        return text
    def printMD(self):
        dic = {}
        for k, v in self.__pieces.items():
            k = Const.type(k)
            if k not in dic: dic[k] = []
            dic[k].append(v)
        for k in dic:
            dic[k].sort()
        ks = sorted(dic.keys())
        return ''.join(map(lambda x:chr(59+x), reduce(lambda x, y:x+y, map(lambda x:dic[x], ks))))

    def info(self):
        texts1 = self.printGraphic().split("\n")
        texts2 = self.printMemory().split("\n")
        texts3 = self.printPosIndex().split("\n")
        for i, l in enumerate(texts2):
            texts1[i] += "| "+ l
        for i, l in enumerate(texts3):
            texts1[i] += "| " + l
        texts1[Const.WY+1] += '-'*(Const.WX*5)
        texts1[Const.WY+2] += str(self.__pits) + ":" + self.printMD() +" = "+ self.get_string_from_board()
        texts1[Const.WY+3] += str(self.__pieces)

        return "\n".join(texts1)


    def isChm(self, x, y):
        return Const.CAO <= self.__board[y][x] < Const.WALL
    def _isChm(self, x):
        return Const.CAO <= self.__board[x] < Const.WALL

    def opEnum(self):
        """
               3
               ^
               |
          1 <--+--> 0
               |
               V
               2
        """
        for x in self.__pits:
            assert self.__board[x] == Const.NIL

            # whether left man can move right
            left_man = self.__board[x-1]
            left_man_type = Const.type(left_man)
            left_pos = self.__pieces.get(left_man)
            if left_pos:
                if left_man_type in Const.HORI_SINGLE:
                    yield [left_pos], [x], 0, left_man
                elif self.__board[x+Const.UX] == Const.NIL:
                    if left_pos == x-2 and left_man_type == Const.CAO:
                        yield [left_pos, left_pos+Const.UX], [x,x+Const.UX], 0, left_man
                    if left_pos == x-1 and left_man_type == Const.VERT_SAT:
                        yield [left_pos, left_pos+Const.UX], [x,x+Const.UX], 0, left_man
#            elif left_man == Const.NIL:
#                left_man = self.__board[x-2]
#                left_man_type = Const.type(left_man)
#                if left_man_type in Const.HORI_SINGLE:
#                    left_pos = self.__pieces.get(left_man)
#                    if left_pos:
#                        yield left_pos, x, 4, left_man

            # whether right man can move left
            right_man = self.__board[x+1]
            right_man_type = Const.type(right_man)
            right_pos = self.__pieces.get(right_man)
            if right_pos:
                if right_man_type in Const.HORI_SINGLE:
                    if right_man_type == Const.PAWN:
                        yield [right_pos], [x], 1, right_man
                    elif right_man_type == Const.HORI_SAT:
                        yield [right_pos+1], [x], 1, right_man
                elif self.__board[x+Const.UX] == Const.NIL:
                    if right_pos == x+1 and right_man_type == Const.VERT_SAT:
                        yield [right_pos, right_pos+Const.UX], [x,x+Const.UX], 1, right_man
                    elif right_pos == x+1 and right_man_type == Const.CAO:
                        yield [right_pos+1, right_pos+Const.WX], [x,x+Const.UX], 1, right_man
#            elif right_man == Const.NIL:
#                right_man = self.__board[x+2]
#                right_man_type = Const.type(right_man)
#                if right_man_type in Const.HORI_SINGLE:
#                    right_pos = self.__pieces.get(right_man)
#                    if right_pos:
#                        yield right_pos, x, 5, right_man


            # whether upper man can move down
            upper_man = self.__board[x-Const.UX]
            upper_man_type = Const.type(upper_man)
            upper_pos = self.__pieces.get(upper_man)
            if upper_pos:
                if upper_man_type in Const.VERT_SINGLE:
                    yield [upper_pos], [x], 2, upper_man
                elif self.__board[x+1] == Const.NIL:
                    if upper_pos == x-Const.U2X and upper_man_type == Const.CAO:
                        yield [upper_pos, upper_pos+1], [x,x+1], 2, upper_man
                    elif upper_pos == x-Const.UX and upper_man_type == Const.HORI_SAT:
                        yield [upper_pos, upper_pos+1], [x,x+1], 2, upper_man
#            elif upper_man == Const.NIL:
#                upper_man = self.__board[x-Const.U2X]
#                upper_man_type = Const.type(upper_man)
#                if upper_man_type in Const.VERT_SINGLE:
#                    upper_pos = self.__pieces.get(upper_man)
#                    if upper_pos:
#                        yield upper_pos, x, 6, upper_man

            # whether lower man can move up
            lower_man = self.__board[x+Const.UX]
            lower_man_type = Const.type(lower_man)
            lower_pos = self.__pieces.get(lower_man)
            if lower_pos:
                if lower_man_type in Const.VERT_SINGLE:
                    if lower_man_type == Const.PAWN:
                        yield [lower_pos], [x], 3, lower_man
                    elif lower_man_type == Const.VERT_SAT:
                        yield [lower_pos+Const.UX], [x], 3, lower_man
                elif self.__board[x+1] == Const.NIL:
                    if lower_pos == x+Const.UX and lower_man_type == Const.CAO:
                        yield [lower_pos+Const.UX, lower_pos+Const.WX], [x,x+1], 3, lower_man
                    elif lower_pos == x+Const.UX and lower_man_type == Const.HORI_SAT:
                        yield [lower_pos, lower_pos+1], [x, x+1], 3, lower_man
#            elif lower_man == Const.NIL:
#                lower_man = self.__board[x+Const.U2X]
#                lower_man_type = Const.type(lower_man)
#                if lower_man_type in Const.VERT_SINGLE:
#                    lower_pos = self.__pieces.get(lower_man)
#                    if lower_pos:
#                        yield lower_pos, x, 7, lower_man

    def do(self, op):
        for p in op.origin:
            self.__board[p] = Const.NIL
            self.__pits.add(p)
        for p in op.dest:
            self.__board[p] = op.man_id
            self.__pits.remove(p)
        self.__pieces[op.man_id] += Const.DIR_DIFF[op.direct]

    def undo(self, op):
        for p in op.origin:
            self.__board[p] = op.man_id
            self.__pits.remove(p)
        for p in op.dest:
            self.__board[p] = Const.NIL
            self.__pits.add(p)
        self.__pieces[op.man_id] -= Const.DIR_DIFF[op.direct]

class Operation(object):
    __slots__ = "origin dest direct man_id".split()
    def __init__(self, orig_pos, dest_pos, direct, man_id):
        self.origin = orig_pos
        self.dest = dest_pos
        self.direct = direct
        self.man_id = man_id
    def __repr__(self):
        return "(%s->%s, %d, %d)"%(str(self.origin), str(self.dest), self.direct, self.man_id)

class Tree(object):
    __slots__ = "parent value children depth history".split()
    def __init__(self, val=None):
        self.parent = None
        self.children = []
        self.value = val
        self.depth = 0
        self.history = set()
    def __repr__(self):
        return "%d.%s %s:%s"%(self.depth, self.value, ",".join(map(lambda x:str(x.value), self.children)), ",".join(self.history))
    def adopt(self, child):
        self.children.append(child)
        child.depth = self.depth + 1
        child.parent = self
        child.history.update(self.history)

class Game(object):
    def __init__(self, opening = None):
        self.base = Board()
        self.tree = []
        self.visited = set()
        self.root_op = Tree()
        self.limit = 150
        if opening is not None:
            self.limit = data[opening][0]*2
            self.base.set_board_by_string(data[opening][3])
            self.visited.add(self.base.printMD())

    def gen_operations(self):
        ops = []
        for i in self.base.opEnum():
            ops.append(Operation(*i))
        return ops

    def search(self):
        try:
            print self.travel(self.root_op)
        except KeyboardInterrupt:
            print
            print self.base.info()

    def travel(self, rop):
        ops = self.gen_operations()
        ret = False
        print self.base.info()
        for op in ops:
            self.base.do(op)
            md = self.base.printMD()
            if md[0] == "Q":
                print md
                ret = True
            #elif md not in rop.history and rop.depth < self.limit:
            elif md not in self.visited and rop.depth < self.limit:
                r = Tree(op)
                rop.adopt(r)
                self.visited.add(md)
                #r.history.add(md)
            self.base.undo(op)
            if ret: return ret
        print rop

        for r in rop.children:
            self.base.do(r.value)
            ret = self.travel(r)
            self.base.undo(r.value)
            if ret: return ret
        rop.children = []
        return False

    def show(self):
        print self.base

    def do_opera(self):
        pass

if __name__ == '__main__':
    g = Game(4)
#    g.base.set_board_by_string("14433030414130100022220")
#    print g.base.info()
#    print g.gen_operations()
    g.search()
#    print g.base.info()
#    ops = []
#    for i in g.base.opEnum():
#        ops.append(Operation(*i))
#
#    g.base.do(ops[0])
#    print g.base.info()
    #g.show()
