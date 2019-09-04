#初始化参数
#要抓取的企业的中文名和英文名的关键字参数
FIRM_NAME = {
    "FIRM1":"FIRM1_ENGLISH",
}
#最大线程数
MAX_THREADS = 3

#最大相似哈希距离值
MAX_SIMHASH_V = 20


import os
from concurrent.futures import ThreadPoolExecutor
from NewsSpyder import newsSpyder
from cleaner import Cleanner
cwd = os.getcwd()
cwd_son_list = os.listdir(cwd)
#检查是否存在文件夹data，没有则创建
flag = False
for son in cwd_son_list:
    if "data" == son:
        flag = True
if not flag:
    os.makedirs(cwd + "/data")
#检查clean_data文件夹是否存在，无则创建
flag = False
for son in cwd_son_list:
    if "clean_data" == son:
        flag = True
if not flag:
    os.makedirs(cwd + "/clean_data")
#生成线程参数
def spyder_run():
    with ThreadPoolExecutor(MAX_THREADS) as executor:
        for k,v in FIRM_NAME.items():
            #定义文件保存位置
            FILE_PATH = "data/%s新闻.xlsx"%k
            #定义日志文件保存位置
            LOG_PATH = "data/%slog.log"%k
            fp = open(LOG_PATH,"a+",encoding="utf-8")
            #定义关键词删选
            FILTER = [k,v.capitalize(),v.lower(),v.upper()]
            #定义关键词
            KWS = ["%s"%k,"%s and 安全"%k,"%s and 数据"%k,"%s and 股东"%k,"%s and 法人"%k,
               "%s and 董事"%k,"%s and 高管"%k,"%s and 总裁"%k,"%s and 违法"%k,"%s and 后门"%k,
               "%s Director Change"%v, "%s Network Security"%v, "%s Illegal"%v, "%s shareholders"%v]
            #获取代理
            # proxies = get_proxies()
            newsspyder = newsSpyder(FILE_PATH,fp,FILTER,KWS)
            executor.submit(newsspyder.run)
#清洗data中excel的数据
def cleaner_run():
    path_li = os.listdir(os.getcwd()+"/data")
    excel_li = []
    for file_name in path_li:
        if file_name.split(".")[-1] == "xlsx":
            excel_li.append(file_name)
    print("待清洗文件：",excel_li)

    #生成线程参数
    with ThreadPoolExecutor(MAX_THREADS) as executor:
        for excel in excel_li:
            file_name = "data/"+excel
            file_save = "clean_data/"+excel
            FILTER = []
            for k,v in FIRM_NAME.items():
                if k in excel:
                    FILTER = [k, v.capitalize(), v.lower(), v.upper()]
                    break
            clean = Cleanner(file_name,file_save,MAX_SIMHASH_V,FILTER)
            executor.submit(clean.run)
if __name__ == '__main__':
    spyder_run()
    print("全部爬取结束，开始清洗和分类")
    cleaner_run()
