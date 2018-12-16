# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import re
import csv
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time
from datetime import datetime


class Spider:

    def __init__(self, base_url):
        self.base_url = base_url
        self.root_url = '{}://{}'.format(urlparse(self.base_url[0]).scheme, urlparse(self.base_url[0]).netloc)
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.crawler = set()  # links crawler
        self.to_crawler = Queue()
        for self.base in self.base_url:  # next url crawler
            self.to_crawler.put(self.base)
        self.docs = list()
        self.count = 0

    @staticmethod
    def request_page(url):
        req = requests.get(url)
        return req

    @staticmethod
    def save_to_es(json):
        # for item in json:
        yield {
            "_index": "test_car",
            "_type": "json",
            "_source": json
        }

    @staticmethod
    def covert_time(time_string):
        time_datetime = datetime.strptime(time_string.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f").isoformat()
        return time_datetime

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        for pag in soup.select('a.control__next'):
            pagination = urljoin(self.root_url, pag.get('href'))
            if pagination not in self.crawler:
                self.to_crawler.put(pagination)

        for link in soup.select('a.cache'):
            product_link = urljoin(self.root_url, link.get('href'))
            if self.root_url in product_link:
                if product_link not in self.crawler:
                    self.to_crawler.put(product_link)

    def parse_info(self, html):
        soup = BeautifulSoup(html, 'lxml')

        link = ''
        categories = ''
        source = ''
        summary = ''
        title = ''
        content = ''
        tags = []
        if soup.select('h1.article__header'):
            print('Parsing ...')
            title = soup.select('h1.article__header')[0].get_text().strip()
            summary = soup.select('div.article__sapo')[0].get_text().strip()

            for elem in soup.select('p.body-text'):
                content += (elem.get_text().strip() + ' ')
            raw_time = soup.select('time.time')[0].get('datetime').strip()
            format_time = Spider.covert_time(raw_time)
            link = soup.select('link[rel|=canonical]')[0].get('href').strip()
            categories = soup.select('a.cate')[0].get_text().strip()
            for tag in soup.select('div.article__tag > p > a.keyword'):
                tags.append(tag.get_text().strip())
            source = soup.select('a.source')[0].get_text().strip()

            doc = json.dumps({
                    'title': title,
                    'summary': summary,
                    'content': content,
                    'time': format_time,
                    'link': link,
                    'categories': categories,
                    'tags': tags,
                    'source': source,
            })
            self.docs.append(doc)

            if len(self.docs) == 200:
                self.count += 1
                print('Bulking ...')
                bulk(es, self.docs, index='baomoi.com', doc_type='doc')
                self.docs = list()

            if self.count == 100:
                run_time = time.time() - start_time
                with open('report.txt', 'w') as f:
                    f.writelines(f'Time: {run_time}')

        else:
            return

    @staticmethod
    def convert_price(string, index):
        string = re.sub(r"\D", "", string)
        value = int(float(string))
        value = value * int(float(scale_list[index]))
        return value

    def post_scrape_callback(self, res):
        result = res.result()
        if result.status_code == 200:
            self.parse_links(result.text)
            self.parse_info(result.text)
        else:
            return

    def run(self):
        while self.count < 100:
            try:
                target_url = self.to_crawler.get()
                print('Crawler ...')
                # print(self.to_crawler.qsize())
                # print(target_url)
                if target_url not in self.crawler:
                    self.crawler.add(target_url)
                    job = self.pool.submit(self.request_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)
                    time.sleep(0.3)
            except Empty:
                return
            except Exception as e:
                # print(e)
                continue


if __name__ == '__main__':
    # read csv file
    start_time = time.time()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    with open('import_table.csv', 'rt') as f1:
        reader1 = csv.DictReader(f1)
        data_ = {}
        for row in reader1:
            for header, value in row.items():
                data_.setdefault(header, list()).append(value)
        links = data_['link']
    s = Spider(links)
    s.run()

