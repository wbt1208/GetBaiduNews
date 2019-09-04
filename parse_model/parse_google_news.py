#这一模块实现的功能依旧是xpath解析
#理想中应该包括一下数据源：
# 第一步：  时间、媒体、标题、正面还是负面、连接
# 第二步：  筛选出负面舆论，判断是否为原发数据源（排除转载等情况），找到作者
# 第三步：  数据分析，首先那些媒体经常黑江淮，那些作者经常发黑江淮的文章，那些负面报道在社会上产生了重大影响（阅读量，导致江淮重大损失）
# 第四步：  针对部分重大舆情，做媒体、作者的深入调查
from lxml import etree
from data_cleaning_model.data_cleaning_model import *

    # 首先是第一步，时间，媒体，标题，链接
    # 确定新闻列表的位置：newlist_xpath = "//div[@class="g"]"
    # 确定标题的位置：titlename_xpath = "./div/div/h3/a"    a下面的em标签和a标签
    # 超链接位置：    urls_xpath = "./div/div/h3/a/@href"
    # 媒体位置：     media_xpath = "./div/div/div[1]/span[1]"
    # 时间位置：     time_xpath = "./div/div/div[1]/span[3]"
def parse_google_news(html):
    parse_list = []
    html_tree = etree.HTML(html)
    for new in html_tree.xpath("//div[@class='g']"):
        try:
            titlenames = new.xpath("./div/div/h3/a")
            titlename = del_douhao(titlenames[0].xpath('string(.)'))
        except:
            titlename= ""
        try:
            url = new.xpath("./div/div/h3/a/@href")[0]
        except:
            url = ""
        try:
            media = new.xpath("./div/div/div[1]/span[1]/text()")[0]
        except:
            media = ""
        try:
            time = new.xpath("./div/div/div[1]/span[3]/text()")[0]
        except:
            time = ""
        try:
            abstracts = new.xpath("./div/div/div[@class='st']")
            abstract = abstracts[0].xpath('string(.)')
        except:
            abstract = ""
        parse_list.append([titlename,media,time,abstract,url])
    return parse_list