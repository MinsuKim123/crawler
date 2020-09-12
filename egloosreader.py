import requests
from bs4 import BeautifulSoup

#Read the last content's address

url = "http://coldstar.egloos.com/"
result = requests.get(url)
bs_obj = BeautifulSoup (result.content, "html.parser")

firsturl = bs_obj.findAll({"class":"post_info_link"})
# lf_items = bs_obj.findAll("div", {"class":"lf-item"})
#hrefs = [div.find("a")['href'] for div in lf_items ]

print (firsturl)

#print (hrefs[10:])
