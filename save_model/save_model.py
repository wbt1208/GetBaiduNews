#应该同时支持json格式、csv格式、xslx格式
import json
import pandas
class SaveAsJson():
    def __init__(self,file_path,methord="w+"):
        """
        :param file_path: 存入路径名称
        :param methord: 写入方式
        """
        self.fp = open(file_path,methord,encoding="utf-8")
    def write(self,s):
        self.fp.write(json.dumps(s))
        self.fp.flush()
    def __del__(self):
        self.fp.close()
class SaveAsCsv():
    def __init__(self,file_path,methord="w+"):
        """
        :param file_path: 存入路径名称
        :param methord: 写入方式
        """
        self.fp = open(file_path,methord,encoding="utf-8")
    def write(self,s):
        self.fp.write(s)
        self.fp.flush()
    def __del__(self):
        self.fp.close()


class SaveAsXslx():
    def __init__(self,args):
        self.df = pandas.DataFrame(index=range(1,10001),columns=args)
        self.count = 0
    def write(self,value):
        for i in range(len(value)):
            self.df.iloc[self.count,i] = str(value[i])
        self.count +=1

    def save(self,file_path):
        print("共%d条数据，正在保存"%self.count)
        self.df.to_excel(file_path)
        print("保存成功，程序结束")
    def __str__(self):
        return str(self.df.head(2))


class SaveAsTxt():
    def __init__(self,file_path,methord="w+"):
        """
        :param file_path: 存入路径名称
        :param methord: 写入方式
        """
        self.fp = open(file_path,methord,encoding="utf-8")
    def write(self,s):
        self.fp.write(s)
        self.fp.flush()
    def __del__(self):
        self.fp.close()