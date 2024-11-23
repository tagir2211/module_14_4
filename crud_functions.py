import sqlite3

from text import *

connection = sqlite3.connect("Product.db")
cursor = connection.cursor()


def connect(funk):
    def wraper(*args):
        connection = sqlite3.connect("Product.db")
        cursor = connection.cursor()
        funk(*args)
        connection.commit()
        connection.close()

    return wraper


@connect
def initiate_db(name):
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {name}(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,    
    price INTEGER NOT NULL
    )
    ''')
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_email ON {name} (id)")


@connect
def add_data(name):
    for i in range(len(title)):
        cursor.execute(f"INSERT INTO {name}(title, description, price) VALUES (?, ?, ?)", (title[i], info[i], price[i]))


def get_all_products(name, id):
    cursor.execute(f"SELECT * FROM {name} WHERE id = ?", (id,))
    product = cursor.fetchall()
    return f'Название: {product[0][1]} | Описание: {product[0][2]} | Цена: {product[0][3]}'

# TABLE_NAME = 'Product'
# initiate_db(TABLE_NAME)
# add_data(TABLE_NAME)
# for i in range(4):
#     print(i)
#     print(get_all_products(TABLE_NAME, i+1))
# print('ok')
