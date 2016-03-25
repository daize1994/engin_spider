from os import system
print 30*'*';
print 'Start Google Play Spider';
print 30*'*';

output_file_name = './result/result_lagou.csv'
system('scrapy crawl lagou_spider -o ' + output_file_name + ' -t csv')

print 30*'*';
print 'Finished';
print 30*'*';
if raw_input("press any key to continue:"):
      pass
