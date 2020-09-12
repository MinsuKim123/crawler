from urllib.request import urlopen
import json

from_date = "2018-01-01"
to_date = "2018-04-28"

url = "http://www.krei.re.kr:18181/chart/main_chart/index/kind/S/sdate/"+from_date+"/edate/"+to_date   #브라우저 개발자 모드 #Network 에서 XHR 의 Headers 참조
text = urlopen(url)
json_obj = json.load(text)

for obj in json_obj :
    print (obj['id'], obj ['date'], obj ['settlement'])

#print (json_obj )
