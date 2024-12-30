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

        return redirect(url_for('render_budget', id=user['id']))
    return render_template('home.html', user=user, budget=budget)


# --------------------------------------------------------------
# -------------------- budget Route ----------------------------
# --------------------------------------------------------------

@app.route('/budget/<id>', methods=['GET', 'POST'])
def render_budget(id):
    user = db.get_one_user(id)
    budget = db.get_budget(id)
    user_budget = db.get_user_budget(id)

    if request.method == 'POST':
        db.clear_budget()
        db.clear_user_budget()
        return redirect(url_for('render_home_user', id=user['id']))


    return render_template('budget.html', user=user, budget=budget, user_budget=user_budget)

# --------------------------------------------------------------
# --------------------- about Route ----------------------------
# --------------------------------------------------------------

@app.route('/about/<id>')
def render_about(id):
    user = db.get_one_user(id)
    return render_template('about.html', user=user)