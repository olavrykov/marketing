from core.core_io import load_table, load_table_all, del_duplicates, set_append_table, del_old_data
from core.driver import Driver

from price_rozetka import rozetka_art
from price_prom import prom_art
from price_hotline import hotline_art
from price_gmc import gmc_art

from schema_parser import schema_parser

path_to_db = 'Price.db'
path_to_db = None

articles = load_table('mk_article', path_to_db)
urls_articles = load_table_all('mk_url', path_to_db)

set_append_table('mk_price')

driver = Driver()
for article in articles:
    print(article)
    print('prom\t', prom_art([article], path_to_db, driver))
    print('hotline\t', hotline_art([article], path_to_db, driver))
    print('gmc\t', gmc_art([article], path_to_db, driver))
    print('rozetka\t', rozetka_art([article], path_to_db, driver))

for url, article in urls_articles:
    if not schema_parser(url, article, path_to_db, driver):
        print(f'Error parse: {url}')

driver.close()

del_old_data('mk_price', path_to_db)
del_duplicates('mk_price', path_to_db)

#import Report
