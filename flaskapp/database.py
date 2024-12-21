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
            "insert into users (email, password) values (%s, %s)",
            (
                user['email'],
                user['password'],
            ),
        )
    conn.commit()
    conn.close()


def get_email():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT email from users")
        emails = curr.fetchall()
        list_emails = []
        for email in emails:
            list_emails.append(email['email'])
    conn.commit()
    conn.close()
    return list_emails

def get_users():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM users")
        users = curr.fetchall()
    conn.commit()
    conn.close()
    return users

def get_one_user(id):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM users WHERE id = %s", (id))
        user = curr.fetchone()
    conn.commit()
    conn.close()
    return user




# --------------------------------------------------------------------------------------
# -------------------- Creating the four tables for the data base ----------------------
# --------------------------------------------------------------------------------------

def intialize_db():
    conn = get_connection()

    _users = """
    CREATE TABLE users (
        id int auto_increment primary key,
        email varchar(50),
        password varchar(50)
    ) engine=InnoDB """


    with conn.cursor() as curr:
        curr.execute("drop table if exists users")
        curr.execute(_users)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    intialize_db()
