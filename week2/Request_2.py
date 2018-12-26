from elasticsearch import Elasticsearch
import csv
from collections import Counter
from underthesea import word_tokenize
from underthesea import pos_tag
import math
import time


def cal_tf(cnt, word_list):
    tf_dict = {}
    for word, count in cnt.items():
        tf_dict[word] = count / len(word_list)
    # print(tf_dict)
    return tf_dict


def cal_idf(cnt, doc_list, scroll_size):
    dic = dict(cnt)
    idf_dict = dict.fromkeys(dic.keys(), 0)
    for doc in doc_list:
        for word, count in cnt.items():
            if word in doc:
                idf_dict[word] += 1
    for word, count_ in idf_dict.items():
        idf_dict[word] = math.log(scroll_size / (count_ + 1))
    # print(idf_dict)
    return idf_dict


def search_tf_idf(category, tags_list):
    with open(TMP_PATH + 'Top_20_keyword_' + str(category) + '_tf_idf.csv', 'w',  encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=tags_list)
        writer.writeheader()
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        page = es.search(
            index='baomoi.com',
            doc_type='doc',
            scroll='2m',
            # size = 100, #number of hits to return
            body={
                "query": {
                    "match_phrase": {
                        "categories": {
                            "query": category
                        }
                    }
                }
            }
        )

        sid = page['_scroll_id']
        scroll_size_ = page['hits']['total']
        print(category)
        scroll_size = 1
        hits = page['hits']['hits']
        cnt = Counter()
        stop_word = ['bị', 'bởi', 'cả', 'các', 'cái', 'cần', 'càng', 'chỉ', 'chiếc', 'cho', 'chứ', 'chưa', 'chuyện', 'có',
                     'có thể', 'cứ', 'của', 'cùng', 'cũng', 'đã', 'đang', 'đây', 'để', 'đến', 'đến nỗi', 'đều', 'điều',
                     'do', 'đó',
                     'được', 'dưới', 'gì', 'khi', 'không', 'là', 'lại', 'lên', 'lúc', 'mà', 'mỗi', 'một', 'một cách', 'này',
                     'năm' 'nên',
                     'nếu', 'ngay', 'nhiều', 'như', 'nhưng', 'những', 'nơi', 'nữa', 'ở' 'phải', 'qua', 'ra', 'rằng', 'rằng',
                     'rất', 'rất', 'rồi', 'sau', 'sẽ', 'so', 'sự', 'tại', 'theo', 'thì', 'trên', 'trong', 'trước', 'từ',
                     'từng',
                     'và', 'vẫn', 'vào', 'vậy', 'về', 'vì', 'việc', 'với', 'vừa', '!', '"', '#', '$', '%', '&', "'", '(',
                     ')',
                     '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|',
                     '}', '~']

        word_list = list()
        while (scroll_size > 0):
            # print('Scrolling ...')
            page = es.scroll(scroll_id=sid, scroll='2m')

            for post in hits:
                post_ = post['_source']['summary']
                word_tok = word_tokenize(post_)
                word_fil = list(filter(lambda x: x not in stop_word, word_tok))
                cnt += Counter(word_fil)
                word_list.append(post_)
            # cal_idf(cnt,word_tok,scroll_size)
            # print(word_list)
            # print (cnt.most_common(10))
            # print(cnt.most_common(10))
            # print (word_tok)
            hits = page['hits']['hits']

            # Update the scroll_id
            sid = page['_scroll_id']

            # Get the number of results
            scroll_size = len(page['hits']['hits'])

        # print(type(cnt))
        tf_dict = cal_tf(cnt, word_tok)
        print('############################')
        idf_dict = cal_idf(cnt, word_list, scroll_size_)
        # print(scroll_size_)
        tf_idf = {}
        for word, val in tf_dict.items():
            tf_idf[word] = val * idf_dict[word]
        sort = Counter(tf_idf)
        # print(sort.most_common(20))
        for item in sort.most_common(20):
            writer.writerow({category: str(item[0]), tags_list[1]: "{0:.2f}".format(item[1])})


def search(category, tags_list):
    with open(TMP_PATH + 'Top_20_keyword_' + str(category) + '.csv', 'w',  encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=tags_list)
        writer.writeheader()
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        page = es.search(
            index='baomoi.com',
            doc_type='doc',
            scroll='2m',
            # size = 100, #number of hits to return
            body={
                "query": {
                    "match_phrase": {
                        "categories": {
                            "query": category
                        }
                    }
                }
            }
        )

        sid = page['_scroll_id']
        scroll_size_ = page['hits']['total']
        print(category)
        scroll_size = 1
        hits = page['hits']['hits']
        cnt = Counter()
        stop_word = ['bị', 'bởi', 'cả', 'các', 'cái', 'cần', 'càng', 'chỉ', 'chiếc', 'cho', 'chứ', 'chưa', 'chuyện', 'có',
                     'có thể', 'cứ', 'của', 'cùng', 'cũng', 'đã', 'đang', 'đây', 'để', 'đến', 'đến nỗi', 'đều', 'điều',
                     'do', 'đó',
                     'được', 'dưới', 'gì', 'khi', 'không', 'là', 'lại', 'lên', 'lúc', 'mà', 'mỗi', 'một', 'một cách', 'này',
                     'năm' 'nên',
                     'nếu', 'ngay', 'nhiều', 'như', 'nhưng', 'những', 'nơi', 'nữa', 'ở' 'phải', 'qua', 'ra', 'rằng', 'rằng',
                     'rất', 'rất', 'rồi', 'sau', 'sẽ', 'so', 'sự', 'tại', 'theo', 'thì', 'trên', 'trong', 'trước', 'từ',
                     'từng',
                     'và', 'vẫn', 'vào', 'vậy', 'về', 'vì', 'việc', 'với', 'vừa', '!', '"', '#', '$', '%', '&', "'", '(',
                     ')',
                     '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|',
                     '}', '~']

        word_list = list()
        while 0 < scroll_size:
            # print('Scrolling ...')
            page = es.scroll(scroll_id=sid, scroll='2m')

            for post in hits:
                post_ = post['_source']['summary']
                word_tok = word_tokenize(post_)
                word_fil = list(filter(lambda x: x not in stop_word, word_tok))
                cnt += Counter(word_fil)
                word_list.append(post_)
            # cal_idf(cnt,word_tok,scroll_size)
            # print(word_list)
            # print (cnt.most_common(10))
            # print(cnt.most_common(10))
            # print (word_tok)
            hits = page['hits']['hits']

            # Update the scroll_id
            sid = page['_scroll_id']

            # Get the number of results
            scroll_size = len(page['hits']['hits'])

        # print(type(cnt))
        tf_dict = cal_tf(cnt, word_tok)
        print('############################')
        idf_dict = cal_idf(cnt, word_list, scroll_size_)
        # print(scroll_size_)
        tf_idf = {}
        for word, val in tf_dict.items():
            tf_idf[word] = val * idf_dict[word]
        sort = Counter(tf_idf)
        # print(sort.most_common(20))
        for item in sort.most_common(20):
            writer.writerow({category: str(item[0]), tags_list[1]: item[1]})


def main():
    for name in category:
        key_word_count = name + '_' + 'keywords_count'
        tags_list = [name, key_word_count]
        search(name, tags_list)


if __name__ == '__main__':
    start_time = time.time()
    TMP_PATH = "C:\\Users\\QuangNguyen\\Desktop\\OSPG-Fresher\\week2\\tmp\\"
    category = ["Xã hội", "Thế giới", "Văn hóa", "Kinh tế", "Giáo dục", "Pháp luật", "Thể thao", "Giải trí"]
    main()
    run_time = (time.time() - start_time) / 60
    print(f'Run time: {run_time} phut')
