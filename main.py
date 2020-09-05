from bs4 import BeautifulSoup
import requests

# need to have user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
           }

r = requests.get(
    "https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1", headers=headers)
print("Status:", r.status_code)
soup = BeautifulSoup(r.text, "lxml")
results = soup.find("div", {"class": "w-blog-content other"})
links = results.findAll("div", {"class": "search_title"})
# print(soup.prettify())
# print(links)

for item in links:
    item_title = item.find("a").text
    item_href = item.find("a").attrs["href"]
    if item_title and item_href:
        print(item_title)
        print(item_href)


# print(results)
