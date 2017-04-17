import requests, time, telepot, datetime, pause
from pytz import timezone
from dateutil import tz

to_buy = []

keyword = "truth"
fsize = "large"
color = "red"
uid = 174865824

user_agent = "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92"

# Set up telegram bot
bot = telepot.Bot("")

start = time.time()
session = requests.Session()

# Wait till 10 minutes before a drop
drop_time = timezone('Europe/London').localize(
    datetime.datetime.strptime("20/04/2017 10:57", "%d/%m/%Y %H:%M")
)

print(drop_time.astimezone(tz.tzlocal()))

pause.until(drop_time.astimezone(tz.tzlocal()))

while len(to_buy) == 0:

    # Find things to buy
    resp = session.get("http://supremenewyork.com/mobile_stock.json",headers={
        "User-agent" : user_agent
        }).json()['products_and_categories']

    # Flatten arrays
    flattened_items = [h for i in resp for h in resp[i]]

    # Remove duplicates
    known_names = []
    items = []

    for i in flattened_items:
        if not i['name'] in known_names:
            items.append(i)
            known_names.append(i['name'])

    to_buy = [i for i in items if keyword in i['name'].lower()]

    if len(to_buy) == 0:
        print("Nothing yet")
        time.sleep(1)

for item in to_buy:
    # Get product info
    product_page = session.get(
        "http://supremenewyork.com/shop/%d.json" %(item['id']),
        headers={
            "User-agent" : user_agent
        }
    ).json()

    # Find size and style
    style = {}
    for s in product_page['styles']:
        if s['name'].lower() in color.lower():
            style = s

    size = 0
    for s in style['sizes']:
        if s['name'].lower() == fsize.lower() and s['stock_level'] > 0:
            size = s['id']

    # Add to cart
    add_to_cart = session.post(
        "http://www.supremenewyork.com/shop/%d/add.json" %(item['id']),
        data={"style" : style['id'], "size":size, "qty":"1"},
        headers={ "User-agent" : user_agent }
    )

# Checkout
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
    "g-recaptcha-response" : "no",
    "is_from_ios_native" : "1",
}

response = session.post("https://www.supremenewyork.com/checkout.json", data=params, headers={
    "User-agent" : user_agent
}).text
took = time.time() - start


bot.sendMessage(uid, "%s in %ss" %(response, took))
