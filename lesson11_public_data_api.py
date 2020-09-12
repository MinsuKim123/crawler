import requests
import bs4
import json

endpoint = "http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?"
serviceKey = "WdMOB3Sx7GmkZmVH%2BTtyE8YV7Wv8FaHqlJE5MYk1xIiJQDYHAqQHb3%2FwFLWEvXM1d4uQUMfv3FoWRUMxOJveLw%3D%3D"
numOfRows = "10"
pageSize = "1"
pageNo = "1"
MobileOS = "ETC"
MobileApp = "AppTest"
arrange="A"
contentTypeId = "15"
areaCode = "1"
sigunguCode = "1"
listYN = "Y"

paramset = "serviceKey=" + serviceKey + "&numOfRows=" + numOfRows + "&pageSize=" + pageSize + "&pageNo=" + pageNo \
           + "&MobileOS=" + MobileOS + "&MobileApp=" + MobileApp + "&arrange=" + arrange + "&contentTypeId=" \
           + contentTypeId + "&areaCode=" + areaCode + "&sigunguCode=" + sigunguCode + "&listYN=" + listYN

url = endpoint + paramset
print (url)

result = requests.get(url)

print ("result= " +result.text)
print (result)

bsobj=bs4.BeautifulSoup(result.content, "html.parser")
print (bsobj.findAll("title"))

print ("-------------")

url = endpoint + paramset + "&_type=json"
result = (requests.get(url).json())
print (result)

i=0
for items in result['response']['body']['items'] ['item']:
    print (items ['title'], i, items)
    i=i+1

#json_obj = json.load(result.text)
#print ("result= " + jsonobj)

# print (result)
