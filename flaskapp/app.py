# Copyright © 2023-2024, Indiana University
# BSD 3-Clause License
# imports
from flask import Flask, render_template, url_for, request, redirect
from collections import defaultdict
import flaskapp.database as db
import random
app = Flask(__name__)




# Function to clean cost in items
def string_to_float(price_str):
    cleaned_str = price_str.replace('$', '').strip()
    return round(float(cleaned_str), 2) 

# --------------------------------------------------------------
# -------------------- login Route -----------------------------
# --------------------------------------------------------------

@app.route("/",  methods=['GET', 'POST'])
def render_login():

    # gets all users
    users = db.get_users()

    # gets form info
    if request.method=='POST':
        email = request.form['form-email']
        password = request.form['form-password']
        
        # loops through user db and checks password match
        for user in users:
            if user['email'] == email and user['password'] == password:
                # redirects user to their home page
                return redirect(url_for('render_home_user', id=user['id']))
            
        # if password is wrong, user is shown a button to try again
        return render_template('login.html', action='invalid_login')
    
    # renders the login template
    return render_template('login.html', action='pass')

# --------------------------------------------------------------
# -------------------- signup Route ----------------------------
# --------------------------------------------------------------

@app.route("/signup/", methods=['GET', 'POST'])
def render_signup():

    # getting emails to check if user is registering with a new email
    user_emails = db.get_email()

    if request.method == 'POST':
        name = request.form['form-name']
        email = request.form['form-email']
        password = request.form['form-password']
        confirm_pass = request.form['form-confirm-password']

        if email in user_emails:
            return render_template('sign_up.html', action='email_exists')
        else:
            if password == confirm_pass:
                new_user = {
                    'name': name,
                    'email': email,
                    'password': password,
                }

                # adds new user to the db as a dictionary
                db.add_user(new_user)
                return redirect(url_for('render_login'))
            else:
                return render_template('sign_up.html', action ='incorrect_password')
    return render_template('sign_up.html', user_emails=user_emails, action='pass')    
        

            
# --------------------------------------------------------------
# -------------------- Home Route ----------------------------
# --------------------------------------------------------------

@app.route("/home/<id>", methods=['GET', 'POST'])
def render_home_user(id):
    user = db.get_one_user(id)
    budget = db.get_budget(id)

    if request.method == 'POST':

        # adding user budget request

        expenses = request.form['expenses-percentage']
        wants = request.form['wants-percentage']
        savings = request.form['savings-percentage']

        budget = {
            'user_id': user['id'],
            'expenses': expenses,
            'wants': wants,
            'savings': savings,
        }

        db.add_budget(budget)

        # calculate user income, expenses, wants, savings

        sum_income = (
            int(request.form['main-income']) + 
            int(request.form['passive']) + 
            int(request.form['other'])
            )
        sum_expenses = (
            int(request.form['mortgage']) + 
            int(request.form['utilities']) + 
            int(request.form['transportation']) + 
            int(request.form['groceries']) + 
            int(request.form['insurance']) + 
            int(request.form['debt']) 
        )
        sum_wants = (
            int(request.form['personal']) + 
            int(request.form['dining']) + 
            int(request.form['shopping']) 
        )

        sum_savings = (
            int(request.form['savings']) + 
            int(request.form['emergency-fund']) + 
            int(request.form['retirement'])
        )

        user_budget = {
            'user_id': user['id'],
            'income': sum_income,
            'expenses': sum_expenses,
            'wants': sum_wants,
            'savings': sum_savings,
        }

        db.add_user_spending(user_budget)
    return render_template('home.html', user=user, budget=budget)

@app.route("/home/clear/<id>")
def render_clear_budget(id):
    db.clear_budget()
    user = db.get_one_user(id)
    return render_template('home.html', user=user)


@app.route("/home/budget/<id>", methods=['GET', 'POST'])
def render_home_user_budget(id):

    user = db.get_one_user(id)

    return render_template('budget.html', user=user)






















# --------------------------------------------------------------
# -------------------- Customer Routes -------------------------
# --------------------------------------------------------------

# Renders customers page
@app.route('/customers/')
def render_customers():
    all_customers = db.get_customer()
    return render_template("customers.html", all_customers=all_customers)


# Directs to adds page where users can add a new customer then redirected back to customers page
@app.route("/customers/add/", methods=['GET', 'POST'])
def render_customer_form():

    if request.method == "POST":
        # Get form data
        customer_name = request.form['form-name']
        email = request.form['form-email']
        phone = request.form['form-phone']
        
        # Processing step 1: Put data into a dictionary
        new_customer = {
            'name': customer_name,
            'email': email,
            'phone': phone
        }

        # Processing step 2: Add new data to CSV
        db.add_customer(new_customer)
        # Redirect to customers list page
        return redirect(url_for('render_customers'))  
    else:
        return render_template("customer_form.html",customer = None, action='add')


# Directs to edits page where user can edit a current customer then redirected back to customers page
@app.route("/customers/edit/<customer_id>", methods=['GET', 'POST'])
def render_customer_form_edit(customer_id):
    # load one customer
    
    customer = db.get_one_customer(customer_id)

    if request.method == 'POST':
        # Get the form data
        new_name = request.form['form-name']
        new_email = request.form['form-email']
        new_phone = request.form['form-phone']

        # Update the customer data
        db.update_customer(customer_id, new_name, new_email, new_phone)

        
        return redirect(url_for('render_customers'))
    
    return render_template("customer_form.html", customer=customer, action='edit')    

# --------------------------------------------------------------
# -------------------- Item Routes -----------------------------
# --------------------------------------------------------------

# Renders items page
@app.route('/items/')
def render_items():
    all_items = db.get_item()
    return render_template('items.html', all_items=all_items)

# Directs user to adds page where user can add a new item then redirected back to items page
@app.route("/items/add/", methods=['GET', 'POST'])
def render_item_form():
    if request.method == "POST":
# get form data
        image = 'images/bread.jpg' 
        # bread here is a place holder image since image isnt required
        name = request.form['form-name']
        cost = request.form['form-cost']
# processing step 1: put data to dictionary
        new_item = {
            'images': image,
            'name': name,
            'cost': cost
        }

# processing step 2: add new data to csv
        db.add_item(new_item)
        # result: redirect to home page route
        return redirect(url_for('render_index'))
    else:
        # view customersw
        return render_template("item_form.html", item=None, action='add')
    

# Directs user to edits page where user can edit a current item then redirected back to items page
@app.route("/items/edit/<item_id>", methods=['GET', 'POST'])
def render_item_form_edit(item_id):
    # load items
    item = db.get_one_item(item_id)

    # get form data
    if request.method == 'POST':
        new_item = request.form['form-name']
        new_cost = request.form['form-cost']

        # updating form data
        
        db.update_item(item_id, new_item, new_cost)

        return redirect(url_for('render_items'))

    return render_template('item_form.html', item=item, action='edit')

# --------------------------------------------------------------
# -------------------- Order Routes ---------------------------
# --------------------------------------------------------------

@app.route('/orders/')
def render_order():
    all_orders = db.get_order()

    return render_template('orders.html', all_orders=all_orders)


@app.route('/order_details/<id>')
def render_order_detail(id):    
    order = db.get_one_order(id)
    all_orders = db.get_order()

    order_details = []
    for item in all_orders:
        if item['orderID'] == order['orderID']:
            order_details.append(item['item'])
    
    
    return render_template('order_details.html', order=order,all_orders=all_orders, order_details=order_details)


# --------------------------------------------------------------
# -------------------- Cart Routes -------------------------
# --------------------------------------------------------------

# Renders cart page
@app.route('/cart/', methods=['GET', 'POST'])
def render_cart():
    cart = db.get_cart()
    all_customers = db.get_customer()
    total = 0

    if cart:
        action ='added'
        total = 0
        # calc subtotal
        for item in cart:
            if 'cost' in item and item['cost']:
                cost_float = string_to_float(item['cost'])  # Convert cost to float
                total += cost_float 
        total = round(total, 2)  

    else:
        action = 'empty'

    return render_template('cart.html', cart=cart, action=action, all_customers=all_customers, total=total)


# Allows users to add items to the cart page
@app.route("/cart/add/<item_id>", methods=['GET', 'POST'])
def render_add_item_to_cart(item_id):
    item = db.get_one_item(item_id)

    if request.method == 'POST':
        db.add_item_to_cart(item)
        cart = db.get_cart()
        return redirect(url_for('render_index'))

    return render_template('cart.html', cart=cart)


# Allows users to clear cart from cart page - redirected back to home page page (empty)
@app.route('/cart/clear/', methods = ['GET', 'POST'])
def render_clear_cart():
    db.clear_cart()
    return redirect(url_for('render_index'))

# Allow users to checkout from cart
@app.route('/cart/checkout/', methods=['POST'])
def render_cart_checkout():
    
    cart = db.get_cart()
    num = random.randint(1,100000000)
    custname = request.form['dropdown']

    for item in cart:
        order = {
            'orderID': num,
            'name': custname,
            'item': item['name']
        }
        db.add_order(order)
    db.clear_cart()

    return redirect(url_for('render_order'))
