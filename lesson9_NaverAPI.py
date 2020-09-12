


#client ID : 84Vi3xu2hkWdAHjDHqw_

#client Secret : yDZJbsUmyX


# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys

import requests
from urllib.parse import urlparse

def get_api_length (keyword):
    url = "https://openapi.naver.com/v1/search/blog?query=" + keyword +" &display=1"
    result = requests.get(urlparse(url).geturl(), headers = {"X-Naver-Client-Id":"84Vi3xu2hkWdAHjDHqw_", "X-Naver-Client-Secret":"yDZJbsUmyX"})
    return result.json()['total']


def get_api_result (keyword, display_length, start):
    url = "https://openapi.naver.com/v1/search/blog?query=" + keyword + "&display=" + str(display_length) + "&start=" + str(start)
    result = requests.get(urlparse(url).geturl(), headers = {"X-Naver-Client-Id":"84Vi3xu2hkWdAHjDHqw_", "X-Naver-Client-Secret":"yDZJbsUmyX"})
    return result.json()

def call_and_print (keyword, start_item_index):
    json_obj = get_api_result(keyword, 5, start_item_index)
    i = 0
    for items in json_obj['items']:
        i = i+1
        title = items ['title'].replace ("<b>", "").replace ("</b>", "")
        print (i, title + "@" + items ['bloggername'] + "@" + items['link'])

        #print (i, items)

#call_and_print("고양이", 1)
#call_and_print("고양이", 2)


json_obj = call_and_print('고양이', 1)
json_obj = call_and_print('고양이', 11)
json_obj = call_and_print('고양이', 21)

print (json_obj)

#print (json_obj['items'])
#print (json_obj['total'])
#print (json_obj)

#json_obj2 = json_obj['items']
#print ("딴 줄..."+json_obj2[1]['title'])


'''
네이버 API 예제코드 (개발자센터 공인)
import urllib.request
client_id = "84Vi3xu2hkWdAHjDHqw_"
client_secret = "yDZJbsUmyX"
encText = urllib.parse.quote("고양이")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
'''
