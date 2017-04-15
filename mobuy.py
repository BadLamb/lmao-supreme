import requests
from pprint import pprint

user_agent = "Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92"
keyword = "knit"

session = requests.Session()

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

for i in items:
    if keyword.lower() in i['name'].lower():
        print(i)

#print(items)
