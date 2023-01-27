from core.price import Price
from core.driver import Driver, By

def rozetka_art(articles, path_to_db = None, driver = None):
    price_table = Price()
    price_table.store = 'rozetka'
    if driver:
        close_driver_on_exit = False
    else:
        close_driver_on_exit = True
        driver = Driver()

    for article in articles:
        price_table.set_article(article)

        link_for_search = 'https://rozetka.com.ua/search/?text='+article
        driver.get(link_for_search)
        try:
            item_list = driver.find_element(By.CLASS_NAME, 'catalog-grid').find_elements(By.TAG_NAME, 'li')
            title_link_list = []
            for item in item_list:
                avail = item.find_element(By.CLASS_NAME, 'goods-tile__availability').text
                if avail in ('Есть в наличии', 'Є в наявності'):
                    title = item.find_element(By.CLASS_NAME, 'goods-tile__heading').get_attribute('title')
                    if price_table.match_article(title):
                        link = item.find_element(By.CLASS_NAME, 'goods-tile__heading').get_attribute('href')
                        title_link_list.append((title, link))

            for title, link in title_link_list:
                driver.get(link)
                price = driver.find_element(By.CLASS_NAME, 'product-prices__big').text
                price = price[:price.find('₴')].replace(' ', '')
                seller = driver.find_element(By.CLASS_NAME, 'product-seller__info').find_element(By.CLASS_NAME, 'ng-star-inserted').text
                price_table.add(title = title, price = price, seller = seller, url = link)

        except Exception as err1:
            #print('EX1', err1)
            try:
                link = driver.find_element(By.CLASS_NAME, 'tabs__list').find_elements(By.TAG_NAME, 'li')[0].find_element(By.CLASS_NAME, 'tabs__link').get_attribute('href')
                title = str(driver.find_element(By.CLASS_NAME, 'product__title').text)
                price = driver.find_element(By.CLASS_NAME, 'product-prices__big').text
                price = price[:price.find('₴')].replace(' ', '')
                seller = driver.find_element(By.CLASS_NAME, 'product-seller__info').find_element(By.CLASS_NAME, 'ng-star-inserted').text
                price_table.add(title = title, price = price, seller = seller, url = link)
            except Exception as err2:
                #print('EX2', err2)
                pass

    if close_driver_on_exit:
        driver.close()
    price_table.write(path_to_db)
    return len(price_table.data)

if __name__ == '__main__':
    path_to_db = 'Price.db'
    articles = ['DS-2CD2021G1-I']
    print(rozetka_art(articles, path_to_db))
