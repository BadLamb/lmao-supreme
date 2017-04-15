import requests
from bs4 import BeautifulSoup
import time

start = time.time()

page = "http://www.supremenewyork.com/shop/tops-sweaters/q3ns0ueyj/t79zepdlv"

# Buy item at `page`
session = requests.Session()

item = BeautifulSoup(session.get(page).text, "lxml")

sizes = item.find_all("option")[0]["value"]
style = item.find_all("input", {"id": "style"})[0]['value']
pourl = item.find_all("form")[0]["action"]

# This request is useless, the cookie is easy to recreate
session.post("http://www.supremenewyork.com" + pourl, data={
    "utf8" : "✓",
    "style": style,
    "size" : sizes,
    "commit": "add to basket",
})

#cookie = "1+item--" + sizes + "%2C" + style

checkout_page = BeautifulSoup(
    session.get("https://www.supremenewyork.com/checkout").text,
    "lxml"
)

csrf_token = checkout_page.find_all("input", {"name" : "authenticity_token"})

session.post("https://www.supremenewyork.com/checkout", data={
    "utf8" : "✓",
    "authenticity_token" : csrf_token,
    "order[billing_name]": "My Name",
    "order[email]": "a@a.com",
    "order[tel]": "+36 0123456789",
    "order[billing_address]":"lol idk 123",
    "order[billing_address_2]":"",
    "order[billing_address_3]":"",
    "order[billing_city]":"Pollo",
    "order[billing_zip]":"15365",
    "order[billing_country]":"IT",
    "same_as_billing_address":"1",
    "store_credit_id":"",
    "credit_card[type]":"visa",
    "credit_card[cnb]":"4242 4242 4242 4242",
    "credit_card[month]":"04",
    "credit_card[year]":"2017",
    "credit_card[vval]":"485",
    "order[terms]":"0",
    "order[terms]":"1",
}).text

print("Done in %ss" %(time.time() - start))
