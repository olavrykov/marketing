import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import traceback

try:
    from core.credentials import DB
except Exception:
    from credentials import DB

LOG_FNAME = "price_log.txt"
engine_str = f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["database"]}'

last_table = ''
last_date = None

def write2database(df, table, dtype, engine = None):
    global last_table
    global last_date
    if engine == None:
        engine = create_engine(engine_str)
    result = 1

    replace_or_append = 'append' if table == last_table else 'replace'
    last_table = table
    if not last_date:
        last_date = datetime.datetime.now()

    try:
        df_dates = pd.DataFrame()
        df_dates['date'] = [last_date]*df.shape[0]
        df = df_dates.join(df)
        df.to_sql(table, con=engine, if_exists=replace_or_append, index=False, dtype = dtype)
    except Exception:
        log_error(f'Problem with download {table} to sql')
        result = 0
#    if result:
#        log_info(f'{table} - ok')
    return result

def load_table(table, engine = None):
    if engine == None:
        engine = create_engine(engine_str)
    else:
        engine = create_engine('sqlite:///' + engine, echo=False)

    try:
        df = pd.read_sql_table(table, con=engine)
        result = [e[0] for e in df.values.tolist()]
    except Exception as err:
        print(err)
        result = []
    return result

def load_table_all(table, engine = None):
    if engine == None:
        engine = create_engine(engine_str)
    else:
        engine = create_engine('sqlite:///' + engine, echo=False)

    try:
        df = pd.read_sql_table(table, con=engine)
        result = df.values.tolist()
    except Exception as err:
        print(err)
        result = []
    return result

def del_duplicates(table_name, path_to_db = None):
    if path_to_db == None:
        engine = create_engine(engine_str)
    else:
        engine = create_engine('sqlite:///' + path_to_db, echo=False)

    df = pd.read_sql(f'SELECT article, title, price, store, seller, url, date FROM {table_name} WHERE DATE(date) >= DATE(\"{datetime.datetime.now()}\")', con=engine, parse_dates=['date'])
    doubles = df.duplicated(subset=['article', 'title', 'price', 'seller'])

    to_del = []
    for n, e in enumerate(doubles):
        if e:
            to_del.append(df.loc[n].tolist())

    with engine.connect() as conn:
        for e in to_del:
            title = str_quotted(e[1])
            store = str_quotted(e[3])
            seller = str_quotted(e[4])
        query_string = f'DELETE FROM {table_name} WHERE article="{e[0]}" AND title={title} AND price={e[2]} AND store={store} AND seller={seller} AND url="{e[5]}" AND date="{e[6]}"'
        conn.execute(query_string)

def del_old_data(table_name, path_to_db = None):
    if path_to_db == None:
        engine = create_engine(engine_str)
    else:
        engine = create_engine('sqlite:///' + path_to_db, echo=False)
    last_table = table_name

    with engine.connect() as conn:
        conn.execute(f'DELETE from {table_name} where DATE(date) < DATE("{datetime.datetime.now()-datetime.timedelta(days=365)}")')

def set_append_table(table_name):
    global last_table
    global last_date
    last_table = table_name
    last_date = datetime.datetime.now()

def log_error(s):
     _log(s, is_error = True)

def log_info(s):
     _log(s, is_error = False)

def _log(s, is_error):
    with open(LOG_FNAME, 'a', encoding='utf-8') as f:
        f.write('\n' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n')
        f.write(s + '\n')
        if is_error:
            traceback.print_exc(file=f)

def str_quotted(s):
    if '\'' in s:
        if '\"' in s:
            q = None
        else:
            q = '\"'
    else:
        q = '\''
    if q:
        return f'{q}{s}{q}'
    else:
        return '\"\"'
