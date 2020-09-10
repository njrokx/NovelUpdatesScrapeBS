from bs4 import BeautifulSoup
import requests
from ln_info import getLNData
from pymongo import MongoClient
import time
import random
from pprint import pprint

client = MongoClient(
    "mongodb://jock:Th1s1sAStr0ngPassw0rd@localhost:27017/admin?authSource=admin")
db = client.LNDB
# need to have user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
           }
url = 'https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1&pg=1'


def delay():
    print("running delay.\n")
    time.sleep(random.uniform(15, 20))


i = 1
while i < 2:
    print("Current page url:", url)
    r = requests.get(url, headers=headers)

    print("\nStatus:", r.status_code)
    print("Page:", i)
    soup = BeautifulSoup(r.text, "lxml")
    results = soup.find("div", {"class": "w-blog-content other"})
    links = results.find_all("div", {"class": "search_main_box_nu"})
    # print(soup.prettify())
    # print(links)

    for item in links:
        item_title = item.find("a").text
        item_href = item.find("a").attrs["href"]
        item_lang = item.find("span").text

        if item_title and item_href and item_lang:
            if item_lang == 'JP':
                print("\nTitle:", item_title)
                print("Link:", item_href)
                print("Original Language:", item_lang)

                data = getLNData(item_href, headers, item_title)
                cursor = db.inventory.find({"Title": item_title})

                # can use cursor.count() to get number of docs that matches the find()
                curlist = list(cursor)
                if len(curlist) == 0:
                    db.inventory.insert_one(data)
                    pprint(data)
                    print("added data")
                else:
                    db.inventory.update_one(
                        {"Title": item_title}, {"$set": data})
                    print("updated data")
    try:
        pages = soup.find("div", {"class": "digg_pagination"}).find(
            "a", {"class": "next_page"}).attrs["href"]
        url = "https:"+pages
        print("\nNext Page url:", url)
    except:
        print("No next page.")

    i += 1
    delay()


# db path for running the mongodb server\
