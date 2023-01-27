import re
import json
import extruct
from urllib.parse import urlsplit
from core.price import Price
from core.driver import Driver, By

def common_schema(data):
    title = ''
    price = 0
    metadata = extruct.extract(data, uniform=True, syntaxes=['json-ld', 'microdata', 'opengraph'])
    rez_shema = metadata['json-ld'] if metadata['json-ld'] else metadata['microdata'] if metadata['microdata'] else metadata['opengraph'] if metadata['opengraph'] else []
    for e in rez_shema:
        if ('@type' in e) and (e['@type'] == 'Product'):
            try:
                title = e['name']
                price = e['offers']['price']
            except Exception as err:
                pass
    return title, price

def rozetka_schema(data):
    title = ''
    price = 0
    rozetka_script = re.findall('application/json\">(.+?)</script>', data)
    for rozetka in rozetka_script:
        try:
            rozetka = json.loads(rozetka.replace('&q;', '\"'))
            for key in rozetka:
                if 'get-main' in key:
                    title = rozetka[key]['body']['data']['title']
                    price = rozetka[key]['body']['data']['price']
        except Exception as err:
            pass
    return title, price

def schema_parser(url, article, path_to_db = None, driver = None):
    price_table = Price()
    price_table.store = ''

    if driver:
        close_driver_on_exit = False
    else:
        close_driver_on_exit = True
        driver = Driver()
    price_table.set_article(article)

    driver.get(url)
    result = driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')

    if 'rozetka.com.ua/' in url:
        title, price = rozetka_schema(result)
    else:
        title, price = common_schema(result)

    if not title:
        title = driver.title

    url = driver.current_url
    seller = urlsplit(url, allow_fragments = False).netloc

    if close_driver_on_exit:
        driver.close()

    price_table.add(title = title, price = price, seller = seller, url = url)
    price_table.write(path_to_db)
    if price == 0:
        return 0

    return len(price_table.data)

if __name__ == '__main__':
    path_to_db = 'Price.db'
    url = 'https://prom.ua/p1396374517-videokamera-hikvision-2cd2043g0.html'
    article = 'DS-2CD2043G0-I'
    print(schema_parser(url, article, path_to_db))
