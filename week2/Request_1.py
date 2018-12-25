from elasticsearch import Elasticsearch
from collections import Counter
import csv


def search():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    with open('Top_20_tag_.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=tags_list)
        writer.writeheader()

        for tag in tags_list:
            page = es.search(
                index='baomoi.com',
                doc_type='doc',
                scroll='2m',
                # size = 200,
                body={
                    "query": {
                        "match_phrase": {
                            "categories": {
                                "query": tag
                            }
                        }
                    }
                }
            )
            sid = page['_scroll_id']
            scroll_size = page['hits']['total']
            # print(scroll_size)
            hits = page['hits']['hits']
            cnt = Counter()
            # post = page['hits']['hits'][0]

            while scroll_size > 0:
                # print('Scrolling ...')
                page = es.scroll(scroll_id=sid, scroll='2m')
                for post in hits:
                    post_ = post['_source']['tags']
                    cnt += Counter(post_)
                hits = page['hits']['hits']
                # Update the scroll_id
                sid = page['_scroll_id']

                # Get the number of results
                scroll_size = len(page['hits']['hits'])
            for item in cnt.most_common(20):
                writer.writerow({tag: str(item[0]), "Values": item[1]})


if __name__ == '__main__':
    tags_list = ["Xã hội", "Values",
                 "Thế giới", "Values",
                 "Văn hóa", "Values",
                 "Kinh tế", "Values",
                 "Giáo dục", "Values",
                 "Pháp luật", "Values",
                 "Thể thao", "Values",
                 "Giải trí", "Values", ]
    search()
    print('Done!')
