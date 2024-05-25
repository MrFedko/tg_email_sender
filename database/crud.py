import sqlite3
from data.config import settings


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(settings.DB_PATH)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mail TEXT NOT NULL,
    phone TEXT NOT NULL
);""")
        self.connection.commit()
        self.cursor.execute("""CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    theme TEXT NOT NULL,
    description TEXT
);""")
        self.connection.commit()
        self.cursor.execute("""CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INTEGER NOT NULL,
    fk_product_name TEXT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    product_date TEXT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (fk_user_id) REFERENCES clients(id),
    CONSTRAINT fk_product FOREIGN KEY(fk_product_name) REFERENCES products(name)
);""")
        self.connection.commit()

    # create
    def new_client(self, name, mail, phone):
        self.cursor.execute(
            "INSERT INTO clients (name, mail, phone) VALUES (?, ?, ?)",
            (name, mail, phone))
        self.connection.commit()

    def new_product(self, name, theme, description):
        self.cursor.execute(
            "INSERT INTO products (name, theme, description) VALUES (?, ?, ?)",
            (name, theme, description))
        self.connection.commit()

    def new_order(self, user_id, prod_name, product_date):
        self.cursor.execute(
            "INSERT INTO orders (fk_user_id, fk_product_name, product_date) VALUES (?, ?, ?)",
            (user_id, prod_name, product_date))
        self.connection.commit()

    # read
    def read_products(self):
        self.cursor.execute("SELECT id, name FROM products;")
        rows = self.cursor.fetchall()
        return rows

    def read_product(self, prod_id):
        self.cursor.execute("""SELECT name, theme, description FROM products
        WHERE id = ? """, (prod_id, ))
        result = self.cursor.fetchone()
        return result

    def get_text(self, name):
        self.cursor.execute("""SELECT theme, description FROM products
        WHERE name = ? """, (name, ))
        result = self.cursor.fetchone()
        return result

    def read_client(self, mail):
        self.cursor.execute("""SELECT id, name, mail, phone FROM clients
        WHERE mail = ? """, (mail, ))
        result = self.cursor.fetchone()
        return result

    def read_client_id(self, mail):
        self.cursor.execute("""SELECT id FROM clients
        WHERE mail = ? """, (mail, ))
        result = self.cursor.fetchone()
        return result

    def read_client_mail_name_by_product_day(self, date):
        self.cursor.execute("""SELECT DISTINCT clients.name, clients.mail 
            FROM orders
            JOIN clients ON orders.fk_user_id = clients.id
            WHERE orders.product_date = ?""", (date, ))
        result = self.cursor.fetchall()
        return result

    def read_dates(self):
        self.cursor.execute("""SELECT DISTINCT product_date, fk_product_name FROM orders""")
        dates = self.cursor.fetchall()
        return dates

    def read_mail_by_id(self, user_id):
        self.cursor.execute("""SELECT mail, name from clients
        WHERE id = ?""", (user_id, ))
        user_mails = self.cursor.fetchall()
        return user_mails


    # update
    def update_product(self, prod_id, name, theme, text):
        self.cursor.execute("""
        UPDATE products
        SET name = ?, theme = ?, description = ?
        WHERE id = ?
    """, (name, theme, text, prod_id))
        self.connection.commit()

