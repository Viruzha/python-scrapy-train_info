# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class Ip138Pipeline(object):
    def process_item(self, item, spider):
        
        pro=item['locat'].split(' ')[0]
        city=item['locat'].split(' ')[1]
        if os.path.isdir(f'e:/data/{pro}')==False:
            os.mkdir(f'e:/data/{pro}')
        if os.path.isdir(f'e:/data/{pro}/{city}')==False:
            os.mkdir(f'e:/data/{pro}/{city}')
        r=0
        with open(f'e:/data/{pro}/{city}/{item["name"]}.txt','w',encoding='utf8') as f:
            for i in item['route']:
                if r==0:
                    f.writelines(['ID：',item['name']+'\n','种类：',item['type_tr']+'\n','全程距离：',item['dist']+'\n','价钱：',item['cost']+'\n'])
                    r=1
                f.write(i['station']+'\t'+i['time']+'\n')
        return item
