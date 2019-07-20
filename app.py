from flask import Flask
from flask import render_template, Flask, flash, request, redirect, url_for, Response, session, abort, jsonify, send_file
import json
import dbConnect

app = Flask(__name__, static_path='/static')
app.secret_key = 'cs348'

product = {
    "Flower A" : 12.99, "Flower B" : 12.99, "Flower C" : 11, "Flower D" : 10, "Flower 11" : 12,
    "Decor A" : 89.99, "Decor B" : 78, "Decor C" : 100, "Decor D" : 9, "Free Stuff" : 0
}

price = 0

@app.route('/createOrder', methods = ['GET', 'POST'])
def createOrder():
    global product
    global price
    if request.method == 'GET':
        return render_template('select.html', product=product)
    else:
        if not price == 0:
            return redirect(url_for('orderInfo'))
        p = request.get_data()
        if not p == 0:
            price = p[6:]
        else:
            price = p
        print(price)
        return redirect(url_for('orderInfo'))

@app.route('/orderInfo', methods = ['GET', 'POST'])
def orderInfo():
    global price
    price = float(price)
    print(price)
    if request.method == 'GET':
        return "hello"

@app.route('/searchOrder', methods = ['GET', 'POST'])
def searchOrder():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        return redirect(url_for('userDashboaerd'))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        postalcode = request.form['postalcode']
        if name == "" or password  == "" or firstname == "" or \
           lastname == "" or phone == "" or email == "" or address == "" or \
           postalcode == "":
           flash("Error! You must fill in all information.")
           return render_template('signup.html')
        if len(password) < 6:
            flash("Error! You password must be at least 6 digits")
            return render_template('signup.html')
        if password == password2:
            #add account into sql
            return redirect(url_for('userDashboard'))
        else:
            flash("Error! You password inputs do not match.")
            return render_template('signup.html')

@app.route('/userDashboard', methods = ['GET', 'POST'])
def userDashboard():
    return "haha"


@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    else:
        name=request.form['username']
        password=request.form['password']
        if name == "":
            flash("Error! Please provide a username.")
            return redirect(url_for('admin'))
        if password == "":
            flash("Error! Please provide a password.")
            return redirect(url_for('admin'))
        elif (not name == "cs348") or (not password == "348348"):
            flash("Error! please provide the correct username and password.")
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('adminDashboard'))

@app.route('/adminDashboard', methods = ['GET', 'POST'])
def adminDashboard():
    return "hi"

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')


@app.route('/', methods = ['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
