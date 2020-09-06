from bs4 import BeautifulSoup
import requests

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
#            }


def getLNData(url, headers):
    link_r = requests.get(url, headers=headers)
    print("\nStatus:", link_r.status_code)
    link_soup = BeautifulSoup(link_r.text, "lxml")
    link_result = link_soup.find(
        "div", {"class": "g-cols wpb_row offset_default"})
    link_data = link_result.find_all("div", {"class": "one-third"})
    # use .replace("\n"," ") instead of strip to prevent no spacing in case of two artist/author/publishers
    for data in link_data:
        data_type = data.find("a", {"class": "genre type"}).text
        data_author = data.find("div", {"id": "showauthors"}).findAll("a")
        data_artist = data.find(
            "div", {"id": "showartists"}).findAll("a")
        data_licensed = data.find(
            "div", {"id": "showlicensed"}).text.strip()
        data_comp_tl = data.find(
            "div", {"id": "showtranslated"}).text.strip()
        data_ori_pub = data.find("div", {"id": "showopublisher"}).findAll("a")
        data_eng_pub = data.find(
            "div", {"id": "showepublisher"}).text.strip()
        data_statuscoo = data.find(
            "div", {"id": "editstatus"}).text.strip()
        print("\nType:", data_type)
        if len(data_author) > 1:
            print("Author(s):")
            for authors in data_author:
                author = authors.text
                print(author, " ")
        if len(data_artist) > 1:
            print("Artist(s):")
            for artists in data_artist:
                artist = artists.text
                print(artist, " ")
        print("Licensed:", data_licensed)
        print("Completely Translated:", data_comp_tl)
        if len(data_ori_pub) > 1:
            print("Original Publisher(s):")
            for opubs in data_ori_pub:
                opub = opubs.text
                print(opub, " ")
        print("English Publisher:", data_eng_pub)
        print("Status in COO:", data_statuscoo)


# getLNData('https://www.novelupdates.com/series/100-things-i-dont-know-about-my-senior/', headers)
