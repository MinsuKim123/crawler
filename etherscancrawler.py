from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup

wallet_address = "0x40dE8Fa4B917Ce19648CadC5E04E03d231dea63c"
url = 'https://etherscan.io/address/' + wallet_address
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(1)

'''만약 etherscan.io 로 브라우저를 띄웠다면, 아래와 같이 검색창에 데이터를 입력할 수 있음
search_box = driver.find_element(By.ID, "txtSearchInput")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)
time.sleep(2)
'''

eth_balance = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/div[1]/div/div[2]/div[1]/div[2]')
print (eth_balance.text)

#Case 2. Klaytn Scope 에서 Klay 잔고 조회
wallet_address = "0x43e3389c620CcaCB53de2aBa8b000888B752****"
url = 'https://scope.klaytn.com/account/' + wallet_address
driver.get(url)
time.sleep(1)
kalytn_balance = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]')
print (kalytn_balance.text)


# Case3. Klaytn Token 잔고 조회 (뷰티풀수프 이용)
wallet_address = "0x43e3389c620CcaCB53de2aBa8b000888B752****"
url = 'https://scope.klaytn.com/account/' + wallet_address + '?tabId=tokenBalance'
driver.get(url)
time.sleep(1)
response = requests.get(url)

if response.status_code == 200:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    currency_value = soup.find_all('span', 'ValueWithUnit__value')
    currency_unit = soup.find_all('span', 'ValueWithUnit__unit')
    i=0
    for li in currency_unit :
        li_value = currency_value[i]
        print (li.text , li_value.text)
        i = i + 1
    time.sleep(1)
else:
    print(response.status_code)
