import scrapy

from random import randint

from ip138.items import Ip138Item

class ip138(scrapy.Spider):
    name='ip'
    # start=[
    #     'http://qq.ip138.com/train/'
    # ]
    UserAgent = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    ]
    def start_requests(self):
        start_urls='http://qq.ip138.com/train/'
        
        yield scrapy.Request(callback=self.GetProvince,headers={'user-agent':self.UserAgent[randint(0,3)]},meta={'cookiejar':1},url=start_urls)




    def GetProvince(self,response):
        urls=response.xpath('//table[@width="600"]//td/a')
        for i in urls:
            url='http://qq.ip138.com'+i.xpath('./@href').extract()[0]
            locat=i.xpath('./text()').extract()[0]
            yield scrapy.Request(callback=self.GetCity,headers={'user-agent':self.UserAgent[randint(0,3)]},meta={'cookiejar':response.meta['cookiejar'],'locat':locat},url=url)
    


    def GetCity(self,response):
        urls=response.xpath('//table[@width="420"]//td/a')
        for i in urls:
            url='http://qq.ip138.com'+i.xpath('./@href').extract()[0]
            locat=response.meta['locat']+' '+i.xpath('./text()').extract()[0]
            yield scrapy.Request(callback=self.GetTrian,headers={'user-agent':self.UserAgent[randint(0,3)]},meta={'cookiejar':response.meta['cookiejar'],'locat':locat},url=url)

    

    def GetTrian(self,response):
        urls=response.xpath('''//tr[@onmouseover="this.bgColor='#E6F2E7';"]''')
        for i in urls:
            url='http://qq.ip138.com'+i.xpath('./td[1]/a/@href').extract()[0]
            tr_id=i.xpath('./td[1]/a/b/text()').extract()[0]
            if response.meta['locat'].endswith(i.xpath('./td[3]/text()').extract()[0]):#确保起始站为当前站
                yield scrapy.Request(callback=self.GetRoute,headers={'user-agent':self.UserAgent[randint(0,3)]},meta={'cookiejar':response.meta['cookiejar'],'locat':response.meta['locat'],'tr_id':tr_id},url=url)
    
    def GetRoute(self,response):
        item=Ip138Item()
        item['locat']=response.meta['locat']
        item['name']=response.meta['tr_id']
        item['type_tr']=response.xpath('//body/center[1]//td[1]/text()').extract()[0].split('：')[1]
        item['dist']=response.xpath('//body/center[1]//td[3]/text()').extract()[0].split('：')[1]
        item['cost']=response.xpath('//body/center[1]//td[4]/text()').extract()[0]
        item['route']=[]
        for i in response.xpath('''//tr[@onmouseover="this.bgColor='#E6F2E7';"]'''):
            station=i.xpath('./td[2]/a/text()')[0].extract()
            time=i.xpath('./td[3]/text()')[0].extract()
            item['route'].append({'station':station,'time':time})
        yield item


