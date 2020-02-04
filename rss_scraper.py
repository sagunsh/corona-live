# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import pymysql
import pytz
import scrapy
from dateutil.parser import parse
from env import HOST, DATABASE, USER, PASSWORD


class RssScraperSpider(scrapy.Spider):
    name = 'rss_scraper'

    conn = pymysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    # add more rss urls as needed
    start_urls = ['https://www.aljazeera.com/xml/rss/all.xml', 'http://rss.cnn.com/rss/cnn_latest.rss', 
                'https://www.business-standard.com/rss/latest.rss', 'https://news.yahoo.com/rss', 
                'https://www.scmp.com/rss/318208/feed']
    
    # add more keywords of interest
    keywords = ['coronavirus', 'corona virus', 'wuhan', 'hubei']

    def parse(self, response):
        parsed_uri = urlparse(response.url)
        for news in response.css('item'):
            title = news.css('title::text').get('').strip()
            description = news.css('description::text').get('').strip()

            # check if the keywords are present in the title and description
            if self.is_corona_related(title) or self.is_corona_related(description):
                item = {
                    'link': response.urljoin(news.css('link::text').get().strip()),
                    'title': title,
                    # https://www.aljazeera.com/xml/rss/all.xml becomes aljazeera.com
                    'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                    # convert datetime to UTC datetime
                    'published_date': parse(news.css('pubDate::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
                }
                self.insert_into_db('news', item)

    def is_corona_related(self, text):
        for keyword in self.keywords:
            if keyword in text.lower():
                return True
        return False

    def insert_into_db(self, table, item, key=None):
        try:
            placeholder = ', '.join(["%s"] * len(item))
            statement = 'INSERT IGNORE INTO {table} ({columns}) VALUES ({values})'.format(
                table=table, columns=','.join(item.keys()), values=placeholder)
            self.cursor.execute(statement, list(item.values()))
            self.conn.commit()
            print('Item: {} inserted to {}'.format(item, table))
        except Exception as e:
            print('Error {} while inserting {}'.format(e, item))
            return False
