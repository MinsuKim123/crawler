

#!/usr/bin/python3
#import json
#file_contents = json.loads(open('post_index.json','r').read())

import os
import re
import oauth
import json
from json import JSONDecoder, JSONEncoder
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import bs4

opts = webdriver.ChromeOptions()
opts.add_argument("user-data-dir=C:\\Users\\min\\AppData\\Local\\Google\\Chrome\\User Data")



decoder = JSONDecoder()
encoder = JSONEncoder()

# Authentication
user_name = 'coldstar'
client_key = '11e92bcc33bd295105ea401d5347691605cd768a0'
client_secret = '9d02bc763de136be2d052748881b2f62'
URL = 'http://api.egloos.com/{}/post.json?page='.format(user_name)
POST_URL = 'http://api.egloos.com/{}/post/'.format(user_name)
WRITE_URL = 'http://api.egloos.com/{}/post.json'.format(user_name)

req = oauth.get_request_token(client_key, client_secret)
verifier = oauth.get_oauth_verifier(req['oauth_session'])
acc = oauth.get_access_token(client_key, client_secret, req['oauth_token'],
    req['oauth_token_secret'], verifier)

# 공통 파일
def saveToFile (filename, py_li, ct_li):
    #filename = cleanText (p['post_date_created']) + cleanText(p['post_title']) + '.json'
    try:
        if is_saved('posts/' + filename) == False :
            fetch = py_li['post']
            post_json = encoder.encode(fetch)
            f = open('posts/' + filename, encoding='utf-8', mode='w')
            f.write(post_json)

            for ct in ct_li:
                f.write(encoder.encode(ct))
            f.close()
            print('saved to posts/' + filename)
        else:
            print('file already saved at posts/' + filename)
            return
    except KeyError:
        print('비공개 포스팅이라서 가져오지 못함 : ' + filename)

def append_file():
    print ("### append additional list to the list")
    base = int(len(post_index)/10)
    print ("post index = " + str(base))
    for i in range (1, page_max + 1):
        url = URL + str (base+i)
        print ("###request url = " + url)
        r = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], url)
        print (r.content)
        py_li = decoder.decode(r.content.decode())
        posts = py_li ['post']
        for p in posts:
            print (p)
            post_index.append(p)

def is_saved(path):
    #return False ppp
    try:
        os.stat(path)
        return True
    except FileNotFoundError:
        return False

def cleanText(readData):
    #텍스트에 포함되어 있는 특수 문자 제거 - From https://niceman.tistory.com/156
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)
    return text



post_index = []
post_list = []
page_max = 5

try:    # 포스트 목록 파일이 있으면 파일을 읽어들임
    os.stat('post_index.json')
    f = open('post_index.json', encoding='utf-8')
    post_index_json = f.read()
    post_index = decoder.decode(post_index_json)
    print('file opened: post_index.json')

except FileNotFoundError:    #포스트 목록 파일이 없으면 API로 목록을 읽어들임
    print ("### exception handling : FileNotFound logic started")
    for i in range(1, page_max + 1):
        url = URL + str(i)
        r = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], url)
        print (r.content)
        py_li = decoder.decode(r.content.decode())
        posts = py_li['post']
        for p in posts:
            print (p)
            post_index.append(p)

print('sorting by date ...')
post_index.sort(key=lambda post: post['post_date_created'], reverse=True)
print('get indexes total ' + str(len(post_index)))
act = ''

driver = webdriver.Chrome ('./chromedriver', options=opts)

while act != 'b':
    act = input('전체 목록에 대한 action [l:목록보기 / a:목록 더 가져오기 /  s:목록보관 / AUTO:목록전체 저장 / p:HTML 파싱 / b:포스트별 작업 ]: ')

    if act == 'l':   #목록 보기
        i =0
        for p in post_index:
            i = i + 1
            print(str(i) + " " + p['post_date_created'] + " " + p['post_title'])
        print('')

    elif act == 'a':  #목록 더 가져오기
        append_file()
        print('another posts appended')

    elif act == 's':  #목록을 파일로 보관
        post_index_json = encoder.encode(post_index)
        f = open('post_index.json', encoding='utf-8', mode='w')
        f.write(post_index_json)
        f.close()
        print('saved to post_index.json')

    elif act == 'AUTO' or act == 'SAVE': # 목록에 있는 모든 포스팅을 파일로 보관
        for p in post_index:
            if p['post_hidden'] == 0 :
                filename = cleanText (p['post_date_created']) + cleanText(p['post_title']) + '.json'
                if is_saved('posts/' + filename) == False :
                    url = POST_URL + p['post_no'] + '.json'
                    r = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], url)
                    py_li = decoder.decode(r.content.decode())

                    urlComment = POST_URL + p['post_no'] +"/comment.json"
                    rComment = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], urlComment)
                    comment_li = decoder.decode(rComment.content.decode())
                    if comment_li['comment'] is not None :
                        ct_li = comment_li['comment']
                    else :
                        ct_li = ""
                    saveToFile(filename, py_li, ct_li)
                else:
                    print("filename "+filename+" already saved")
            else:

                '''포스팅 작성 샘플
                command = "post_title=abcd&post_content=content&post_hidden=1"
                url = WRITE_URL + '?' + command
                r = oauth.post(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], url)
                print (decoder.decode(r.content.decode()))
                '''

                '''포스팅 업데이트 : API가 정상이라면 제대로 작동해야 함 (권한 오류 발생)
                command = "post_title=abcd&post_content=content&post_hidden=0"
                url = POST_URL + '7455944' + '.json' + '?' + command
                r = oauth.post(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], url)
                print (decoder.decode(r.content.decode()))
                '''
                print ("hidden post : require to implement Selenium")
                bsobj = oauth.getdata (p['post_no'])
                print()


    elif act == 'p':
        file_list = os.listdir('./posts')
        source_list = [file for file in file_list if file.endswith (".json")]

        for source_file_name in reversed(source_list):
            dest_file_name = source_file_name.split('.') [0] + ".html"

            if is_saved('./posts/'+dest_file_name) == False :
                f = open('./posts/' + source_file_name, encoding = 'utf-8')
                source_txt = f.read().split('}')
                t = open('./posts/' + source_file_name.split('.') [0] + '.html', mode='w')
                print ('----START -----')

                #source_txt[0] = 본문, [1]~[N] = 커멘트
                #본문 파싱하기
                try:
                    post_json = json.loads(source_txt[0]+"}")
                    print(post_json)
                    t.write("<H2>"+post_json['post_title']+"</H2>")
                    t.write("<H3>"+post_json['post_date_created']+"</H3>")
                    t.write("<div>카테고리:"+post_json['category_name']+"</div>")
                    t.write("<div> <a href=\"http://coldstar.egloos.com/"+post_json['post_no']+"\">"+"http://coldstar.egloos.com"+post_json['post_no']+"</a></H3>"  )
                    t.write(post_json['post_content'])

                except:
                    post_json = ""
                    print ("###post_json error!")

                #커멘트 파싱하기
                t.write("<H3>Comment</H3><div>")
                for i in range (len(source_txt)-2):
                    try:
                        comment_json = json.loads(source_txt[i+1]+"}")
                        #print (json.loads(source_txt[i+1]+"}"))
                        print (comment_json)
                        t.write(comment_json['comment_date_created']+"  ")
                        t.write("<B>"+comment_json['comment_nick']+"</B>  ")
                        t.write(comment_json['comment_content']+"\n<br>")

                    except:
                        #comment_json[i] = ""
                        print ("###comment_json error!")
                t.close()
                print ("------------절 취 선 ----------")

            else :
                print (dest_file_name+" already exists")

# ----------------------------------------------------------------------------------------------
# 각 파일에 대한 상세 작업 루틴 : 꼭 실행할 필요는 없음

for p in post_index:
    fetch = None
    #filename = p['post_date_created'].replace('-', '').replace(':','').replace(' ','_') + cleanText(p['post_title'])
    filename = cleanText (p['post_date_created']) + cleanText(p['post_title']) + '.json'
    act = ''
    while act != 'n':
        print("\n* 제목="+ p['post_title'] + "  날짜=" + p['post_date_created'] + "   공개=" + str(p['post_hidden']))
        act = input('세부 포스트에 대한 action [p:print / n:next / s:save and next / q:saved?]: ')

        if act == 'p':
        #if fetch == None:
            url = POST_URL + p['post_no'] + '.json'
            r = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], url)
            print ("### post request r = ")
            print (r.content)
            py_li = decoder.decode(r.content.decode())

            if 'post' in py_li :
                fetch = py_li['post']

                print('')
                print('title: ' + fetch['post_title'])
                print('no: ' + str(fetch['post_no']))
                print('content: ')
                print(fetch['post_content'])
                print('category: ' + fetch['category_name'])
                print('category_no: ' + str(fetch['category_no']))
                print('name: ' + fetch['post_nick'])
                print('comments: ' + str(fetch['comment_count']))
                print('trackbacks: ' + str(fetch['trackback_count']))
                print('hidden? ' + str(fetch['post_hidden']))
                print('commend allowed? ' + str(fetch['comment_enabled']))
                print('trackback allowed? ' + str(fetch['trackback_enabled']))
                print('date: ' + fetch['post_date_created'])
               # print('update: ' + fetch['post_date_modified'])
               # print('tags: ' + fetch['post_tags'])
                print('-------------------------------------------')

            elif 'error' in py_li :
                print ("????????????")
                print(r.content.decode())

            #comment
            urlComment = POST_URL + p['post_no'] +"/comment.json"
            rComment = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], urlComment)
            comment_li = decoder.decode(rComment.content.decode())
            #fetchComment = comment_li['comment']

            print()
            if comment_li['comment'] is not None :
                for cp in comment_li['comment'] :
                    print (cp['comment_nick'])
                    print (cp['comment_content'])
                    print (cp['comment_depth'])

        elif act == 's':   #save and next
        #if fetch == None:
            url = POST_URL + p['post_no'] + '.json'
            r = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], url)
            py_li = decoder.decode(r.content.decode())

            #if py_li[]

            urlComment = POST_URL + p['post_no'] +"/comment.json"
            rComment = oauth.request(client_key, client_secret, acc['oauth_token'], acc['oauth_token_secret'], urlComment)
            comment_li = decoder.decode(rComment.content.decode())
            if comment_li['comment'] is not None :
                ct_li = comment_li['comment']
            else :
                ct_li = ""

            filename = cleanText (p['post_date_created']) + cleanText(p['post_title']) + '.json'
            saveToFile(filename, py_li, ct_li)
            break

        elif act == 'a':
            # hidden post could not be fetched (bug)
            if str(p['post_hidden']) != '1' and is_saved('posts/' + filename) == False:
                # not implemented
                '''
                if fetch == None:
                    url = POST_URL + p['post_no'] + '.json'
                    r = oauth.request(client_key, client_secret,
                            acc['oauth_token'], acc['oauth_token_secret'], url)
                    py_li = decoder.decode(r.content.decode())
                    fetch = py_li['post']
                post_json = encoder.encode(fetch)
                f = open('posts/' + filename, encoding='utf-8', mode='w')
                f.write(post_json)
                f.close()
                print('saved to posts/' + filename)
                break
                '''

        elif act == 'q':
            if is_saved('posts/' + filename) == True:
                print('yes! :)')
                print('')
            else:
                print('not yet')
                print('')

print('== end ==')
