import thulac
from data_cleaning_model.data_cleaning_model import cleaner
import hashlib
th = thulac.thulac(T2S=True)
class simHash():
    def __init__(self,context,th1 = None):
        if th1:
            self.th1 = th1
        else:
            global th
            self.th1 = th
        self.context = context
        self.simhash = self.get_simhash()
    def __str__(self):
        print(self.simhash)
    def get_weight(self,s):
        """n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
    m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
    v/动词 a/形容词 d/副词 h/前接成分 k/后接成分
    i/习语 j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
    e/叹词 o/拟声词 g/语素 w/标点 x/其它 """
        d1 = {}
        d1_trans = {"n":5, "np":4,"ns":4,"ni":4,"nz":4,"m":3,"q":3,"mq":3,"t":3,"f":3,"s":3,"v":2,"a":1,"d":1}
        for factor in s.split():
            li = factor.split("_")
            key = li[0]
            value = li[1]
            if value in d1_trans:
                value_trans = d1_trans[value]
                d1[key] = value_trans
        return d1
    def get_simhash(self):
        s = cleaner(self.context)
        text = self.th1.cut(s, text=True)
        value1 = [0 for i in range(128)]
        value_add = []
        for k,v in self.get_weight(text).items():
            md5 = hashlib.md5()
            md5.update(k.encode("utf-8"))
            value = bin(int(md5.hexdigest(), 16))
            value = value+"0"*(130-len(value))
            value = list(value[2:])
            for i in range(128):
                if value[i] == "0":
                    value[i] = -1 * v
                else:
                    value[i] = int(value[i]) * v
            for j in range(128):
                value_add.append(value1[j] + value[j])
            value1 = value_add
            value_add = []
        for a in range(128):
            if value1[a]>0:
                value1[a] = 1
            else:
                value1[a] = 0
        s = ""
        for s1 in value1:
            s += str(s1)
        s = "0b"+s
        # print(s)
        return s
    def hamming_distance(self,simhash):
        sim1 = simhash.simhash[2:]
        sim2 = self.simhash[2:]
        distance = 0
        for i in range(128):
            if sim1[i] != sim2[i]:
                distance += 1
        return distance












# value1 = [1,2,3,4]
# value2 = []
# if len(value2)==0:
#     value2 = [0 for i in range(128)]
# value_add = []
# for i in range(len(value1)):
#     value_add.append(value1[i] + value2[i])
# value1 = value_add
# print(value_add)

"""test simhash"""
# simhash1 = simHash("腾讯将与长安汽车联合展示全新语音交互的微信车载版本")
# simhash2 = simHash("腾讯将和长安汽车联合展示全新语音交互的微信车载版本")
# print(simhash1.hamming_distance(simhash2))

# import simhash
# a = simhash.Simhash("美方召开华为美企供应商会议讨论华为解禁问题")
# a.distance("美方召开华为美企供应商会议讨论华为")