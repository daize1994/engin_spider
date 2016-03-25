# -*- coding: utf-8 -*-
import os
from scrapy import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from ENGIN_144.items import SlidebdItem, GooglePlayItem, LagouItem, zhuhsou360Item

'''
   slidedb爬虫需求
'''
# scrapy crawl slidedb_spider -o details.csv -t csv
class slidedbSpider(CrawlSpider):
    page = 1
    name = "slidedb_spider"
    allowed_domains = ["slidedb.com"]
    start_urls = [
        # "http://www.slidedb.com/games?sort=dateup-desc",
        # "http://www.slidedb.com/members/cobolfoo"
                  ]

    rules = (
        # Rule(LinkExtractor(allow=('/page/.*')), follow=True, callback='parse_list'),
        # Rule(SgmlLinkExtractor(allow=('/games/[^page].*')), follow=True, callback='parse_detail'),
     )

    # login and get cookies
    def start_requests(self):
        return [FormRequest(
            "https://secure.slidedb.com/members/login",
            formdata={'username': 'TestBird_Luke',
                      'password': 'Gamest0p',
                      'referer': '',
                      'members': 'Sign In'},
            meta={'cookiejar': "https://secure.slidedb.com/members/login"},
            callback=self.begin
        )]

    # start the first link
    def begin(self, response):
        yield Request("http://www.slidedb.com/games?sort=dateup-desc", meta={'cookiejar': response.meta['cookiejar']})

# first spider,to get gamesname
    def parse(self, response):
        self.page += 1
        sel = Selector(response)
        sites = sel.css('.content > h4 > a')
        # next_url = sel.css('.next::attr(href)').extract()[0]
        items = []
        for site in sites:
            item = SlidebdItem()
            # get details url in this page of the number site
            detail_urls = site.css('::attr(href)').extract()[0]
            # get Name from GamesList by css selector
            item['Name'] = site.css('::text').extract()
            items.append(item)
            # return all next Request to callbackmethod ,And Transfer some parameters which get to callback method
            yield Request('http://www.slidedb.com' + detail_urls, meta={'item': item, 'cookiejar': response.meta['cookiejar']}, callback=self.parse_detail)
        # yield Request('http://www.slidedb.com'+next_url)
        if self.page < 6:
            yield Request('http://www.slidedb.com/games/page/%d?sort=dateup-desc' % self.page, meta={'cookiejar': response.meta['cookiejar']})

    # get games' details
    def parse_detail(self, response):
        sel = Selector(response)
        items = []
        # get all path's common body list
        sites = sel.xpath('//*[@class="column span-300 last sidecolumn"]')
        for site in sites:
            # recieve parameters from last methonds
            item = response.meta['item']
            item['Platforms'] = site.xpath('./div[1]/div[2]/div/div[2]/div[2]/span/a/text()').extract()
            item['Developed_By'] = site.xpath('./div[1]/div[2]/div/div[2]/div[3]/span//a/text()').extract()
            item['Engine'] = site.xpath('./div[1]/div[2]/div/div[2]/div[4]/span//a/text()').extract()
            item['Official_Page'] = site.xpath('./div[1]/div[2]/div/div[2]/div[6]/span//a/@href').extract()
            item['Release_Date'] = site.xpath('./div[1]/div[2]/div/div[2]/div[7]/span/text()').extract()
            item['Google_Play'] = site.css('.googlebtn::attr(href)').extract()
            # 如下3个信息，有的是在页面第二排，有的是第3排，所以不能用xpath定位
            item['Genre'] = site.css('.body.bodysimple')[1].css('.table.tablemenu').css('.row.clear')[0].css('.summary::text').extract()
            item['Theme'] = site.css('.body.bodysimple')[1].css('.table.tablemenu').css('.row.clear')[1].css('.summary::text').extract()
            item['Players'] = site.css('.body.bodysimple')[1].css('.table.tablemenu').css('.row.clear')[2].css('.summary::text').extract()
            items.append(item)
            yield Request('http://www.slidedb.com' +site.xpath('./div[1]/div[2]/div/div[2]/div[3]/span//a/@href').extract()[0], meta={'item': item, 'cookiejar': response.meta['cookiejar']}, callback=self.parse_campany)
        # return items

    # get games'campany message
    def parse_campany(self, response):
        sel = Selector(response)
        items = []
        site = sel.xpath('//*[@class="column span-300 last sidecolumn"]')
        item = response.meta['item']
		# country和Email可能有或者没有，这两个情况的路径稍有差别，所以下面就两个相加，保证一定可以根据路径可以取到值。
        item['Country'] = site.xpath('//div[h5="Country"]/span/text()').extract()+site.xpath('.//h4/text()').extract()
        item['Email'] = site.xpath('.//div[h5="Email"]/span/text()').extract()+site.xpath('.//div[h5="Email"]/span/a/text()').extract()
        item['Phone'] = site.xpath('.//div[h5="Phone"]/span/text()').extract()
        item['Address'] = site.xpath('.//div[h5="Address"]/span/text()').extract()
        items.append(item)
        return items

# 所有request循环后，才开始解析response，解析response期间继续请求下一页面，所以会在解析之后页面的过程中出现前面的游戏信息（使用深度优先，可解决）


'''
   Google Play 爬虫需求
'''
# scrapy crawl google_spider -o test.csv

class SpiderSpider(CrawlSpider):
    name = "google_spider"
    start_urls = [
        "https://play.google.com/store/apps/category/GAME/collection/topselling_new_free",
        "https://play.google.com/store/apps/category/GAME/collection/topselling_new_paid",
        "https://play.google.com/store/apps/category/GAME/collection/topselling_free",
        "https://play.google.com/store/apps/category/GAME/collection/topselling_paid",
        "https://play.google.com/store/apps/category/GAME/collection/topgrossing",
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('.//*[@class="details"]')
        items = []
        for site in sites:
            i = GooglePlayItem()
            i['dev_name'] = site.xpath('.//a[@class="subtitle"]/text()').extract()[0].encode('utf-8')
            i['name'] = site.xpath('./a[@class="title"]/@title').extract()[0].encode('utf-8')
            i['url'] ="https://play.google.com"+ site.xpath('./a[@class="title"]/@href').extract()[0].encode('utf-8')
            items.append(i)
            yield Request(i['url'], meta={'item': i}, callback=self.parse_details)

    def parse_details(self, response):
         sel = Selector(response)
         items = []
         item = response.meta['item']
         # 邮箱可能位于第一，第二或者第三排位置，所以依次遍历三个位置，直到发现一个邮箱符合邮箱规律
         try:
             email = sel.xpath('.//a[@class="dev-link"][2]/@href').extract()[0].encode('utf-8')
             item['email'] = sel.xpath('.//a[@class="dev-link"][2]/@href').extract()[0][7:].encode('utf-8')
             #item['email'] = email[0][7:]
             if email[0:6] != 'mailto':
                 item['email'] = sel.xpath('.//a[@class="dev-link"][3]/@href').extract()[0][7:].encode('utf-8')
         except Exception,e:
             item['email'] = sel.xpath('.//a[@class="dev-link"][1]/@href').extract()[0][7:].encode('utf-8')
         items.append(item)
         return items

'''
    抓取拉勾网的公司名称
'''
class LagouSpider(CrawlSpider):
    name = "lagou_spider"
    start_urls = [
        "http://www.lagou.com/jobs/list_%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91?px=default&city=%E6%88%90%E9%83%BD"
    ]
    def parse(self, response):
        site = Selector(response)
        pages = site.xpath('.//*[@class="content_left"]')
        items = []
        for page in pages:
            i = LagouItem()
            i['campany'] = page.xpath('.//div[@class="company_name"]/a/text()').extract()
            items.append(i)
            return items

'''
    360游戏中心爬虫
'''
class ZhuShou360Spider(CrawlSpider):
    name = "zhushou360"
    start_urls = ["http://zhushou.360.cn/list/index/cid/102139/?page=1"]
    page_index = 1

    def parse(self, response):
        self.page_index += 1
        res = Selector(response)
        items = []
        sites = res.css('#iconList>li>h3>a')
        for site in sites:
            item = zhuhsou360Item()
            detail_url = site.css('::attr(href)').extract()[0]
            item['app_name'] = site.css('::text').extract()[0].encode('utf-8')
            items.append(item)
            yield Request('http://zhushou.360.cn' + detail_url, meta={'item': item}, callback=self.parse_detail)
        if self.page_index < 101:
            yield Request('http://zhushou.360.cn/list/index/cid/102139/?page=%d' % self.page_index )

    def parse_detail(self,response):
        res = Selector(response)
        items = []
        item = response.meta['item']
        item['campany_name'] = res.xpath('.//*[@id="sdesc"]/div/div/table/tbody/tr[1]/td[1]/text()').extract()[0].encode('utf-8')
        items.append(item)
        return items