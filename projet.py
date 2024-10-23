import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil

image_folder = 'book_images'
if os.path.exists(image_folder):
    shutil.rmtree(image_folder)
os.makedirs(image_folder)



def clean_title(title):
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- "
    new_title = ''
    new_count = 0
    for i in range(len(title)):
        if title[i] in valid_chars:
            new_title += title[i]
            new_count += 1
        else:
            if len(new_title) > new_count+1 and new_title[new_count + 1] in valid_chars:
                new_title += '_'
                new_count += 1
    return new_title



def book_explorer(url, category_folder):
    product_page_url = url

    response = requests.get(product_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())

    tr = soup.find_all('tr')
    td = soup.find('td')
    universal_product_code = td.text

    title = soup.find('h1').text
    title = clean_title(title)
    # print(title)

    price_including_tax = tr[3]
    price_including_tax = price_including_tax.find('td').text.replace('Â', '')
    # print(price_including_tax)

    price_excluding_tax = tr[2]
    price_excluding_tax = price_excluding_tax.find('td').text.replace('Â', '')
    # print(price_excluding_tax)

    number_available = tr[5]
    number_available = number_available.find('td').text
    number_available = ''.join(filter(str.isdigit, number_available))
    # print(number_available)

    product_description = soup.find_all('p')
    product_description = product_description[3].text
    # print(product_description)

    category = soup.find_all('a')
    category = category[3].text
    # print(category)

    review_rating = soup.find('p', class_='star-rating')['class'][1]
    # print(review_rating)


    image_url = soup.find('img')['src']
    image_url = 'https://books.toscrape.com/' + image_url
    # print(image_url)

    image_response = requests.get(image_url)
    image_name = f"{title.replace('/', '_').replace(' ', '_').replace("'", "_")}.jpg"  # Nommer l'image avec le titre du livre
    image_path = os.path.join("book_images/" + category_folder, image_name)

    with open(image_path, 'wb') as image_file:
        image_file.write(image_response.content)


    return (universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url)






def get_datas(url, category):
    category_page = requests.get(url)
    soup = BeautifulSoup(category_page.text, 'html.parser')

    books = soup.find_all('h3')
    print("-------------------------------------------------")
    print("Category : " + category)
    print("-------------------------------------------------")
    # print(books)
    csv_file_path = os.path.join('csv_files', f'{category}.csv')
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for el in books:
            url_books = 'https://books.toscrape.com/catalogue/' + el.find('a')['href']
            url_books = url_books.replace('../', '')
            # print(url_books)
            datas = book_explorer(url_books, category)
            writer.writerow([datas[0], datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7], datas[8]])
    try :
        next_page = soup.find('li', class_='next')
        next_page = next_page.find('a')['href']
        print("on change de page")
        print("Nouvelle page : " + category_url + next_page)
        print("-------------------------------------------------")
        get_datas(category_url + next_page, category)
    except:
        return





def make_csv(category):
    csv_folder = 'csv_files'

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    csv_file_path = os.path.join(csv_folder, f'{category}.csv')
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])





def get_categories(url):
    global category_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find_all('ul')[1]
    categories = categories.find_all('a')
    categories = categories[1:]
    csv_folder = 'csv_files'
    if os.path.exists(csv_folder):
        shutil.rmtree(csv_folder)
    os.makedirs(csv_folder)
    for category in categories:
        category_url = 'https://books.toscrape.com/' + category['href']
        print("Catégorie url : " + category_url)
        category_url = category_url.replace('index.html', '')
        category_name = category.text.strip()
        category_name = category_name.replace(' ', '_')

        category_folder = os.path.join(image_folder, category_name)
        if os.path.exists(category_folder):
            shutil.rmtree(category_folder)
        os.makedirs(category_folder)

        print(category_name)
        make_csv(category_name)
        get_datas(category_url, category_name)

get_categories('https://books.toscrape.com/index.html')
category_url = ""