from bs4 import BeautifulSoup
import requests
from ln_info import getLNData
from pymongo import MongoClient

client = MongoClient(
    "mongodb://jock:Th1s1sAStr0ngPassw0rd@localhost:27017/admin?authSource=admin")
db = client.LNDB
# need to have user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
           }
url = 'https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1&pg=1'


i = 1
while i < 10:
    r = requests.get(url, headers=headers)

    print("\nStatus:", r.status_code)
    print("Page:", i)
    soup = BeautifulSoup(r.text, "lxml")
    results = soup.find("div", {"class": "w-blog-content other"})
    links = results.find_all("div", {"class": "search_main_box_nu"})
    # print(soup.prettify())
    # print(links)
    try:
        pages = soup.find("div", {"class": "digg_pagination"}).find(
            "a", {"class": "next_page"}).attrs["href"]
        print("https:" + pages)
        url = "https:"+pages
    except:
        print("No next page.")

    i += 1
# db path for running the mongodb server

# for item in links:
#     item_title = item.find("a").text
#     item_href = item.find("a").attrs["href"]
#     item_lang = item.find("span").text

#     if item_title and item_href and item_lang:
#         if item_lang == 'JP':
#             print("\nTitle:", item_title)
#             print("Link:", item_href)
#             print("Original Language:", item_lang)

#             getLNData(item_href, headers)
#         else:
#             print("\nNot a Japanese Light Novel.\n")
