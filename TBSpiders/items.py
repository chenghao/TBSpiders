# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TbspidersItem(scrapy.Item):
    """存储条目信息"""

    #商铺名
    shop_name = scrapy.Field()
    #是否是天猫店铺
    shop_istmall = scrapy.Field()
    #商铺地址
    shop_address = scrapy.Field()
    #商品名
    goods_name = scrapy.Field()
    #商品URL
    goods_url = scrapy.Field()
    #商品价格
    goods_price = scrapy.Field()
    #商品卖出数量
    goods_sale_num = scrapy.Field()


