from flask import Flask
from flask import render_template, Flask, flash, request, redirect, url_for, Response, session, abort, jsonify, send_file
import json
app = Flask(__name__, static_path='/static')
app.secret_key = 'cs348'

product = {
    "Flower A" : 12.99, "Flower B" : 12.99, "Flower C" : 11, "Flower D" : 10, "Flower 11" : 12,
    "Decor A" : 89.99, "Decor B" : 78, "Decor C" : 100, "Decor D" : 9, "Free Stuff" : 0
}

@app.route('/createOrder', methods = ['GET', 'POST'])
def createOrder():
    global product
    price = 0
    if request.method == 'GET':
        return render_template('select.html', product=product)
    else:
        price = request.get_data()
        price = price[6:]
        return redirect(url_for('orderInfo', price=price))

@app.route('/orderInfo/<price>', methods = ['GET', 'POST'])
def orderInfo(price):
    price = float(price)
    if request.method == 'GET':
        return "hello"

@app.route('/searchOrder', methods = ['GET', 'POST'])
def searchOrder():
    if request.method == 'GET':
        return "world"

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
    # else:
    #     print("post")
    #     d = request.args.get('teamData')
    #     print(d)
    #     print(request.json)
    #     return redirect(url_for('admin'))


@app.route('/', methods = ['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
