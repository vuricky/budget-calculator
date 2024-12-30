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
# ----------------- User functions for signing up and logining in ----------------------
# --------------------------------------------------------------------------------------

def add_user(user: dict[str, str]) -> None:
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into users (name, email, password) values (%s, %s, %s)",
            (
                user['name'],
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
# ---------------------------- User budget functions ----------------------------------
# --------------------------------------------------------------------------------------

def get_budget(id):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM budget WHERE user_id =%s", (id))
        budget = curr.fetchone()
    conn.commit()
    conn.close()
    return budget

def get_user_budget(id):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM user_budget WHERE user_id =%s", (id))
        user_budget = curr.fetchone()
    conn.commit()
    conn.close()
    return user_budget

def clear_budget():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            'delete from budget'
        )
    conn.commit()
    conn.close()

def clear_user_budget():
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            'delete from user_budget'
        )
    conn.commit()
    conn.close()



def add_budget(budget: dict[str, str]) -> None:
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into budget (user_id, expenses, wants, savings) values (%s, %s, %s, %s)",
            (
                budget['user_id'],
                budget['expenses'],
                budget['wants'],
                budget['savings'],
            )
        )
    conn.commit()
    conn.close()

def add_user_spending(spending :dict[str,str]) -> None:
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            "insert into user_budget (user_id, income, expenses, wants, savings) values (%s, %s, %s, %s, %s)",
            (
                spending['user_id'],
                spending['income'],
                spending['expenses'],
                spending['wants'],
                spending['savings'],

            )
        )
    conn.commit()
    conn.close()
# --------------------------------------------------------------------------------------
# -------------------- Creating the tables for the data base ---------------------------
# --------------------------------------------------------------------------------------

def intialize_db():
    conn = get_connection()

    _users = """
    CREATE TABLE users (
        id int auto_increment primary key,
        name varchar(50),
        email varchar(50),
        password varchar(50)
    ) engine=InnoDB """

    _budget = """
    CREATE TABLE budget (
        user_id INT not null,
        expenses decimal(10,2) NOT NULL,
        wants decimal(10,2) NOT NULL,
        savings decimal(10,2) NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    ) engine=InnoDB """

    _user_budget = """
    CREATE TABLE user_budget (
        user_id INT NOT NULL,
        income decimal(10,2) NOT NULL,
        expenses decimal(10,2) NOT NULL,
        wants decimal(10,2) NOT NULL,
        savings decimal(10,2) NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    ) engine=InnoDB """


# --------------------------------------------------------------------------------------
# ------------------- Resets data base when the database is run ------------------------
# --------------------------------------------------------------------------------------


    with conn.cursor() as curr:
        curr.execute("drop table if exists user_budget")
        curr.execute("drop table if exists budget")
        curr.execute("drop table if exists users")
        curr.execute(_users)
        curr.execute(_budget)
        curr.execute(_user_budget)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    intialize_db()
