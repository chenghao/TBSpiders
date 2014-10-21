#coding:utf-8

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from TBSpiders.items import TbspidersItem


class TBSpider(Spider):
    """淘宝爬虫。"""
    #唯一标识
    name = "TBSpiders"
    #下一次下载等待4秒
    download_delay = 4
    allowed_domains = ["taobao.com"]
    start_urls = ["http://s.taobao.com"]

    #从第2页开始，抓取到第5页。淘宝上每页有44条数据。
    next_page_urls = []
    page_num = 44
    for i in range(1, 5):
        next_page_urls.append("http://s.taobao.com/search?spm=a230r.1.8.17.7svYcQ&stats_click=search_radio_all%253A1" \
          "&js=1&initiative_id=staobaoz_20140813&q=%C1%AC%D2%C2%C8%B9%B6%AC&suggest=history_2" \
          "&wq=%E8%BF%9E%E8%A1%A3%E8%A3%99&suggest_query=%E8%BF%9E%E8%A1%A3%E8%A3%99&source=suggest&tab=all&s=" + str(page_num * i))

    def parse(self, response):
        #由于不能直接进入搜索页，这里先到首页然后进入搜索页
        if response.url == "http://s.taobao.com":
            print "********************response url:****************** \n %s" % response.url
            #“连衣裙 女”的搜索页第一页
            url = "http://s.taobao.com/search?spm=a230r.1.8.17.7svYcQ&stats_click=search_radio_all%253A1" \
                  "&js=1&initiative_id=staobaoz_20140813&q=%C1%AC%D2%C2%C8%B9%B6%AC&suggest=history_2" \
                  "&wq=%E8%BF%9E%E8%A1%A3%E8%A3%99&suggest_query=%E8%BF%9E%E8%A1%A3%E8%A3%99&source=suggest&tab=all&s=0"

            yield Request(url, callback=self.parse)

        else:
            print "*************response url:****************** \n %s" % response.url
            sel = Selector(response)
            #sel.remove_namespaces()
            #提取所有店铺
            shops = sel.xpath('//div[@class="tb-content"]/div[@class="row grid-view newsrp-gridcontent-el"]/div')

            #逐一提取
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

            for next_page_url in self.next_page_urls:
                yield Request(next_page_url, callback=self.parse)
