import pandas as pd
from del_duplication_model.del_duplication_model import simHash
from save_model.save_model import SaveAsXslx
class Cleanner():
    def __init__(self,file_name,file_save,MAX_SIMHASH_V,filter):
        print("清洗器初始化")
        #定义读取文件名
        self.file_name = file_name
        #定义保存文件名
        self.file_save = file_save
        #定义允许重复的最大simhash值
        self.MAX_SIMHASH_V = MAX_SIMHASH_V
        #定义保存对象的表头
        self.saver = SaveAsXslx(["标题","媒体","发表时间","摘要","url链接","类别"])
        #定义类别筛选字段
        self.FILTER = filter
    def run(self):
        #读取excel
        df1 = pd.read_excel(self.file_name)
        #标号+标题列表，其中标号是标题唯一标识列表
        print("除去空值")
        df1.dropna(axis=0,how="any",inplace=True,subset=["标题"])
        print("筛选")
        l1 = []
        for i in range(df1.shape[0]):
            #取出标题，并生成simhash对象
            s1 = simHash(str(df1.iloc[i,:]["标题"]))
            #生成标号与s1对应的字典
            d1 = {i:s1}
            #遍历l1取差
            if not l1:
                l1.append(d1)
                print("lo....")
                continue
            flag = True
            for j in l1:
                if s1.hamming_distance([v for k,v in j.items()][0]) < self.MAX_SIMHASH_V:
                    flag = False
                    break
            if flag:
                l1.append(d1)
        print("保存")
        for d in l1:
            biahao = [k for k,v in d.items()][0]
            title = df1.iloc[biahao,:]["标题"]
            grey = ""
            flag = False
            for kw in self.FILTER:
                if kw in title:
                    flag = True
            if flag:
                for key in ["任职","离职","出任","跳槽","升职","担任"]:
                    if key in title:
                        grey = "高管变动"
                for key in ["方案","巡展","发布","推出"]:
                    if key in title:
                        grey = "产品情况"
                for key in ["携手","中标","合作","签署","份额","启动","牌照"]:
                    if key in title:
                        grey = "企业经营"
                for key in ["丑闻","套现","起诉","诉讼","处罚","欺骗","指控","质疑","勒索","被罚","致歉","道歉"]:
                    if key in title:
                        grey = "企业负面"
            media = df1.iloc[biahao,:]["媒体"]
            time =  df1.iloc[biahao,:]["发表时间"]
            absjract = df1.iloc[biahao,:]["摘要"]
            url = df1.iloc[biahao,:]["url链接"]
            self.saver.write([title,media,time,absjract,url,grey])
        self.saver.save(self.file_save)
