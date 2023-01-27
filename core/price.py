#encoding: windows-1251
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import sqlite3 as sl

try:
    from core.core_io import write2database, log_error, log_info
except Exception:
    from core_io import write2database, log_error, log_info

class Price():
    dtype = {
        'article': sqlalchemy.types.NVARCHAR(length=255),
        'title': sqlalchemy.types.NVARCHAR(length=255),
        'price': sqlalchemy.types.Float(),
        'store': sqlalchemy.types.NVARCHAR(length=50),
        'seller': sqlalchemy.types.NVARCHAR(length=255),
        'url': sqlalchemy.types.NVARCHAR(length=255),
        }

    def __init__(self):
        self.data = []
        self.article = ''
        self.store = ''
        self.table_name = 'mk_price'
  
    def add(self, title, price, seller, url):
        self.data.append((self.article, title, price, self.store, seller, url))

    def write(self, path = None):
        #write data do db
        df = pd.DataFrame(self.data, columns=[e for e in self.dtype])

        if path == None:
            write2database(df, self.table_name, dtype=self.dtype)
        else:
            write2database(df, self.table_name, dtype=None, engine = sl.connect(path))#4Debug

    def _hash(self, s):
        _hash = ''
        for c in s:
            c = c.lower()
            if c.isdigit() or ('a' <= c <= 'z'):
                _hash += c
        return _hash

    def set_article(self, article):
        self.article = article
        self.article_hash = self._hash(article)

    def match_article(self, title):
        return self.article_hash in self._hash(title)

if __name__ == '__main__':
    price = Price()
    price.store = 'rozetka'
    price.set_article('TV article MCD45')

    print(price.match_article('Супер test tv article MCD45 цветной + T2'))

#    price.add(title = 'test_title1', price = 77, seller = 'sellerX', url = 'link1')
#    price.add(title = 'test_title2', price = 76, seller = 'sellerY', url = 'link2')
#    price.add(title = 'test_title3', price = 78, seller = 'sellerZ', url = 'link3')

#    price.write('test.db')
