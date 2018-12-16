import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def request_facebook(id, access_token):
    request_friends = requests.get('')
    requests_page = requests.get('')


def root_request(ID, access_token):
    me_url_friend = 'https://graph.facebook.com/v1.0/' + ID + '/likes?fields=name,description,category,category_list,id,' \
                                                         'created_time,likes&access_token=' + access_token
    while me_url_friend:
        root_request = requests.get()


if __name__ == "__main__":

    ACCESS_TOKEN = 'EAAAAUaZA8jlABAAF0pDnFVB6Y91ChzZAtrjCTZCp3RcSS0gdMMymiDtWzDycizDWwWpDalq9kQN1gfnbYeICZCKaqz9QZCRcxfwD6bSAMXfZCCkLwxXcbgi1uJ9N2qjBGWbZAnGW3SQPMc4FZAGz26XiKfo6tHe9OpBbb6CR30ZAO8eYGdErmgGrkuJ6fUNhhtZCsZD '
    url_friends = 'https://graph.facebook.com/v1.0/' + ID + '/friends?access_token=' + ACCESS_TOKEN
    url_page = 'https://graph.facebook.com/v1.0/' + ID + '/likes?fields=name,description,category,category_list,id,' \
                                                     'created_time,likes&access_token=' + ACCESS_TOKEN

