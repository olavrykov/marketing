import re

from core.price import Price
from core.driver import Driver, By

def prom_art(articles, path_to_db = None, driver = None):
    price_table = Price()
    price_table.store = 'prom'
    if driver:
        close_driver_on_exit = False
    else:
        close_driver_on_exit = True
        driver = Driver()

    for article in articles:
        price_table.set_article(article)
        for page_counter in range(1, 4):
            url = f'https://prom.ua/search?search_term={article}&exact_match=true&binary_filters=presence_available&page={page_counter}'
            driver.get(url)

            list_of_item = driver.find_elements(By.CLASS_NAME, 'js-productad')
            for item in list_of_item:
                #find_elements(By.XPATH Dont work correctly there. Use re
                price = re.findall(r'product_price".*?price="(.*?)"', item.get_attribute('outerHTML'))
                if price:
                    price = price[0]
                else:
                    #ignore priceless records
                    continue

                a_tags = item.find_elements(By.TAG_NAME, 'a')
                if not a_tags: continue
                link = a_tags[0].get_attribute('href')
                link = link.split('?')[0]
                title = a_tags[0].get_attribute('title')
                seller = a_tags[-1].get_attribute('title')

                if not title: continue
                if not price_table.match_article(title): continue

                price_table.add(title = title, price = price, seller = seller, url = link)

    if close_driver_on_exit:
        driver.close()
    price_table.write(path_to_db)
    return len(price_table.data)

if __name__ == '__main__':
    path_to_db = 'Price.db'
    articles = ['DH-IPC-HFW1431SP-S4']
    articles = ['DS-2CD1021-I(F)']
    prom_art(articles, path_to_db)
