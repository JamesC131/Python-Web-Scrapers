import requests
import bs4
import time
from tkinter import messagebox

while True:
    Macbook = requests.get("https://www.amazon.com/Apple-2023-MacBook-Laptop-chip/dp/B0C75ZRQLB/ref=sr_1_2_sspa?crid=1JGR6IBON1RXL&keywords=macbook&qid=1705931206&sprefix=mac%2Caps%2C102&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1")
    soup = bs4.BeautifulSoup(Macbook.text, 'lxml')
    price = soup.find("span", class_="a-price-whole").text[1:]
    print(price)
    prices = []
    prices.append(price)
    print(prices)
    time.sleep(10)
