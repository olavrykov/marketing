from core.price import Price
from core.driver import Driver, By

import re

def hotline_art(articles, path_to_db = None, driver = None):
    price_table = Price()
    price_table.store = 'hotline'
    if driver:
        close_driver_on_exit = False
    else:
        close_driver_on_exit = True
        driver = Driver()

    for article in articles:
        price_table.set_article(article)
        url = 'https://hotline.ua/sr/?q=' + article
        driver.get(url)

        #Search last page number
        last_page_num = 1
        try:
            pages = driver.find_elements(By.CLASS_NAME, 'page')
        except Exception as err:
            pages = []
        for e in reversed(pages):
            if e.text.isnumeric():
                last_page_num = int(e.text)
                break

        #Cycle for All search pages results.
        for page in range(1, last_page_num + 1):
            if page == 1:
                pass #1st page already load
            else:
                driver.get(f'{url}&p={page}')

            items = driver.find_elements(By.CLASS_NAME, 'list-item')

            #Generate links
            title_link_list = []
            for item in items:
                title = item.find_elements(By.CLASS_NAME, 'list-item__title')
                if title: title = title[0].text
                else: continue
                link = item.find_elements(By.TAG_NAME, 'a')
                if link: link = link[0].get_attribute('href')
                else: continue
                if price_table.match_article(title):
                    title_link_list.append((title, link))

            #Pass thwough links
            for title, link in title_link_list:
                driver.get(f'{link}?tab=prices')

                items = driver.find_elements(By.CLASS_NAME, 'list__item')

                for item in items:
                    seller = item.find_elements(By.CLASS_NAME, 'shop__title')
                    if seller: seller = seller[0].text
                    else: continue
                    price = item.find_elements(By.CLASS_NAME, 'price__value')
                    if price: price = price[0].text
                    else: continue
                    price = price.replace(' ', '')
                    link = item.find_elements(By.TAG_NAME, 'a')
                    if link: link = link[0].get_attribute('href')
                    else: continue
                    if seller:
                        price_table.add(title = title, price = price, seller = seller, url = link)

    if close_driver_on_exit:
        driver.close()
    price_table.write(path_to_db)
    return len(price_table.data)

if __name__ == '__main__':
    path_to_db = 'Price.db'
    articles = ['DH-IPC-HFW1431SP-S4', 'DH-IPC-HFW1431SP', 'DH-IPC-HFW', 'DH-IPC']
    hotline_art(articles, path_to_db)
