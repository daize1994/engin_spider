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
from selenium.webdriver import ActionChains
from selenium import webdriver
from w3lib.html import get_base_url
from weblib import content
from ENGIN_144.items import GooglePlayItem


class BroswerMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        if (request.url[35:48]=='category/GAME'):
        #if request.url == ('https://play.google.com/store/apps/category/GAME/collection/topselling_new_free'or 'https://play.google.com/store/apps/category/GAME/collection/topselling_new_paid'):
            print ("-----------------browser has been started--------------------------")
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
            print ("----------------The all page has been done!!!-----------------------")
            content = driver.page_source.encode('utf-8')
            url = driver.current_url.encode('utf-8')
            driver.quit()
            return HtmlResponse(url, encoding='utf-8', status=200, body=content)
