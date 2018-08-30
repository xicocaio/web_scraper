from urllib.request import urlopen
from bs4 import BeautifulSoup
import os.path
import csv
import traceback
from datetime import date, datetime
import shutil
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# generate htmls temp folder name for storing htmls
def generate_folder_name(website_name='olx', prefix='sp', name=date.today()):
    folder_name = BASE_DIR + '/data/{}-{}-{}'.format(website_name, prefix, name)
    return folder_name


# downloads olx product htmls once a day, for a given Brazil state
def download_htmls(source_url=None, dest_folder=None, next_page_html_tag='li', next_page_html_class='item next'):
    page_number = 1

    # if folder already exists, there is no need to download htmls again
    if dest_folder and not os.path.isdir(dest_folder):
        os.makedirs(dest_folder)
        print('--- Starting webpages download ---\n')

        # goes through all pages of that product for that state
        while source_url:
            try:
                # getting the html
                web_page = urlopen(source_url)

                # parsing html
                soup = BeautifulSoup(web_page, 'html.parser')

                input_fname = dest_folder + '/page-{}.html'.format(page_number)
                with open(input_fname, "w") as file:
                    file.write(str(soup))

                print('Page {} finished'.format(page_number))

            except Exception as e:
                print('Something went wrong with the downloads')
                print("type error: " + str(e))
                print(traceback.format_exc())

                # remove the download folder if something went wrong with any of the downloads
                # this guarantees data consistency and let the program try again letter
                shutil.rmtree(dest_folder)

            # getting next page url
            source_url = soup.find(next_page_html_tag, next_page_html_class)
            if source_url:
                source_url = source_url.a.get('href')
                page_number += 1
            else:
                break

        print('\n--- Webpages download finished successfully ---')

    else:
        print('--- Webpages already downloaded today, continuing to data extraction ---')


# generate csv files from the htmls, for a given Brazil state
def generate_iphone8_olx_csv(date=date.today(), company='olx', state='sp', dest_folder=None, out_path=None):
    print('\n--- Starting extraction of data to CSV ---\n')

    html_files = glob.glob('{}/*.html'.format(dest_folder))

    if len(html_files) > 0:
        with open(out_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['id', 'date', 'company', 'state', 'city', 'title', 'price'])

    for in_filename in html_files:
        print('File {} extraction starting'.format(in_filename))
        soup = BeautifulSoup(open(in_filename), 'html.parser')

        products = soup.find_all('a', 'OLXad-list-link')
        warning_for_file = False

        for p in products:
            try:
                # preparing data for csv by getting raw text and:
                # extracting integer
                id = int(p.get('id').strip())

                # removing special chars
                title = p.find('h2', 'OLXad-list-title mb5px').text.strip().lower().replace(',', ' ').replace('"', '')

                # extracting integer
                price = int(p.find('p', 'OLXad-list-price').text.strip().split('R$ ')[1].replace('.', ''))

                # extracting city name
                city = p.find('p', 'text detail-region').text.strip().split('-')[0].split(',')[0].strip()

            except Exception as e:
                if not warning_for_file:
                    print('Warning: Some of the items downloaded in this file have missing data')
                warning_for_file = True
                continue

            # checking that all fields are present and that it is an iphone 8 that costs at least 1000
            if not id or not title or not price or not city or '8' not in title or 'x' in title or price < 1000:
                continue

            # only save to file if there is no missing data
            with open(out_path, 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([id, date, company, state, city, title, price])

        print('File {} extraction finished\n '.format(in_filename))

    for in_filename in glob.glob('{}/*.html'.format(dest_folder)):
        os.remove(in_filename)
    print('Downloaded files removed\n')

    print('--- Data extraction finished ---\n')


def scrap_olx_iphone8():
    state = 'sp'
    product_path = 'celulares/iphone/novo?q=iphone+8&sr=1'
    source_url = 'https://{}.olx.com.br/{}'.format(state, product_path)
    today = date.today()
    state = 'sp'
    company = 'olx'
    dest_folder = generate_folder_name(company, state, today)
    out_path = '{}/{}'.format(dest_folder, 'products.csv')

    next_page_html_tag = 'li'
    next_page_html_class = 'item next'
    download_htmls(source_url, dest_folder, next_page_html_tag, next_page_html_class)
    generate_iphone8_olx_csv(today, company, state, dest_folder, out_path)

    return out_path
