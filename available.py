import requests
from bs4 import BeautifulSoup
from time import sleep

def get_products():
    raw_html = requests.get("http://www.supremenewyork.com/shop/all").text
    articles = BeautifulSoup(raw_html, "html.parser").find_all("article")

    available = []

    for i in articles:
        if len(i.find_all("div", "sold_out_tag")) == 0:
            available.append(i.find_all("a")[0]["href"])
    
    return available

print '\n'.join(get_products())