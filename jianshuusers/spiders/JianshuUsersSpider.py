#coding= utf-8
from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from jianshuusers.items import UserItem

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class JianshuUsersSpider(CrawlSpider):

    name = "jianshuusers"

    start_urls=[
        'http://www.jianshu.com/users/aTFqFm/following', #首席拒稿官, --> 简书签约作者
        'http://www.jianshu.com/users/1441f4ae075d/followers',#彭小六  --> 普通用户居多,下同
        'http://www.jianshu.com/users/y3Dbcz/followers',  # 简叔
        'http://www.jianshu.com/users/8f03f4df0d30/followers' #剽悍一只猫
        'http://www.jianshu.com/users/5SqsuF/followers', #刘淼
        'http://www.jianshu.com/users/d9edcb44e2f2/followers' #简书日报

    ]

    def parse(self, response):

        selector = Selector(response)

        url = str(response.url)

        ###先爬取用户的粉丝或关注的数,分页使用
        if url.find('?page') <0 :

            attennums = selector.xpath('//div[@class="info"]/ul/li/div/p/text()').extract()[0]

            attennums = int(attennums)  ##爬取关注用户时使用

            fannums = selector.xpath('//div[@class="info"]/ul/li/div/p/text()').extract()[1]
            fannums = int(fannums)



        infos = selector.xpath('//li/div[@class="info"]')

        item = UserItem()

        for info in infos:

            nickname = info.xpath('a/text()').extract()[0]
            userurl = info.xpath('a/@href').extract()[0]

            atten = info.xpath('div[1]/span[1]/text()').extract()[0]
            fans = info.xpath('div[1]/span[2]/text()').extract()[0]
            articles = info.xpath('div[1]/span[3]/text()').extract()[0]
            collections = info.xpath('div[1]/span[4]/text()').extract()[0]

            meta = (info.xpath('div[2]/text()').extract()[0]).strip()

            meta = str(meta).split('，')

            item['url'] = 'http://www.jianshu.com'+userurl
            item['nickname']= nickname
            item['atten'] = int(filter(str.isdigit,str(atten)))
            item['fans'] = int(filter(str.isdigit,str(fans)))
            item['articles'] = int(filter(str.isdigit,str(articles)))
            item['collections'] = int(filter(str.isdigit,str(collections)))

            item['words'] = int(filter(str.isdigit,str(meta[0])))
            item['likes'] = int(filter(str.isdigit,str(meta[1])))

            yield item

        if url.find('?page') < 0:
            if url.find('followers') > 0 :
                for i in range(2,(fannums/9)+2):
                    nexturl = response.url+'?page=%s'%i
                    yield Request(nexturl,callback=self.parse)
            elif url.find('following') >0:
                for i in range(2, (attennums / 9) + 2):
                    nexturl = response.url + '?page=%s' % i
                    yield Request(nexturl, callback=self.parse)





