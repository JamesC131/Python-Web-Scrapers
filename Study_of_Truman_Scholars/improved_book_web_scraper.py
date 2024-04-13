import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data(soup, data):
    winners = soup.find_all("article", class_="directory-entry")

    for winner in winners:
        item = {}
        try:
            item["Name"] = winner.find("h3", class_="directory-entry__title").text
        except:
            item["Name"] = 'N/A'
        try:
            item["Institution"] = winner.find_all(class_="field__content")[-1].text
        except:
            item["Institution"] = 'N/A'
        data.append(item)


base_url = 'https://www.truman.gov/meet-our-scholars/scholar-listing'

page = requests.get(base_url)

data = []

soup = BeautifulSoup(page.text, 'html.parser')

get_data(soup, data)

next_li_element = soup.find('li', class_="pager__item pager__item--next")

while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', class_="pager__link pager__link--next", href=True)['href']

    # getting the new page
    page = requests.get(base_url + next_page_relative_url)

    # parsing the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    # scraping the new page
    get_data(soup, data)

    # looking for the "Next →" HTML element in the new page
    next_li_element = soup.find('li', class_='pager__item pager__item--next')


def export_data(data):
    df = pd.DataFrame(data)
    df.to_excel("winners.xlsx")
    df.to_csv("winners.csv")


if __name__ == "__main__":
    export_data(data)
    print("Done.")
