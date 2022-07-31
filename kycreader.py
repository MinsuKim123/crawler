from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


with open('user.txt', 'r') as x:
    username_kdac = x.readline().rstrip()
    password_kdac = x.readline()

# 로그인
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://kyc6.com')
time.sleep(1)

username_box = driver.find_element(By.ID, "Username")
username_box.send_keys(username_kdac)

password_box = driver.find_element(By.ID, "PasswordDisplay")
password_box.send_keys(password_kdac)

password_box.send_keys(Keys.RETURN)
time.sleep(5)

# Search 이동
driver.find_element(By.XPATH, '//*[@id="71"]/a').click()
time.sleep(3)

# 명단 읽어서 검색하고 다운로드
f = open('people_list.csv', encoding='utf-8')
reader_temp = csv.reader(f)

# 명단 루프
for li in reader_temp:
    print (li[0], li[1], li[2], li[3], li[4])  # 0:이름, 1:dd, 2:mm, 3:yy, 4:국가

    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/form/div[2]/div/div[2]/div[1]/div/div/input').send_keys(li[0])
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/form/div[2]/div/div[2]/div[2]/div/div/input[1]').send_keys(li[1])
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/form/div[2]/div/div[2]/div[2]/div/div/input[2]').send_keys(li[2])
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/form/div[2]/div/div[2]/div[2]/div/div/input[3]').send_keys(li[3])

    '''
    # 국가 선택 - 클릭만 하고, 2번 동작 수행 안 함. 액션체인으로 안 됨 
    #country_1 : Country 클릭 버튼, #country_2 : 한국 - Item 110 
    country_1 = driver.find_element(By.CLASS_NAME, 'bx--list-box__menu-icon')
    country_2 = driver.find_element(By.XPATH, '//*[@id="country__menu"]')
    country_3 = driver.find_element(By.XPATH, '//*[@id="downshift-1-item-110"]')
    ActionChains(driver).click(country_1).move_to_element(country_2).click(country_3).perform()
    '''

    # Reactive Selection page - 국가 선택
    driver.find_element(By.XPATH, "(//*[name()='svg' and @aria-label='Open menu'])[2]").click()
    option = driver.find_element(By.XPATH, "//*[text()='"+li[4]+"']")
    driver.execute_script("arguments[0].scrollIntoView();", option)
    option.click()

    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/form/div[2]/div/div[5]/div/div/div/button').click()  #검색

    time.sleep(5)

    #검색결과 리스트 화면에서, 다운로드 클릭 -> 확인 -> Search Page로 되돌아감
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div[1]/div[1]/button[4]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[3]/button[2]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div[2]/div/div[1]/div[1]/button[3]').click()
    time.sleep(1)
