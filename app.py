from flask import Flask
from flask import render_template, Flask, flash, request, redirect, url_for, Response, session, abort, jsonify, send_file
import json
#import dbConnect
from db_helper import *

app = Flask(__name__, static_path='/static')
app.secret_key = 'cs348'

username = "gab"

product = ""

eventType = {"1" : "birthday",
             "2" : "wedding",
             "3" : "professional",
             "4" : "other"}

product_price = {"000000":12.99,"000001":45.99,"000003":100.99,"000004":70, "000005":12,"000006":33}

paytype = {"visa" : 1, "master-card":2, "amex":3,"vishwa":4, "cash":5}

price = 0

@app.route('/createOrder', methods = ['GET', 'POST'])
def createOrder():
    global product
    global price
    if request.method == 'GET':
        return redirect(url_for('userlogin'))


@app.route('/shoppingcart', methods = ['GET', 'POST'])
def shoppingcart():
    global product
    global price
    global product_price
    if request.method == 'GET':
        return render_template('shoppingcart.html')
    else:
        try:
            add = request.json
        except:
            pass
        try:
            add.items()
        except:
            return redirect(url_for('orderInfo'))
        s = ""
        p = 0
        for k,v in add.items():
            s += str(k) + "-" + str(v) + " "
            p = p + product_price[k] * v
        product = s
        price = p #excluding shipping and tax
        print(product)
        print(price)
        return redirect(url_for('orderInfo'))

@app.route('/orderInfo', methods = ['GET', 'POST'])
def orderInfo():
    global price
    global eventType
    global username
    global product

    venues = selectAll_db("Venue", "Venue_id, Location")
    v = {}
    for record in venues:
        v[record[0]] = record[1]
    if request.method == 'GET':
        return render_template('orderInfo.html', venue=v, type=eventType)
    else:
        invittes = request.form['invittes']
        starttime = request.form['starttime']
        closetime = request.form['closetime']
        budgets = request.form['budgets']
        deliverytime = request.form['deliverytime']
        customization = request.form['customization']
        venueoption = request.form['venueoption']
        billing = request.form['Billing']
        type = request.form['type']
        if billing == "" or invittes == "" or starttime == "" or closetime == "" or budgets == "" or deliverytime == "":
            flash("Error! Fields cannot be blank")
            return render_template('orderInfo.html', venue=v, type=eventType)
        #save into dbConnect
        pk_id = generate_id("Event", "Event_id")
        value = (pk_id,float(budgets),invittes,int(type),starttime,closetime, \
                    v[venueoption], customization, deliverytime, username, venueoption)
        try:
            insert_db("Event", schema_event, value) #insert data
            print(value)
        except:
            print(value)
            insert_db("Event", schema_event, value) #insert data

            flash("Internal error occurs, please try again.")
            return render_template('orderInfo.html', venue=v, type=eventType)
        return redirect(url_for('payment', pk_id=pk_id, billing=billing))

@app.route('/payment/<pk_id>/<billing>', methods = ['GET', 'POST'])
def payment(pk_id, billing):
    global username
    global price
    global product
    global paytype
    print("information recorded: ")
    print(product)
    print(price)
    if request.method == 'GET':
        return render_template('payment.html')
    else:
        paidtype = request.form['options'] #get payment type
        paidtype = paytype[paidtype]
        iscomplete = 0
        cardtype = paidtype
        isPaid = 0
        price = int(price * 1.13 + 15)
        order_number = generate_id("OrderInfo","Order_number")
        value = (billing, iscomplete, product, price, isPaid, paidtype, order_number, cardtype, pk_id, username)
        insert_db("OrderInfo", schema_order, value) #insert data
        print("Value inserted into order table")
        return redirect(url_for('success'))

@app.route('/success', methods = ['GET', 'POST'])
def success():
    return render_template('success.html')


@app.route('/userlogin', methods = ['GET', 'POST'])
def userlogin():
    global username
    if request.method == 'GET':
        return render_template('login2.html')
    else:
        name = request.form['username']
        password = request.form['password']
        record = select_db("Customer", "UserId='" + name + "' and Password = '" + password +"'")
        if record == []:
            flash("Error, incorrect username or password")
            return redirect(url_for('userlogin'))
        username = name
        return redirect(url_for('shoppingcart'))

@app.route('/searchOrder', methods = ['GET', 'POST'])
def searchOrder():
    global username
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        password = request.form['password']
        record = select_db("Customer", "UserId='" + name + "' and Password = '" + password +"'")
        if record == []:
            flash("Error, incorrect username or password")
            return redirect(url_for('searchOrder'))
        username = name
        return redirect(url_for('userDashboard'))

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
            value = (name,password,firstname,lastname,phone,email,address,postalcode)
            insert_db("Customer", schema_customer, value) #insert data
            return redirect(url_for('dashboard'))
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
