import requests
from pprint import pprint

user_agent = "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92"
session = requests.Session()

def buy_product(json):
    text = session.get(
        "http://supremenewyork.com/shop/%d.json" %(json['id']),
        headers={
            "User-agent" : user_agent
        }
    ).json()

    style = text['styles'][0]
    size = text['styles'][0]['sizes'][0]

    print(session.post(
        "http://www.supremenewyork.com/shop/%d/add.json" %(json['id']),
        data={"size":size['id'], "style":style['id'], "qty":"1"},
        headers={
            "User-agent" : user_agent
        }
    ).text)

    # TODO Style selction algo

    params = {
        "from_mobile" : "1",
        "same_as_billing_address" : "1",
        "order[billing_name]" : "A b",
        "order[email]" : "a@b.com",
        "order[tel]" : "0418485923",
        "order[billing_address]" : "Jggj khbhkb 78",
        "order[billing_city]" : "Hbkhb",
        "order[billing_state]" : "",
        "order[billing_zip]" : "47869",
        "order[billing_country]" : "FI",
        "credit_card[type]" : "visa",
        "credit_card[cnb]" : "4242 4242 4242 4242",
        "credit_card[month]" : "06",
        "credit_card[year]" : "2017",
        "credit_card[vval]" : "456",
        "order[terms]" : "1",
        "order[terms]" : "1",
        "g-recaptcha-response" : "no",
        "is_from_ios_native" : "1",
        }

    x = session.post("https://www.supremenewyork.com/checkout.json", data=params, headers={
        "User-agent" : user_agent
    }).text

    print (x)

wanted_product = ["Supreme®/Duralex® Glasses (Set of 4)",
                  "Supreme Truth Tour Jacket"]

items = session.get("http://supremenewyork.com/mobile_stock.json",
    headers={
        "User-agent" : user_agent
    }).json()

for i in items["products_and_categories"]:
    for h in items["products_and_categories"][i]:
        if h["name"] in wanted_product:
            buy_product(h)
