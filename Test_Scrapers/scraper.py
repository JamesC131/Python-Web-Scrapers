import requests
from bs4 import BeautifulSoup
import csv

# METHODS OF PARSING DATA

# get all elements with an h1 tag:
# h1_elements = soup.find_all('h1')

# get the element with id="main-title"
# main_title_element = soup.find(id='main-title')

# find the footer element
# based on the text it contains
# footer_element = soup.find(text={'Powered by WordPress'})

# find the email input element
# through its "name" attribute
# email_element = soup.find(attrs={'name': 'email'})

# find all the centered elements
# on the page
# centered_element = soup.find_all(class_='text-center')

# these requests can be concatenated
# get all "li" elements
# in the ".navbar" element
# soup.find(class_='navbar').find_all('li')

# Simpler request concatenation using CSS selectors
# get all "li" elements
# in the ".navbar" element
# soup.select('.navbar > li')

def scrape_page(soup, quotes):
    # retrieving all the quote <div> HTML element on the page
    quote_elements = soup.find_all('div', class_='quote')

    # iterating over the list of quote elements
    # to extract the data of interest and store it
    # in quotes
    for quote_element in quote_elements:
        # extracting the text of the quote
        text = quote_element.find('span', class_='text').text
        # extracting the author of the quote
        author = quote_element.find('small', class_='author').text

        # extracting the tag <a> HTML elements related to the quote
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

        # storing the list of tag strings in a list
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        # appending a dictionary containing the quote data
        # in a new format in the quote list
        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)  # merging the tags into a "A, B, ..., Z" string
            }
        )

#Use a crawler to navigate and scrape every page on the website
# the URL of the home page of the target website
base_url = 'https://quotes.toscrape.com'

#informs the server what type of OS, browser, and device is being used
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

#targets the website which we will extract data from
page = requests.get('https://quotes.toscrape.com', headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')
# retrieve the page and initializing soup...
quotes = []

scrape_page(soup, quotes)

# get the "Next →" HTML element
next_li_element = soup.find('li', class_='next')

# if there is a next page to scrape
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # get the new page
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    # parse the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_page(soup, quotes)

    # look for the "Next →" HTML element in the new page
    next_li_element = soup.find('li', class_='next')

    #Extract the info into a CSV file

    # reading  the "quotes.csv" file and creating it
    # if not present
    csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')

    # initializing the writer object to insert data
    # in the CSV file
    writer = csv.writer(csv_file)

    # writing the header of the CSV file
    writer.writerow(['Text', 'Author', 'Tags'])

    # writing each row of the CSV
    for quote in quotes:
        writer.writerow(quote.values())

    # terminating the operation and releasing the resources
    csv_file.close()