# -*- coding: utf-8 -*-
import re
from scrapy import log
from scrapy.http import HtmlResponse, Response
from fpformat import extract
from logging import info
import time
from scrapy import Request, FormRequest
from scrapy.selector import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium import webdriver
from w3lib.html import get_base_url
from weblib import content
from ENGIN_144.items import GooglePlayItem


class BroswerMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        #判断为谷歌游戏网页
        if (request.url[35:48]=='category/GAME'):
        #if request.url == ('https://play.google.com/store/apps/category/GAME/collection/topselling_new_free'or 'https://play.google.com/store/apps/category/GAME/collection/topselling_new_paid'):
            print ("-----------------Browser Has Been Started--------------------------")
            driver = webdriver.Firefox()
            driver.get(request.url)
            copyright = driver.find_element_by_class_name('copyright')
            more = driver.find_element_by_id('show-more-button')
            ActionChains(driver).move_to_element(copyright).perform()
            while not copyright.is_displayed():
                copyright = driver.find_element_by_class_name('copyright')
                time.sleep(3)  # to let page content loading
                ActionChains(driver).move_to_element(copyright).perform()
                if more.is_displayed():
                    more.click()
                    print ("***********has click show-more button once !!!********")
            print ("----------------The One Of Pages Has Been Done!!!-----------------------")
            content = driver.page_source.encode('utf-8')
            url = driver.current_url.encode('utf-8')
            driver.quit()
            return HtmlResponse(url, encoding='utf-8', status=200, body=content)

        # 判断为拉勾网页
        if (request.url=="http://www.lagou.com/jobs/list_%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91?px=default&city=%E6%88%90%E9%83%BD"):
            print "拉勾网爬公司名字"
            driver = webdriver.PhantomJS()
            driver.get(request.url)
            next = driver.find_element_by_css_selector('.pager_next')
            for i in range(0,5):
                driver.find_element_by_css_selector('.pager_next').click()
                time.sleep(3)
            print "all pages done"
            content = driver.page_source.encode('utf-8')
            url = driver.current_url.encode('utf-8')
            driver.quit()
            return HtmlResponse(url, encoding='utf-8', status=200, body=content)