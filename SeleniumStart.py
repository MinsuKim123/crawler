import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib.request
import bs4

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#userID = "coldstar"
#userPassword = "aaaaaa"
#lastPostAddr = "7579826"

userID = input("이글루스ID는 ? ")
userPassword = input("이글루스 패스워드는 ? ")
lastPostAddr = input("최종 포스트 번호는 ? ")
filename =  input ("저장할 파일 경로/이름은? (예: D:/egloosBackup.txt ")
if filename =="":
    filename="D:/egloosBackup2.txt"

blogAddr = userID+'egloos.com'

def login():
    try:

        addr = "http://sec.egloos.com/login.php?returnurl=http://"+blogAddr+"/"+lastPostAddr
        driver.get(addr)

        elem = driver.find_element(By.XPATH,'//*[@id="userid"]')
        #elem = driver.find_element_by_xpath('//*[@id="userid"]')
        ac=ActionChains(driver)
        ac.move_to_element(elem)
        ac.click()
        ac.send_keys(userID)
        ac.perform()
        print ("LOG:id input")

        elem = driver.find_element(By.XPATH, '//*[@id="userpwd_alt"]')
        #elem = driver.find_element_by_xpath('//*[@id="userpwd_alt"]')
        ac.reset_actions()
        ac.move_to_element(elem)
        ac.click()
        ac.send_keys(userPassword)  #캐쉬에 저장된 값을 사용하므로 주석처리함
        ac.perform()
        print ("LOG:pwd input")

        elem = driver.find_element(By.XPATH, '//*[@id="EKS_LOGIN"]/li[2]/button')
        #elem = driver.find_element_by_xpath('//*[@id="EKS_LOGIN"]/li[2]/button')
        ac.reset_actions()
        ac.move_to_element(elem)
        ac.click()
        ac.perform()
        print ("LOG:login button clicked")

    except Exception as e:
        print("LOG: Exception")
        print(e)
        driver.quit()
    #finally:
    #    driver.quit()

def getContent(addr):
    driver.get('http://coldstar.egloos.com/'+addr)
    print ("LOG:driver get Content")
    html = driver.page_source
    bsobj = bs4.BeautifulSoup(html, "html.parser")
    return bsobj

def getContentByUrllib (urlstring):
    html = urllib.request.urlopen(urlstring)
    bsobj = bs4.BeautifulSoup(html, "html.parser")
    print (bsobj.text)

def analysisPost (bsObjPage):  #페이지를 읽어서 제목, 날짜, 본문, 다음페이지 주소를 리턴한다
    postTitleRaw = bsObjPage.find ("h2", {"class":"entry-title"})
    postDate = bsObjPage.find ("li", {"class":"post_info_date"}).text
    postContent = bsObjPage.find ("div", {"class":"hentry"})
    postComment = bsObjPage.find("div", {"class": "post_comment"})

    postTitle = postTitleRaw.contents[1].text
    nextPg = bsObjPage.find ("div", {"class":"next"})  #nextAddr 구하기 위한 임시 변수
    nextAddr = nextPg.find ("a") ['href']

    post = { 'postTitle':postTitle, 'postDate':postDate, 'postContent':postContent, 'postComment':postComment, 'nextAddr':nextAddr}
    return post

def imageDownload (content):
    divLines = content.findAll('div')
    for eachLine in divLines:
        # 각 줄마다 div 가 매겨지는 최근 포스팅에서만 가능
        if (len(eachLine.findAll("div")) == 0) :
            images = eachLine.findAll ("img")  #Image process
            if (len(images) > 0 ):
                print ("####images = ")
                print (images [0] )
            #print (dd.find('img')['src'])
            #print (eachLine.text)
        else:
            pass


def makeText (entry):
    post = "## 제목: " + entry['postTitle'] + "\n"+\
           "## 날짜: " + entry['postDate'] + \
           "## 본문: \n"+ entry['postContent'].text.replace('\xa0','\n').replace('<br/>','\n').replace('\n\n\n신고\n\n',"") + \
           "## 댓글: \n"+entry['postComment'].text.replace('\n','').replace('댓글 입력 영역 닉네임비밀번호블로그로그인 비공개','') + "\n"\
           "## 다음 포스트 고유번호:"+entry['nextAddr'] + "\n************************************\n\n\n\n"
    return post

def writeToOneTxtfile (entryTextList):
    for i in entryTextList :
        f.write(i)
    f.close()

def appendToExistingTxtfile (entryText):
    f.write(entryText)


### Start Main ###
print ("LOG: login started")
login()
print ("LOG: login finished")


wholePage = getContent(lastPostAddr)
print ("LOG: getContent finished")

entry = analysisPost (wholePage)
print ("LOG: analysisPost finished")

imageDownload(entry['postContent'])
print ("LOG: parseContent finished")

i=0

entryTextList = []
entryTextList.append(makeText(entry))
f = open("D:/egloosBackup.txt", "a", encoding='utf-8')

while (entry ['nextAddr'] is not None) :
    wholePage = getContent(entry['nextAddr'])
    entry = analysisPost (wholePage)
    postText=makeText(entry)
    entryTextList.append(postText)
    print (postText)
    appendToExistingTxtfile(postText)
    #imageDownload(entry['postContent'])
    i = i + 1

    if (i>10) :
        writeToOneTxtfile(entryTextList)
        driver.close()
        exit()

'''
    print ("count =", i)
    print ("postTitle =" + entry ['postTitle'])
    print ("postDate =" + entry ['postDate'])
    print ("postContent =" + entry ['postContent'].text)
    print ("postComment = " + entry ['postComment'].text) '''







#getContentByUrllib('http://coldstar.egloos.com')
