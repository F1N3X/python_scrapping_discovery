import requests
from bs4 import BeautifulSoup
import csv

product_page_url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(product_page_url)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())

tr = soup.find_all('tr')
td = soup.find('td')
universal_product_code = td.text

title = soup.find('h1').text
print(title)

price_including_tax = tr[3]
price_including_tax = price_including_tax.find('td').text.replace('Â', '')
print(price_including_tax)

price_excluding_tax = tr[2]
price_excluding_tax = price_excluding_tax.find('td').text.replace('Â', '')
print(price_excluding_tax)

number_available = tr[5]
number_available = number_available.find('td').text
number_available = ''.join(filter(str.isdigit, number_available))
print(number_available)

product_description = soup.find_all('p')
product_description = product_description[3].text
print(product_description)

category = soup.find_all('a')
category = category[3].text
print(category)

review_rating = soup.find('p', class_='star-rating')['class'][1]
print(review_rating)


image_url = soup.find('img')['src']
image_url = 'https://books.toscrape.com/' + image_url
print(image_url)


with open('book_info.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    writer.writerow([universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])