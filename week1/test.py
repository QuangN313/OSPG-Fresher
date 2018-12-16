
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import re
from datetime import datetime

def test_parse_product(seed_url):

    req = requests.get(seed_url)
    soup = BeautifulSoup(req.text, 'lxml')
    
    title = soup.select('h1.article__header')[0].get_text().strip()
    summary = soup.select('div.article__sapo')[0].get_text().strip()
    content = ''
    for elem in soup.select('p.body-text'):
        content += (elem.get_text().strip() + ' ')
    time = soup.select('time.time')[0].get('datetime').strip()
    link = soup.select('link[rel|=canonical]')[0].get('href').strip()
    categories = soup.select('a.cate')[0].get_text().strip()
    tags = []
    for tag in soup.select('div.article__tag > p > a.keyword'):
        tags.append(tag.get_text().strip())
    source = soup.select('a.source')[0].get_text().strip()
    a = datetime.strptime(time.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
    readable = datetime.fromtimestamp(214214).isoformat()
    print(type(readable))
    print(readable)


def test_parse_link(seed_url):
    req = requests.get(seed_url)
    soup = BeautifulSoup(req.text, 'lxml')
    for pag in soup.select('a.cache'):
        pagination = urljoin(root_url, pag.get('href'))
        if root_url in pagination:
            print(pagination)


def read_csv():
    with open('regex_table.csv', 'rt') as f:
        reader = csv.DictReader(f)
        data = {}
        for row in reader:
            for header, value in row.items():
                data.setdefault(header, list()).append(value)
                print(value)
        scale_list = data['regex']
        regex_list = data['scale']
        string = ' '
        
        string = re.sub('',"",string)


def convert_price(string, index):
    string = re.sub(r"\D","",string)
    # print(string)
    value = int(float(string))
    value = value * int(float(scale_list[index]))
    return value


if __name__ == '__main__':
    base_url = 'https://baomoi.com/xa-hoi.epi'
    root_url = '{}://{}'.format(urlparse(base_url).scheme, urlparse(base_url).netloc)
    
    test_parse_product('https://baomoi.com/moi-sinh-vien-phai-la-mot-tuyen-truyen-vien-atgt-tich-cuc/c/28973999.epi')
    # set1 = Queue()
    # set1.put([1,2])
    # print(set1.qsize())
    # test_parse_link('https://baomoi.com/xa-hoi.epi')
    # req = requests.get(base_url)
    # print(req)