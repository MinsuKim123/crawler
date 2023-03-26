import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import urllib.request
import bs4

opts = webdriver.ChromeOptions()
opts.add_argument("user-data-dir=C:\\Users\\min\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome ('./chromedriver', options=opts)
#driver = webdriver.Chrome ("D:\\PyWork")

def login():
    try:
        driver.get('http://sec.egloos.com/login.php?returnurl=http://coldstar.egloos.com/7450184')
        #html = driver.page_source()
        #print (html)
        time.sleep(0)

        elem = driver.find_element_by_xpath('//*[@id="userid"]')
        ac=ActionChains(driver)
        ac.move_to_element(elem)
        ac.click()
        #ac.send_keys('coldstar')   #캐쉬에 저장된 값을 사용하므로 주석처리함
        ac.perform()
        print ("LOG:id input")

        elem = driver.find_element_by_xpath('//*[@id="userpwd_alt"]')
        ac.reset_actions()
        ac.move_to_element(elem)
        ac.click()
        #ac.send_keys('')  #캐쉬에 저장된 값을 사용하므로 주석처리함
        ac.perform()
        print ("LOG:pwd input")

        elem = driver.find_element_by_xpath('//*[@id="EKS_LOGIN"]/li[2]/button')
        ac.reset_actions()
        ac.move_to_element(elem)
        ac.click()
        ac.perform()
        print ("LOG:login button clicked")

        #input()
        time.sleep(1)

    except Exception as e:
        print(e)
    #finally:
    #    driver.quit()

def getContent(addr):
    driver.get('http://coldstar.egloos.com'+addr)
    print ("LOG:driver get Content")
    time.sleep(0)
    html = driver.page_source
    bsobj = bs4.BeautifulSoup(html, "html.parser")
    return bsobj

def getContentByUrllib (urlstring):
    html = urllib.request.urlopen(urlstring)
    bsobj = bs4.BeautifulSoup(html, "html.parser")
    print (bsobj.text)

def analysisPost (bsObjPage):
    postTitle = bsObjPage.find ("h2", {"class":"entry-title"}).text
    postDate = bsObjPage.find ("li", {"class":"post_info_date"}).text
    postContent = bsObjPage.find ("div", {"class":"hentry"})

    next = bsObjPage.find ("div", {"class":"next"})
    nextAddr = next.find ("a") ['href']
    print ("nextAddr = "+nextAddr)

    post = { 'postTitle':postTitle, 'postDate':postDate, 'postContent':postContent, 'nextAddr':nextAddr}
    return post

def parseContent (content):
    divLines = content.findAll('div')
    for eachLine in divLines:
        # 각 줄마다 div 가 매겨지는 최근 포스팅에서만 가능
        if (len(eachLine.findAll("div")) == 0) :
            images = eachLine.findAll ("img")  #Image process
            if (len(images) > 0 ):
                print ("####images = ")
                print (images [0] )
            #print (dd.find('img')['src'])
            print (eachLine.text)
        else:
            pass


### Start Main ###

print ("LOG: login started")
login()
print ("LOG: login finished")
wholePage = getContent('/4442256')
entry = analysisPost (wholePage)
parseContent(entry['postContent'])

i=0

while (entry ['nextAddr'] is not None) :
    wholePage = getContent(entry['nextAddr'])
    entry = analysisPost (wholePage)
    print ("count =", i)
    print ("postTitle =" + entry ['postTitle'])
    print ("postDate =" + entry ['postDate'])
    print ("postContent =" + entry ['postContent'].text)
    parseContent(entry['postContent'])

    i = i + 1
    if (i>10) :
        driver.close()
        exit()





#getContentByUrllib('http://coldstar.egloos.com')
