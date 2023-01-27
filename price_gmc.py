from core.price import Price
from core.driver import Driver, By

def gmc_art(articles, path_to_db = None, driver = None):
    price_table = Price()
    price_table.store = 'gmc'
    if driver:
        close_driver_on_exit = False
    else:
        close_driver_on_exit = True
        driver = Driver()

    for article in articles:
        price_table.set_article(article)
        url_search = f'https://www.google.com/search?q={article}&tbm=shop'

        driver.get(url_search)

        try:
            #Load links to search result
            pages = driver.find_element(By.CLASS_NAME, 'huiPV').find_elements(By.TAG_NAME, 'a')
            pages = [e.get_attribute('href') for e in pages[:-1]]
        except Exception:
            pages = []

        bad_results_count = 0
        for page in pages:
            if bad_results_count > 100:
                break
            if 'items' in locals():
                driver.get(page)
            else: pass #1st page already load

            #Load data block
            items = driver.find_elements(By.CLASS_NAME, 'sh-dgr__content')
            for item in items:
                #All data in a tags
                a_tags = item.find_elements(By.TAG_NAME, 'a')
                
                title, price_seller = (e.text for e in a_tags[1:3])
                title = title.split('\n')[0]
                if not title: continue #Ignore promo or error block.
                if not price_table.match_article(title):
                    bad_results_count +=1
                    continue

                price_seller = price_seller.split('\n')
                price = price_seller[0]
                seller = price_seller[-1]

                link = a_tags[2].get_attribute('href').split(r'/url?url=')[-1].split('&')[0].split('%')[0]

                try:
                    price = float(price.split(' ')[0].replace(',','.'))
                except Exception:
                    price = 0.0

                price_table.add(title = title, price = price, seller = seller, url = link)

    if close_driver_on_exit:
        driver.close()
    price_table.write(path_to_db)
    return len(price_table.data)

if __name__ == '__main__':
    path_to_db = 'Price.db'
    articles = ['DH-IPC-HFW1431SP-S4']
    articles = ['DS-2CD1027G0-L(C)']
    gmc_art(articles, path_to_db)
