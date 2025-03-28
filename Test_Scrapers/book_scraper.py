from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,
                         "lxml")
    books = soup.find_all("article",
                          class_="product_pod")
    data = []

    for book in books:

        item = {}

        item["Title"] = book.find("img",
                                  class_="thumbnail").attrs["alt"]
        item["Price"] = book.find("p",
                                  class_="price_color").text[1:]
        data.append(item)
    return data

def export_data(data):
    df = pd.DataFrame(data)
    df.to_excel("books.xlsx")
    df.to_csv("books.csv")

if __name__ == "__main__":
    data = get_data('https://books.toscrape.com/')
    export_data(data)
    print("Done.")