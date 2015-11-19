# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from openpyxl import Workbook
import csv

# class Engin144Pipeline(object):
#     def process_item(self, item, spider):
#         return item
#
# class ENGIN_147_Pipeline(object):
#
#     def __init__(self):
#         self.file = codecs.open('w3school_data_utf8.csv', 'wb', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         line = csv.dumps(dict(item)) + '\n'
#         # print line
#         self.file.write(line.decode("unicode_escape"))
#         return item
#
# def write_to_csv(item):
#        writer = csv.writer(codecs.open('w3school_data_utf8.csv', 'wb', encoding='utf-8'), dialect='excel', lineterminator='\n')
#        writer.writerow([item[key] for key in item.keys()])
#
# class WriteToCsv(object):
#     def process_item(self, item, spider):
#             write_to_csv(item)
#             return item
#
#
# class TuniuPipeline(object):  # 设置工序一
#     wb = Workbook()
#     ws = wb.active
#     ws.append(['游戏名', '开发者', '邮箱', '游戏链接'])  # 设置表头
#
#
# def process_item(self, item, spider):  # 工序具体内容
#     line = [item['name'], item['dev_name'], item['email'], item['url']]  # 把数据中每一项整理出来
#     self.ws.append(line)  # 将数据以行的形式添加到xlsx中
#     self.wb.save('C:/Users/Administrator/Scrapy_proj/ENGIN_147/tuniu.xlsx')  # 保存xlsx文件
#     return item