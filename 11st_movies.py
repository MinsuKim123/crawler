# 11번가 모바일 화면에 접속해서, 상품 정보를 읽어오는 프로그램
# '20.9.12
# 뷰티플숲으로는 세부 목록이 읽어지지 않음 (동적 로딩)

import time
from selenium import webdriver
#from selenium.webdriver.remote.webelement import WebElement
import json
import csv
import pymysql

#f=open ('11stmovie.csv')

def jsonParser(doc, key, key2=None):
    jsonObject = json.loads(doc)
    #print (jsonObject, key, key2)
    if key2 is None:
        return jsonObject.get(key)
    else:
        return jsonObject.get(key).get(key2)

#웹드라이버 로딩
opts = webdriver.ChromeOptions()
opts.add_argument('headless')
opts.add_argument('disable-gpu')
driver = webdriver.Chrome ('./chromedriver.exe', options=opts)
driver.get("https://m.11st.co.kr/MW/html/main.html#")
driver.implicitly_wait(1)

#바닥까지 자동 스크롤
SCROLL_PAUSE_TIME = 1
new_height = 0
last_height = 1
while True:
    # 화면 최하단으로 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로드를 기다림
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    # 새로운 높이가 이전 높이와 변하지 않았을 경우 스크롤 종료
    if new_height == last_height:
        break

    # 스크롤 다운이 된다면 스크롤 다운이 된 후의 창 높이를 새로운 높이로 갱신
    last_height = new_height

elem = driver.find_elements_by_class_name("c-card__link")
#elem: WebElement = driver.find_elements_by_xpath("l-grid__col")  # class_name으로 찾아지는 최하위는 l_grid_col


db_connection = pymysql.connect(
    user='root',
    passwd='zxc135',
    host='127.0.0.1',
    db = 'product'
    #,charset='utf-8'
)

cursor = db_connection.cursor(pymysql.cursors.Cursor)


k=0
for i in elem:
    k += 1

    area = i.get_attribute("data-log-actionid-area")
    label = i.get_attribute("data-log-actionid-label")

    datalog = i.get_attribute("data-log-body")
    position_l2 = jsonParser(datalog, "position_l2")
    position_l3 = jsonParser(datalog, "position_l3")
    content_name = jsonParser(datalog, "content_name")
    movie_yn = jsonParser(datalog, "movie_yn")
    if movie_yn == "Y":
        movie_res = jsonParser(datalog, "movie_object", "movie_resolution")

    href = i.get_attribute("href")
    date1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    time1 = time.strftime('%H:%M', time.localtime(time.time()))

    print (area, movie_yn, position_l2, position_l3, content_name, movie_res)
    sql = "INSERT INTO prd_movie (date,time, serial, category, movie_yn, number_l1, number_l2, prd_name, size)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (date1, time1, k, area, movie_yn, position_l2, position_l3, content_name, movie_res))

db_connection.commit()
db_connection.close()
driver.close()

print("END")

