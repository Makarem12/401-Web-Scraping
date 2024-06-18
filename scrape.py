import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website
base_url = 'https://books.toscrape.com/'

# Fetch the main page content
main_page = requests.get(base_url)
main_soup = BeautifulSoup(main_page.content, 'html.parser')

# Find the ul element with the class 'nav nav-list'
all_books_ul = main_soup.find('ul', class_='nav nav-list')

# Find all li elements inside the all-books ul element
li_elements = all_books_ul.find_all('li')

def get_books_data(category_name):
    # Extract the category page link
    category_link = None
    for li in li_elements:
        a_tag = li.find('a')
        if a_tag and category_name in a_tag.get_text(strip=True):
            category_link = a_tag['href']
            break

    if category_link:
        # Build the full URL for the category link
        category_url = base_url + category_link

        # Fetch the category page content
        category_page = requests.get(category_url)
        category_soup = BeautifulSoup(category_page.content, 'html.parser')

        # Find all books in the category
        books_ol = category_soup.find('ol', class_='row')
        book_elements = books_ol.find_all('li')

        books_data = []

        for book in book_elements:
            book_info = {}

            # Title
            title_tag = book.find('h3').find('a')
            if title_tag:
                book_info['title'] = title_tag['title']

            # Rating
            rating_tag = book.find('p', class_='star-rating')
            if rating_tag:
                book_info['rating'] = rating_tag['class'][1]

            # Price
            price_tag = book.find('p', class_='price_color')
            if price_tag:
                book_info['price'] = price_tag.get_text()

            # Availability
            availability_tag = book.find('p', class_='instock availability')
            if availability_tag:
                book_info['availability'] = availability_tag.get_text(strip=True)

            books_data.append(book_info)

        return books_data
    else:
        print(f"{category_name} link not found")
        return []

# Get books data for Travel category
travel_books_data = get_books_data("Travel")

# Get books data for Mystery category
mystery_books_data = get_books_data("Mystery")

# Get books data for Fiction category
fiction_books_data = get_books_data("Fiction")

# Combine all data into a single dictionary
all_books_data = {
    "Travel": travel_books_data,
    "Mystery": mystery_books_data,
    "Historical Fiction": fiction_books_data
}

# Write the combined data to a JSON file
with open("book_api.json", "w") as json_file:
    json.dump(all_books_data, json_file, indent=2)

# Print confirmation message
print("Books data has been written to book_data.json")
