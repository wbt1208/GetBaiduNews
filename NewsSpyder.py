#coding:utf-8
from request_model.request_model import request_by_selenium_chrome,request_by_requests
from parse_model.parse_google_news import parse_google_news
from save_model.save_model import SaveAsCsv,SaveAsXslx
from parse_model.parse_baidu_news import parse_baidu_news
from parse_model.parse_sougou_news import parse_sougou_news
from proxies_model.get_proxies import get_proxies
class newsSpyder():
    def __init__(self,FILE_PATH,fp,FILTER,KWS):
        print("线程初始化参数")
        print("文件保存位置:",FILE_PATH)
        print("关键字:", KWS)
        #配置初始化参数
        #文件保存位置
        self.FILE_PATH = FILE_PATH
        #定义保存对象的表头
        self.saver = SaveAsXslx(["标题","媒体","发表时间","摘要","url链接"])
        #定义日志文件
        self.fp = fp
        #定义关键词删选
        self.FILTER = FILTER
        #定义关键词
        self.KWS = KWS
        #获取代理
        # self.proxies = get_proxies()
    def run(self):
        print("开始爬取")
        for kw in self.KWS:
            # "达索系统 and 网络安全", "达索系统 and 股东变更", "达索系统 and 法人变更", "达索系统 and 董事变更", "达索系统 and 违法","达索系统 and 合法"
            # "IDassault Director Change","Dassault Network Security","Dassault Illegal","Dassault shareholders"
            # kw = "Microsoft Director Change"
            # 微星，msi，MSI,Msi
            for page in range(0,300,10):
                url = "https://www.google.com/search?q=%s&newwindow=1&rlz=1C1CHWL_zh-CNUS820US820&tbm=nws&ei=LGgdXaTpLLKUr7wPscinyA8&start=%d&sa=N&ved=0ahUKEwikr9K2n5rjAhUyyosBHTHkCfkQ8tMDCFU&biw=1920&bih=888&dpr=1"%(kw,page)
                try:
                    html =  request_by_selenium_chrome(url=url,headless=True)
                    print("当前关键词：" + kw + "\t当前数据来源：谷歌新闻" + "\t当前请求页码：" + str(page) + "\t请求成功，开始解析和写入")
                except Exception as e:
                    print("当前关键词：" + kw + "\t当前数据来源：谷歌新闻" + "\t当前请求页码：" + str(page) + "\t请求失败，写入log文件")
                    self.fp.write("请求失败："+url+"-"+"失败原因："+str(e.args)+"\n")
                    self.fp.flush()
                    continue
                for contexts in parse_google_news(html):
                    # print(contexts)
                    for filt in self.FILTER:
                        if filt in contexts[0] or filt in contexts[3]:
                            self.saver.write(contexts)
                            break
            for page in range(0,200,10):
                url = "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%s&tngroupname=organic_news&pn=%d"%(kw,page)
                try:
                    html =  request_by_selenium_chrome(url=url,headless=True)
                    print("当前关键词：" + kw + "\t当前数据来源：百度新闻" + "\t当前请求页码：" + str(page) + "\t请求成功，开始解析和写入")
                except Exception as e:
                    print("当前关键词：" + kw + "\t当前数据来源：谷歌新闻" + "\t当前请求页码：" + str(page) + "\t请求失败，写入log文件")
                    self.fp.write("请求失败："+ url +"\t"+"失败原因："+str(e.args)+"\n")
                    self.fp.flush()
                    continue
                for contexts in parse_baidu_news(html):
                    # print(contexts)
                    for filt in self.FILTER:
                        if filt in contexts[0] or filt in contexts[3]:
                            self.saver.write(contexts)
                            break
            for page in range(1,21):
                url = "https://news.sogou.com/news?mode=1&manual=&query=%s&time=0&sut=3026&sst0=1564550347888&sort=0&page=%d&w=01029901&dr=1"%(kw,page)
                try:
                    html =  request_by_selenium_chrome(url=url,headless=True)
                    print("当前关键词：" + kw + "\t当前数据来源：搜狗新闻" + "\t当前请求页码：" + str(page) + "\t请求成功，开始解析和写入")
                except Exception as e:
                    print("当前关键词：" + kw + "\t当前数据来源：谷歌新闻" + "\t当前请求页码：" + str(page) + "\t请求失败，写入log文件")
                    self.fp.write("请求失败："+ url +"\t"+"失败原因："+str(e.args)+"\n")
                    self.fp.flush()
                    continue
                for contexts in parse_sougou_news(html):
                    # print(contexts)
                    for filt in self.FILTER:
                        if filt in contexts[0] or filt in contexts[3]:
                            self.saver.write(contexts)
                            break
        self.saver.save(self.FILE_PATH)
        self.fp.close()