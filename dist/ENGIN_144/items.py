# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class SlidebdItem(Item):
    Name = Field()  # 游戏名
    Platforms = Field()  # 平台
    Developed_By = Field()  # 公司/开发者
    Engine = Field()  # 引擎
    Official_Page = Field()  #官网
    Release_Date = Field()  #上线日期
    Genre = Field()  # 类型
    Theme = Field()  # 主题
    Players = Field()  # 玩家
    Google_Play = Field()  # 谷歌下载地址
    Country = Field()
    Email = Field()
    Phone = Field()
    Address = Field()

class GooglePlayItem(Item):
    name = Field()
    dev_name = Field()
    url = Field()
    email = Field()