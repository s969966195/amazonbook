#coding=utf-8
import re
from scrapy import Request
from amazon.items import AmazonItem
import requests
from scrapy.spiders import Spider
from scrapy.selector import Selector

class amazon(Spider):
    name='amazon'
    allowed_domains=['amazon.cn']
    
    def __init__(self,*args,**kwargs):
        super(amazon,self).__init__(*args,**kwargs)
        self.start_urls=[kwargs.get('start_url')]
    '''
    start_urls=[
            #'https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C',
            'https://www.amazon.cn/s/ref%5C=nb_sb_noss%5C?__mk_zh_CN%5C=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99%5C&url%5C=search-alias%3Daps%5C&field-keywords%5C=%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C',
    ]
    '''
    
    author=[]

    def parse(self,response):
        sel=Selector(response)
        for book_url in sel.xpath('//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href').extract():
            yield Request(book_url,callback=self.book_parse)

        for next_url in sel.xpath('//a[@id="pagnNextLink"]/@href').extract():
            yield Request('https://www.amazon.cn'+next_url,callback=self.parse)

    def book_parse(self,response):
        self.author=[]
        sel=Selector(response)
        item=AmazonItem()

        try:
            title=sel.xpath('//h1[@id="title"]/span[@id="productTitle"]/text()').extract()[0].strip()
        except:
            title=sel.xpath('//h1[@id="title"]/span[@id="ebooksProductTitle"]/text()').extract()[0].strip()+u'Kindle电子书'
        item['title']=title

        for author in sel.xpath('//div[@id="byline"]//a[@class="a-link-normal"]/text()').extract():
            self.author.append(author)
        item['author']=self.author

        introduction=sel.xpath('//div[@id="bookDescription_feature_div"]/noscript/div/text()').extract()
        item['introduction']=introduction
        
        try:
            p=sel.xpath('//span[@class="a-button-inner"]/a[@href="javascript:void(0)"]//span[@class="a-color-price"]/text()').extract()[0].strip()
            prime_ebook=p
            prime_paperback=None
        except:
            p=sel.xpath('//span[@class="a-button-inner"]/a[@href="javascript:void(0)"]//span[@class="a-size-base a-color-price a-color-price"]/text()').extract()[0].strip()
            prime_ebook=None
            prime_paperback=p
        item['prime_ebook']=prime_ebook
        item['prime_paperback']=prime_paperback

        li_num=len(sel.xpath('//div[@id="detail_bullets_id"]//td[@class="bucket"]/div[@class="content"]/ul/li').extract())
        try:
            promotion=sel.xpath('//table[@class="a-normal a-align-center a-spacing-small"]//span[@class="apl_m_font"]/text()').extract()[0].strip()
            item['promotion']=promotion
        except:
            item['promotion']=None

        for i in range(li_num):
            data=sel.xpath('//div[@id="detail_bullets_id"]//td[@class="bucket"]/div[@class="content"]/ul/li')[i].xpath('string(.)').extract()[0]
            if re.search(u'出版社',data):
                press=data
                item['press']=press
            elif re.search('ISBN',data):
                ISBN=data
                item['ISBN']=ISBN
            elif re.search('ASIN',data):
                ASIN=data
                item['ASIN']=ASIN

        yield item
