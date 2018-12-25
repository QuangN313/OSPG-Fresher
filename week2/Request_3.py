from elasticsearch import Elasticsearch
import json
from collections import Counter
import pickle
from underthesea import word_tokenize
from underthesea import pos_tag
# from underthesea import ner 
import math
category = ["Xã hội", "Thế giới", "Văn hóa", "Kinh tế", "Giáo dục", "Pháp luật", "Thể thao", "Giải trí"]

def cal_tf(cnt,word_list):
	tf_dict = {}
	for word, count in cnt.items():
		tf_dict[word] = count / len(word_list)
	# print(tf_dict)
	return tf_dict
	
def cal_idf(cnt,doc_list,scroll_size):
	dic = dict(cnt)
	idf_dict = dict.fromkeys(dic.keys(),0)
	for doc in doc_list:

		for word, count in cnt.items():
			if word in doc:
				idf_dict[word] += 1
	for word, count_ in idf_dict.items():
		idf_dict[word] = math.log(scroll_size/(count_+1))
	# print(idf_dict)
	return idf_dict


def search(category):
	thefile = open('Top_20_N_' + str(category) + '_tfidf.txt', 'w')
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	page = es.search(
		index ='baomoi.com',
		doc_type = 'document',
		scroll = '2m',
		# size = 100, #number of hits to return 
		body ={
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
	list_Np = ['Np']
	word_list = list()
	word_fil2 = list()
	while (scroll_size > 0):
		# print('Scrolling ...')
		page = es.scroll(scroll_id = sid, scroll = '2m')

		for post in hits:
			post_ = post['_source']['brief']
			word_tok = word_tokenize(post_)
			word_postag = pos_tag(post_)
			word_fil = list(filter(lambda x: (x[1] == 'N') and(x[0] != "'"), word_postag))
			word_fil2 = list(map(lambda x: x[0],word_fil))
			cnt += Counter(word_fil2)
			# print(cnt)
			word_list.append(post_)
			# cal_idf(cnt,word_tok,scroll_size)
			# print(word_list)
			# print (cnt.most_common(10))
		# print(cnt.most_common(10))
			# print (word_tok)
		hits = page['hits']['hits']

		# Update the scroll_id
		sid = page['_scroll_id']
		
		# Get the number of resuilts
		scroll_size = len(page['hits']['hits'])
	
	# print(type(cnt))
	tf_dict = cal_tf(cnt,word_tok)
	print ('############################')
	idf_dict = cal_idf(cnt,word_list,scroll_size_)
	# print(scroll_size_)
	tfidf = {}
	for word, val in tf_dict.items():
		tfidf[word] = val*idf_dict[word]
	sort = Counter(tfidf)
	# print(sort.most_common(20)) 	
	for item in sort.most_common(20):
		thefile.writelines("%s\n" % str(item))
def main():
	for name in category:

		search(name)

main()