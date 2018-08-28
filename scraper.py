from urllib.request import urlopen
from bs4 import BeautifulSoup
import os.path
import csv
from datetime import date

today = date.today()
input_fname = str(today) + '.html'
output_fname = str(today) + '.csv'

if not os.path.isfile(input_fname):
    quote_page = 'https://sp.olx.com.br/celulares/iphone/novo?o=1&q=iphone+8+plus+64gb&sr=1'

    # getting the html
    page = urlopen(quote_page)

    # parsing html
    soup = BeautifulSoup(page, 'html.parser')

    with open(input_fname, "w") as file:
        file.write(str(soup))

soup = BeautifulSoup(open(input_fname), 'html.parser')


# name_box = soup.find_all(['p', 'h2'], attrs={'class':['OLXad-list-title mb5px', 'OLXad-list-price', 'text detail-region']})

products = soup.find_all('a', 'OLXad-list-link')

with open(output_fname, 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['date', 'title', 'price', 'city'])

for p in products:

    # preparing data for csv:
    #
    title = p.find('h2', 'OLXad-list-title mb5px').text.strip().lower().replace(',', ' ').replace('"', '')
    price = int(p.find('p', 'OLXad-list-price').text.strip().split('R$ ')[1].replace('.', ''))
    city = p.find('p', 'text detail-region').text.strip().split('-')[0].split(',')[0].strip()

    if not title or not price or not city or '8' not in title:
        continue

    with open(output_fname, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([today, title, price, city])
