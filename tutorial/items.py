# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class EtherscanProductRaw(scrapy.Item):
    '''定义需要格式化的内容（或是需要保存到数据库的字段）'''
    name = scrapy.Field()
    TxHash = scrapy.Field()
    Block = scrapy.Field()
    From_account = scrapy.Field()
    To_account = scrapy.Field()
    Value = scrapy.Field()
    TxFee = scrapy.Field()
    create_time = scrapy.Field()
    operate_type = scrapy.Field()