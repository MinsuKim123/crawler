#!/usr/bin/python3
from requests_oauthlib import OAuth1Session
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import bs4

opts = webdriver.ChromeOptions()
opts.add_argument("user-data-dir=C:\\Users\\min\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome ('./chromedriver', options=opts)

request_token_url = 'http://api.egloos.com/request_token'
base_authorization_url = 'http://api.egloos.com/authorize'
access_token_url = 'http://api.egloos.com/access_token'

def get_request_token(client_key, client_secret):
    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    return {
        'oauth_session': oauth,
        'oauth_token': resource_owner_key,
        'oauth_token_secret': resource_owner_secret,
    }

def get_oauth_verifier(oauth_session):
    authorization_url = oauth_session.authorization_url(base_authorization_url)
    print('visit the page and authorize: ')
    print ("### start get_oauth" )
    print(authorization_url)

    driver.get(authorization_url)
    time.sleep(0)

    elem = driver.find_element_by_xpath('//*[@id="userid"]')
    ac=ActionChains(driver)
    ac.move_to_element(elem)
    ac.click()
    #ac.send_keys('coldstar')   #캐쉬에 저장된 값을 사용하므로 주석처리함
    ac.perform()
    print ("### oauth.py: selenium id input")

    elem = driver.find_element_by_xpath('//*[@id="userpwd"]')
    ac.reset_actions()
    ac.move_to_element(elem)
    ac.click()
    #ac.send_keys('your password')  #캐쉬에 저장된 값을 사용하므로 주석처리함
    ac.perform()
    print ("### oauth.py: selenium pwd input")


    elem = driver.find_element_by_xpath('//*[@id="content"]/form/div/div/div[2]/input[1]')
    ac.reset_actions()
    ac.move_to_element(elem)
    ac.click()
    ac.perform()
    print ("### oauth.py: selenium login button clicked")

    #input()
    time.sleep(2)


    redirect_response = authorization_url
    # oauth_response = oauth_session.parse_authorization_response(redirect_response)
    # verifier = oauth_response.get('verifier')
    print ("### redirect_response.split(sep[0] = " +  redirect_response.split(sep="=")[0] )
    print ("### redirect_response.split(sep[1] = " +  redirect_response.split(sep="=")[1] )


    verifier = redirect_response.split(sep='=')[1]
    #driver.close()

    return verifier

def get_access_token(client_key, client_secret, request_token, request_secret,
                        verifier):
    oauth = OAuth1Session(client_key, client_secret=client_secret,
        resource_owner_key=request_token, resource_owner_secret=request_secret,
        verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    print ("### oauth.py_get_access_token : resource_owner_key= " + resource_owner_key)


    return {
        'oauth_token': resource_owner_key,
        'oauth_token_secret': resource_owner_secret,
    }

def request(client_key, client_secret, access_key, access_secret, url):
    oauth = OAuth1Session(client_key, client_secret=client_secret,
        resource_owner_key=access_key, resource_owner_secret=access_secret)
    r = oauth.get(url)

    return r

def post(client_key, client_secret, access_key, access_secret, url):
    oauth = OAuth1Session(client_key, client_secret=client_secret,
        resource_owner_key=access_key, resource_owner_secret=access_secret)
    r = oauth.post(url)

    return r

def get_secret_html(post_no):
    driver.get('http://coldstar.egloos.com/'+post_no)
    print ("LOG:driver get Content")
    time.sleep(0)
    html = driver.page_source
    bsobj = bs4.BeautifulSoup(html, "html.parser")
    return bsobj
