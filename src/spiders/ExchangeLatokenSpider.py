# -*- coding: utf-8 -*-
import json
import re
import xml.etree.ElementTree

import scrapy

from items import ExLatItem


class ExchangeLatokenSpider(scrapy.Spider):
    name = "exchange_latoken"
    logo = 'https://cms.latoken.com/api/currency/v1/info/'
    ieo = 'https://api.latoken.com/v2/ieo/active?size=2000&page=0'
    currency = 'https://cms.latoken.com/api/ieo/v1/projects/?crowd_sale_id={}&format=json'
    is_desc = True

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ExchangeLatokenSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def __init__(self, *args, **kwargs):
        scrapy.Spider.__init__(self, *args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(
            url=self.logo,
            callback=self.parse_logo
        )

    def parse_logo(self, response):
        logo_array = json.loads(response.body)
        logo = {}

        for item in logo_array:
            logo[item['id']] = item['logo']

        yield scrapy.Request(
            url=self.ieo,
            callback=self.parse_ieo,
            meta={
                'logo': logo,
            }
        )

    def parse_ieo(self, response):
        idx_array = json.loads(response.body)
        idxs = {}

        for item in idx_array['content']:
            idxs[item['id']] = item['rewardCurrency']

        for idx, rewardCurrency in idxs.items():
            yield scrapy.Request(
                url=self.currency.format(idx),
                callback=self.parse_currency,
                meta={
                    'logo': response.meta['logo'][rewardCurrency],
                }
            )

    def parse_currency(self, response):
        data = json.loads(response.body)['results'][0]

        icon = response.meta['logo']
        thumbnail_images = data['slider'][0]['slider_item']
        thumbnail_image = ''
        for image in thumbnail_images:
            if image['item_type'] == 'image':
                thumbnail_image = image['image']
                break

        title = data['title']
        title_symbol = data['url']

        price_currency = data['token_info'][0]['price_eth']
        price = re.search(r'([.\d]+)', price_currency)
        price = price.groups()[0] if price else ''
        cur = re.search(r'([^\d^.]+)', price_currency)
        cur = cur.groups()[0].strip() if cur else '$'

        currencies = {
            '€': 'EUR',
            'CHf': 'CHF',
            '$': 'USD',
            'Ξ': 'ETH',
        }

        currency = ''
        currency_symbol = ''
        for smb, cur_name in currencies.items():
            if cur == smb:
                currency_symbol = smb
                currency = cur_name
                break
            if cur == cur_name:
                currency_symbol = smb
                currency = cur_name
                break

        whitepaper = data['whitepaper']
        overview = data['overview'].split('\r\n')
        long_description = ''
        website = ''
        facebook = ''
        linkedin = ''
        telegram = ''
        twitter = ''

        for parag in overview:
            if '<b>Visit' in parag:
                website = self.get_href(parag)
            elif '<b>Facebook' in parag:
                facebook = self.get_href(parag)
            elif '<b>LinkedIn' in parag:
                linkedin = self.get_href(parag)
            elif '<b>Telegram' in parag:
                telegram = self.get_href(parag)
            elif '<b>Twitter' in parag:
                twitter = self.get_href(parag)
            elif self.is_desc:
                long_description += parag

        long_description = re.sub(r'<.*?>', '', long_description)
        self.is_desc = True

        videos = data['slider'][0]['slider_item']
        video = ''
        for item in videos:
            if item['item_type'] == 'video':
                video = item['video']
                break
        video_image = ''
        if video:
            if '=' in video:
                token = re.search(r'=(.+)', video)
            else:
                token = re.search(r'https://youtu\.be/(.+)', video)
            if token:
                video_image = 'https://i.ytimg.com/vi/{}/maxresdefault.jpg'
                video_image = video_image.format(token.groups()[0])

        yield ExLatItem(
            icon=icon,
            thumbnail_image=thumbnail_image,
            title=title,
            title_symbol=title_symbol,
            price=price,
            currency=currency,
            currency_symbol=currency_symbol,
            whitepaper=whitepaper,
            long_description=long_description,
            website=website,
            facebook=facebook,
            linkedin=linkedin,
            telegram=telegram,
            twitter=twitter,
            video=video,
            video_image=video_image,
        )

        # self.logger.info('icon ' + icon)
        # self.logger.info('thumbnail_image ' + thumbnail_image)
        # self.logger.info('title ' + title)
        # self.logger.info('title_symbol ' + title_symbol)
        # self.logger.info('price_currency ' + price_currency)
        # self.logger.info('price ' + price)
        # self.logger.info('cur ' + cur)
        # self.logger.info('currency ' + currency)
        # self.logger.info('currency_symbol ' + currency_symbol)
        # self.logger.info('whitepaper ' + str(whitepaper))
        # self.logger.info('overview ' + str(overview))
        # self.logger.info('long_description ' + long_description)
        # self.logger.info('website ' + website)
        # self.logger.info('facebook ' + facebook)
        # self.logger.info('linkedin ' + linkedin)
        # self.logger.info('telegram ' + telegram)
        # self.logger.info('twitter ' + twitter)
        # self.logger.info('video ' + video)
        # self.logger.info('video_image ' + video_image)

    def get_href(self, parag):
        self.is_desc = False
        source = re.search(r'href=\"(.+?)\"', parag)
        return source[0] if source else ''

    def spider_closed(self):
        pass
