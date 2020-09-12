import requests
from bs4 import BeautifulSoup

url = "https://jolse.com"
result = requests.get(url)

bs_obj = BeautifulSoup(result.content, "html.parser")
print (bs_obj)

