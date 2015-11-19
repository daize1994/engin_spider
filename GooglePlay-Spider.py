#打包exe专用，也可以直接执行
from os import system
print 30*'*';
print 'Start Google Play Spider';
print 30*'*';

output_file_name = './result/result_googleplay.csv'
system('scrapy crawl google_spider -o ' + output_file_name + ' -t csv')

print 30*'*';
print 'Finished';
print 30*'*';
if raw_input("press any key to continue:"):
      pass

#'''
#from twisted.internet import reactor
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.project import get_project_settings
#
#runner = CrawlerRunner(get_project_settings())
#
## 'followall' is the name of one of the spiders of the project.
#d = runner.crawl('google_spider')
#d.addBoth(lambda _: reactor.stop())
#reactor.run() # the script will block here until the crawling is finished
#'''





