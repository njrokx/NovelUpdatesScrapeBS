from bs4 import BeautifulSoup
import requests

lnartist = []
lnauthor = []
lnopub = []


def getLNData(url, headers, title):
    # need to clear the list for the next entry
    lnartist.clear()
    lnauthor.clear()
    lnopub.clear()

    link_r = requests.get(url, headers=headers)
    print("\nStatus:", link_r.status_code)
    link_soup = BeautifulSoup(link_r.text, "lxml")
    link_result = link_soup.find(
        "div", {"class": "g-cols wpb_row offset_default"})
    link_data = link_result.find_all("div", {"class": "one-third"})
    # use .replace("\n"," ") instead of strip to prevent no spacing in case of two artist/author/publishers
    for data in link_data:
        try:
            data_type = data.find("a", {"class": "genre type"}).text
        except:
            data_type = "Unknown"
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

    for authors in data_author:
        author = authors.text
        lnauthor.append(author)
    for artists in data_artist:
        artist = artists.text
        lnartist.append(artist)
    for opubs in data_ori_pub:
        opub = opubs.text
        lnopub.append(opub)
    data = {"Title": title,
            "Type": data_type,
            "Author(s)": lnauthor,
            "Artist(s)": lnartist,
            "Licensed": data_licensed,
            "Completely Translated": data_comp_tl,
            "Original Publisher(s)": lnopub,
            "English Publisher": data_eng_pub,
            "Status in COO": data_statuscoo}
    return data
