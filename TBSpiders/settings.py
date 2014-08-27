# -*- coding: utf-8 -*-

# Scrapy settings for TBSpiders project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'TBSpiders'

SPIDER_MODULES = ['TBSpiders.spiders']
NEWSPIDER_MODULE = 'TBSpiders.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TBSpiders (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'TBSpiders.pipelines.TbspidersPipeline': 300,
}

COOKIES_ENABLED = False

LOG_FILE = 'tb.log'

DOWNLOADER_MIDDLEWARES = {
     'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
     'TBSpiders.spiders.custom_useragent.CustomUserAgentMiddleware' : 400
}

DEFAULT_REQUEST_HEADERS = {
    'Referer': 'http://s.taobao.com'
}