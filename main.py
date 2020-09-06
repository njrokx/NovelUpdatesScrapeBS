from bs4 import BeautifulSoup
import requests
# need to have user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
           }

r = requests.get(
    "https://www.novelupdates.com/novelslisting/?sort=7&order=1&status=1", headers=headers)
print("\nStatus:", r.status_code)
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
            link_r = requests.get(item_href, headers=headers)
            print("\nStatus:", link_r.status_code)

            link_soup = BeautifulSoup(link_r.text, "lxml")
            link_result = link_soup.find(
                "div", {"class": "g-cols wpb_row offset_default"})
            link_data = link_result.find_all("div", {"class": "one-third"})

            # use .replace("\n"," ") instead of strip to prevent no spacing in case of two artist/author/publishers
            for data in link_data:
                data_type = data.find("a", {"class": "genre type"}).text
                data_author = data.find("a", {"id": "authtag"}).text
                data_artist = data.find(
                    "div", {"id": "showartists"}).text.strip()
                data_licensed = data.find(
                    "div", {"id": "showlicensed"}).text.strip()
                data_comp_tl = data.find(
                    "div", {"id": "showtranslated"}).text.strip()
                data_ori_pub = data.find("a", {"id": "myopub"}).text
                data_eng_pub = data.find(
                    "div", {"id": "showepublisher"}).text.strip()
                data_statuscoo = data.find(
                    "div", {"id": "editstatus"}).text.strip()
                print("\nType:", data_type)
                print("Author(s):", data_author)
                print("Artist(s):", data_artist)
                print("Licensed:", data_licensed)
                print("Completely Translated:", data_comp_tl)
                print("Original Publisher:", data_ori_pub)
                print("English Publisher:", data_eng_pub)
                print("Status in COO:", data_statuscoo)
        else:
            print("Not a Japanese Light Novel.\n")


# item_title = links[0].find("a").text
# item_href = links[0].find("a").attrs["href"]
# item_lang = links[0].find("span").text
# if item_title and item_href:
#     print("Title:", item_title)
#     print("Link:", item_href)
#     print("Original Language:", item_lang)
#     link_r = requests.get(item_href, headers=headers)

#     print("Status:", link_r.status_code)
#     link_soup = BeautifulSoup(link_r.text, 'lxml')
#     link_result = link_soup.find(
#         "div", {"class": "g-cols wpb_row offset_default"})
#     link_data = link_result.find_all("div", {"class": "one-third"})

#     for data in link_data:
#         data_type = data.find("a", {"class": "genre type"}).text
#         data_author = data.find("a", {"id": "authtag"}).text
#         data_artist = data.find("div", {"id": "showartists"}).text.strip('\n')
#         data_licensed = data.find("div", {"id": "showlicensed"}).text.strip()
#         data_comp_tl = data.find("div", {"id": "showtranslated"}).text.strip()
#         data_ori_pub = data.find("a", {"id": "myopub"}).text
#         data_eng_pub = data.find("div", {"id": "showepublisher"}).text.strip()
#         data_statuscoo = data.find("div", {"id": "editstatus"}).text.strip()
#         print("Type:", data_type)
#         print("Author(s):", data_author)
#         print("Artist(s):", data_artist)
#         print("Licensed:", data_licensed)
#         print("Completely Translated:", data_comp_tl)
#         print("Original Publisher:", data_ori_pub)
#         print("English Publisher:", data_eng_pub)
#         print("Status in COO:", data_statuscoo)

#     if item_lang != 'JP':
#         print("not Japanese")
