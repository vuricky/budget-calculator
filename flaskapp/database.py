import csv
import os
import pymysql
import pymysql.cursors

def load_password():
    path = os.path.join(os.path.expanduser("~"), "i211f24-password.txt")
    with open(path) as fh:
        return fh.read().strip()
    
DB_PASSWORD = load_password()
DB_HOST = 'db.luddy.indiana.edu'
DB_USER = 'i211f24_rvu'
DB_DATABASE = 'i211f24_rvu'

# getting connected to database in maria
def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    )

# --------------------------------------------------------------------------------------
# ------------------------------- User functions -----------------------------------
# --------------------------------------------------------------------------------------

def add_user(user: dict[str, str]) -> None:
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into users (username, password) values (%s, %s)",
            (
                user['username'],
                user['password'],
            ),
        )
    conn.commit()
    conn.close()



def add_customer(customer: dict[str, str]) -> None:
    """takes a dictionary and inserts into a database table"""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into customers (name, email, phone) values (%s, %s, %s)",
            (
                customer["name"],
                customer["email"],
                customer["phone"],

            ),
        )
    conn.commit()
    conn.close()




# --------------------------------------------------------------------------------------
# ------------------------------- Customer functions -----------------------------------
# --------------------------------------------------------------------------------------


# function to get all customers from table
def get_customer():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM customers")
        customers = curr.fetchall()
    conn.commit()
    conn.close()
    return customers

# function to get data for one customer
def get_one_customer(id):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM customers WHERE id = %s", (id))
        customer = curr.fetchone()
    conn.commit()
    conn.close()
    return customer

# function updating customer information when edited
def update_customer(customer_id, name, email, phone):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            """
            UPDATE customers
            SET name = %s, email = %s, phone = %s
            WHERE id = %s
            """,
            (name, email, phone, customer_id)
        )
    conn.commit()
    conn.close()
    

# Adding customers to the database when making a new customer
def add_customer(customer: dict[str, str]) -> None:
    """takes a dictionary and inserts into a database table"""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into customers (name, email, phone) values (%s, %s, %s)",
            (
                customer["name"],
                customer["email"],
                customer["phone"],

            ),
        )
    conn.commit()
    conn.close()

# --------------------------------------------------------------------------------------
# ----------------------------- functions for Items ------------------------------------
# --------------------------------------------------------------------------------------

# getting all items from database
def get_item():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM items")
        items = curr.fetchall()
    conn.commit()
    conn.close()
    return items

# getting data for one item from database
def get_one_item(id):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM items WHERE id = %s", (id))
        item = curr.fetchone()
    conn.commit()
    conn.close()
    return item

# Updating item information after editing
def update_item(item_id, name, cost):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            """
            UPDATE items
            SET name = %s, cost = %s
            WHERE id = %s
            """,
            (name, cost, item_id)
        )
    conn.commit()
    conn.close()

# Adding items to the database when creating a new item
def add_item(item: dict[str, str]) -> None:
    """takes a dictionary and inserts into a database table"""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into items (images, name, cost) values ( %s, %s, %s)",
            (
                item["images"],
                item["name"],
                item["cost"],

            ),
        )
    conn.commit()
    conn.close()

# --------------------------------------------------------------------------------------
# ---------------------------- functions for orders ------------------------------------
# --------------------------------------------------------------------------------------

# Getting all orders from database
def get_order():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM orders")
        orders = curr.fetchall()
    conn.commit()
    conn.close()
    return orders

# Getting data from a single order
def get_one_order(id):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute('SELECT * FROM orders WHERE orderID=%s', id)
        order = curr.fetchone()
    conn.commit()
    conn.close()
    return order


def add_order(order: dict[str, str]) -> None:
    """takes a dictionary and inserts into a database table"""
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into orders (orderID, name, item) values (%s, %s, %s)",
            (
                order["orderID"],
                order["name"],
                order["item"],

            ),
        )
    conn.commit()
    conn.close()
# --------------------------------------------------------------------------------------
# ---------------------------------- Cart Section --------------------------------------
# --------------------------------------------------------------------------------------

# Getting all all data in cart
def get_cart():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute('SELECT * FROM cart join items on items.id = cart.item_id')
        cart = curr.fetchall()
    conn.commit()
    conn.close()
    return cart

# adding an item to the cart by its id
def add_item_to_cart(item):
    conn = get_connection()
    with conn.cursor() as curr:
       curr.execute(
           'insert into cart (item_id) values (%s)',
           (
            item['id'],
           )
                
        ),
    conn.commit()
    conn.close()

# Deleting all items from cart table
def clear_cart():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            'delete from cart'
        )
    conn.commit()
    conn.close()

# --------------------------------------------------------------------------------------
# -------------------- Creating the four tables for the data base ----------------------
# --------------------------------------------------------------------------------------

def intialize_db():
    conn = get_connection()

    _users = """
    CREATE TABLE users (
        id int auto_increment
        username varchar(50),
        password varchar(50)
    ) engine=InnoDB """
    

    with conn.cursor() as curr:
        curr.execute("drop table if exists users")
        curr.execute(_users)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    intialize_db()
