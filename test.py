from ln_info import getLNData
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pprint import pprint

client = MongoClient(
    "mongodb://jock:Th1s1sAStr0ngPassw0rd@localhost:27017/admin?authSource=admin")
db = client.LNDB
genres = []
# need to have user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
           }
url = 'https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1&pg=1'

r = requests.get(url, headers=headers)

print("\nStatus:", r.status_code)

soup = BeautifulSoup(r.text, "lxml")
results = soup.find("div", {"class": "w-blog-content other"})
links = results.find_all("div", {"class": "search_main_box_nu"})

# url = 'https://www.novelupdates.com/series/do-you-know-the-limits/'

item_title = links[1].find("a").text
item_href = links[1].find("a").attrs["href"]
item_lang = links[1].find("span").text
item_genres = links[1].find("div", {"class": "search_genre"}).findAll("a")
# data.find("div", {"id": "showauthors"}).findAll("a")
if item_title and item_href:
    print("Title:", item_title)
    print("Link:", item_href)
    print("Original Language:", item_lang)
    for genre in item_genres:
        data_genre = genre.text
        genres.append(data_genre)
    # data = getLNData(item_href, headers, item_title)
    # cursor = db.inventory.find({"Title": item_title})
    print(genres)
    db.inventory.update_one({"Title": item_title}, {
                            "$set": {"Genres": genres, "url": item_href}})
    item = db.inventory.find({"Title": item_title})
    for data in item:
        pprint(data)
    # # can use cursor.count() to get number of docs that matches the find()
    # curlist = list(cursor)
    # if len(curlist) == 0:
    #     db.inventory.insert_one(data)
    #     print("added data")
    # else:
    #     db.inventory.update_one({"Title": item_title}, {"$set": data})
    #     print("updated data")

    # if item_lang != 'JP':
    #     print("not Japanese")
