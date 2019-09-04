
from data_cleaning_model.data_cleaning_model import *
from lxml import etree
"""
title_xpath = "//div[@class="result"]/h3/a"  还需再取一次string
url_xpath = "//div[@class="result"]/h3/a/@href"
abstract_xpath = "//div[@class="result"]/div"
time_xpath = "//div[@class="result"]/div//p"
meiti_xpath = "//div[@class="result"]/div//p"
"""


def parse_baidu_news(html):
    html_tree = etree.HTML(html)
    parse_list = []
    for news in html_tree.xpath("//div[@class='result']"):
        try:
            title = del_block(del_enter(news.xpath("./h3/a")[0].xpath("string(.)")))
        except:
            title = ""
        try:
            url = news.xpath("./h3/a/@href")[0]
        except:
            url = ""
        try:
            meiti_time = del_block(del_enter(news.xpath("./div//p")[0].xpath("string(.)")))
            meiti_time_list = meiti_time.replace("              "," ").split()
            meiti = meiti_time_list[0]
            time = meiti_time_list[1]
        except:
            meiti = ""
            time = ""
        try:
            abstract = ""
            for abstracts in del_block(del_enter(news.xpath("./div")[0].xpath("string(.)"))).replace("              "," ").replace("    "," ").split()[3:-1]:
                abstract+=abstracts
        except:
            abstract = ""
        parse_list.append([title,meiti,time,abstract,url])
    return parse_list
    # print(meiti_time_list)