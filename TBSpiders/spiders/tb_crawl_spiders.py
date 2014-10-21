#coding:utf-8
import sys
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from TBSpiders.items import TbspidersItem

class TBCrawlSpiders(CrawlSpider):
    """继承自CrawlSpider，实现自动爬取的爬虫。"""
    name = "TBCrawlSpiders"
    download_delay = 4
    allowed_domains = ["taobao.com"]
    start_urls = ["http://s.taobao.com/search?initiative_id=staobaoz_20140814&js=1&" \
                  "stats_click=search_radio_all%253A1&q=%C1%AC%D2%C2%C8%B9%B6%AC"]

    rules = [
        Rule(LinkExtractor(allow=('/search?[^/]'),
                           restrict_xpaths=('//div[@class="page-top"]//a[@class="page-next"]')
                          ),
            callback='parse_item',
            follow=True)
    ]

    flag = 1

    def parse_item(self, response):
        if self.flag > 2:
            sys.exit(0)

        print "********************response url:****************** \n %s" % response.url
        self.flag += 1

        sel = Selector(response)
        shops = sel.xpath('//div[@class="tb-content"]/div[@class="row grid-view newsrp-gridcontent-el"]/div')

        for shop in shops:
            item = TbspidersItem()
            shop_name = shop.xpath('div[@class="item-box st-itembox"]/div[@class="row"]/div[1]/a/text()').extract()
            shop_address = shop.xpath('div[@class="item-box st-itembox"]/div[@class="row"]/div[2]/text()').extract()
            shop_istmall = shop.xpath('div[@class="item-box st-itembox"]/div[@class="row service-box"]/div[@class="service-btns feature-icon"]//span[@class="icon-pit icon-service-tianmao"]').extract()
            #判断是不是天猫商铺
            shop_istmall = "is_tmall" if shop_istmall else "not_tmall"
            goods_price = shop.xpath('div[@class="item-box st-itembox"]/div/div[@class="col price g_price g_price-highlight"]/strong/text()').extract()
            #清除其中的空格
            goods_price = goods_price[0].strip()
            goods_sale_num = shop.xpath('div[@class="item-box st-itembox"]/div/div[@class="col end dealing"]/text()').extract()
            #提取其中的数字
            goods_sale_num = "".join([s for s in goods_sale_num[0] if s.isdigit()])
            goods_name = shop.xpath('div[@class="item-box st-itembox"]/h3/a/@title').extract()
            goods_url = shop.xpath('div[@class="item-box st-itembox"]/h3/a/@href').extract()

            #将值储存到item里面，如果是汉字还要编码
            item["shop_name"] = [n.encode("utf-8") for n in shop_name][0]
            item["shop_address"] = [a.encode("utf-8") for a in shop_address][0]
            item["shop_istmall"] = shop_istmall
            item["goods_price"] = goods_price
            item["goods_sale_num"] = goods_sale_num
            item["goods_name"] = [na.encode("utf-8") for na in goods_name][0]
            item["goods_url"] = goods_url[0]

            yield item



