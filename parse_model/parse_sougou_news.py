from data_cleaning_model.data_cleaning_model import *
from lxml import etree
from request_model.request_model import request_by_selenium_chrome

"""
url_xpath = "//div[@class="results"]/div[@class="vrwrap"]//h3/a/@href"
title_xpath = "//div[@class="results"]/div[@class="vrwrap"]//h3/a"
media_time = "//div[@class="results"]/div[@class="vrwrap"]//div[@class="news-detail"]//p[1]"
abstract = "//div[@class="results"]/div[@class="vrwrap"]//div[@class="news-detail"]//p[2]/span"
"""
def parse_sougou_news(html):
    html_tree = etree.HTML(html)
    parse_list = []
    for news in html_tree.xpath("//div[@class='results']/div[@class='vrwrap']")[:-1]:
        try:
            url =news.xpath(".//h3/a/@href")[0]
        except:
            url = ""
        try:
            title = del_block(del_enter(news.xpath(".//h3/a")[0].xpath("string(.)")))
        except:
            title = ""
        try:
            media_time = news.xpath(".//div[@class='news-detail']//p[1]/text()")[0]
            media = media_time.split()[0]

            time = media_time.split()[1]
            if "小时" in time or "分钟" in time:
                time = "2019/07/31"
        except:
            media = ""
            time = ""
        try:
            abstract = news.xpath(".//div[@class='news-detail']//p[2]/span")[0].xpath("string(.)")
        except:
            abstract = ""
        parse_list.append([title,media,time,abstract,url])
    return parse_list