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

paytype_reverse = {
                    0 : "Visa Card",
                    1 : "Master-card",
                    2 : "Amercian Express Card",
                    3 : "Vishwa Card",
                    4 : "Cash"
                }

price = 0

def menu_process():
    """
        Lookup table for product name - product id in menu table
    """
    data = selectAll_db("Menu")
    lookup = {}
    for item in data:
        lookup[item[0]] = item[1]
    return lookup

def process_order_data(data):
    """
        active order = 0,
        cancelled order = 2, completed = 1
    """
    #print(data)
    global eventType
    global paytype_reverse
    active = {}
    complete = {}
    cancelled = {}
    lookup = menu_process()
    for item in data:
        temp = {}
        id = item[0]
        temp["budget"] = item[1]
        temp["capacity"] = item[2]
        temp["eventtype"] = eventType[str(item[3])]
        temp["opentime"] = item[4]
        temp["closetime"] = item[5]
        temp["location"] = item[6]
        temp["customization"] = item[7]
        temp["delivery"] = item[8]
        temp["venueid"] = item[10]
        temp["billingaddr"] = item[11]
        temp["status"] = item[12]
        temp["paidamount"] = item[14]
        temp["paid"] = paytype_reverse[int(item[15])]
        temp["orderNum"] = item[17]
        temp["userid"] = item[20]
        try:
            temp["password"] = item[22]
            temp["name"] = item[23] + " " + item[24]
            temp["phone"] = item[25]
            temp["email"] = item[26]
            temp["addr"] = item[27]
            temp["postal"] = item[28]
        except:
            pass
        orderitem = item[13].split(" ")
        order =""
        for x in orderitem:
            if x == "":
                break
            if int(x[x.find("-")+1:]) != 0:
                s = lookup[x[:x.find("-")]] + ": qty:" + x[x.find("-")+1:] + " "
                order += s
        temp["order"] = order
        if int(temp["status"]) == 0:
            temp["status_en"] = "Active/Pending"
            active[id] = temp
        elif int(temp["status"]) == 1:
            temp["status_en"] = "Completed"
            complete[id] = temp
        else:
            temp["status_en"] = "Cancelled"
            cancelled[id] = temp

    #print(active)
    #print(complete)
    #print(cancelled)
    return active, complete, cancelled #k v pairs



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
    """
        active order = 1, pending order = 0,
        cancelled order = 2, completed = 3
    """
    global username
    active,complete,cancelled = process_order_data(join_Order_Event(username))
    if request.method == 'GET':
        return render_template('userDashboard.html', active=active, complete=complete, cancelled=cancelled)
    else:
        if "cancel" in request.form:
            orderNum = request.form['cancel']
            update_db("OrderInfo", "isComplete=2", "Order_number='" + str(orderNum) + "'")
            return redirect(url_for('userDashboard'))
        else:
            return redirect(url_for('dashboard'))

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
    global username
    active,complete,cancelled = process_order_data(join_customer_order_event())
    count_active = len(active)
    count_complete = len(complete)
    count_cancel = len(cancelled)
    if request.method == 'GET':
        return render_template('adminDashboard.html', active=active, complete=complete, \
                                cancelled=cancelled, count_cancel=count_cancel, \
                                count_complete=count_complete, count_active=count_active)
    else:
        if "edit1submit" in request.form:
            id = request.form['edit1submit']
            target = request.form['info1']
            select = request.form.get('options1')
            try:
                update_db("Event", str(select) + "='" + str(target) +"'", "Event_id='" + str(id) + "'")
            except:
                try:
                    update_db("Event", str(select) + "=" + str(target), "Event_id='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))
        if "edit2submit" in request.form:
            id = request.form['edit2submit']
            target = request.form['info2']
            select = request.form.get('options2')
            try:
                update_db("OrderInfo", str(select) + "='" + str(target) +"'", "Order_number='" + str(id) + "'")
            except:
                try:
                    update_db("OrderInfo", str(select) + "=" + str(target), "Order_number='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))
        if "edit3submit" in request.form:
            id = request.form['edit3submit']
            target = request.form['info3']
            select = request.form.get('options3')
            try:
                update_db("Customer", str(select) + "='" + str(target) +"'", "UserId='" + str(id) + "'")
            except:
                try:
                    update_db("Customer", str(select) + "=" + str(target), "UserId='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))
        if "edit4submit" in request.form:
            id = request.form['edit4submit']
            target = request.form['info4']
            select = request.form.get('options4')
            try:
                update_db("Event", str(select) + "='" + str(target) +"'", "Event_id='" + str(id) + "'")
            except:
                try:
                    update_db("Event", str(select) + "=" + str(target), "Event_id='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))
        if "edit5submit" in request.form:
            id = request.form['edit5submit']
            target = request.form['info5']
            select = request.form.get('options5')
            try:
                update_db("OrderInfo", str(select) + "='" + str(target) +"'", "Order_number='" + str(id) + "'")
            except:
                try:
                    update_db("OrderInfo", str(select) + "=" + str(target), "Order_number='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))
        if "edit6submit" in request.form:
            id = request.form['edit6submit']
            target = request.form['info6']
            select = request.form.get('options6')
            try:
                update_db("Customer", str(select) + "='" + str(target) +"'", "UserId='" + str(id) + "'")
            except:
                try:
                    update_db("Customer", str(select) + "=" + str(target), "UserId='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))

        if "edit7submit" in request.form:
            id = request.form['edit7submit']
            target = request.form['info7']
            select = request.form.get('options7')
            try:
                update_db("Event", str(select) + "='" + str(target) +"'", "Event_id='" + str(id) + "'")
            except:
                try:
                    update_db("Event", str(select) + "=" + str(target), "Event_id='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))
        if "edit8submit" in request.form:
            id = request.form['edit8submit']
            target = request.form['info8']
            select = request.form.get('options8')
            try:
                update_db("OrderInfo", str(select) + "='" + str(target) +"'", "Order_number='" + str(id) + "'")
            except:
                try:
                    update_db("OrderInfo", str(select) + "=" + str(target), "Order_number='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))
        if "edit9submit" in request.form:
            id = request.form['edit9submit']
            target = request.form['info9']
            select = request.form.get('options9')
            try:
                update_db("Customer", str(select) + "='" + str(target) +"'", "UserId='" + str(id) + "'")
            except:
                try:
                    update_db("Customer", str(select) + "=" + str(target), "UserId='" + str(id) + "'")
                except:
                    flash("Error! update to table generates an error. Please provide correct syntax.")
                    return redirect(url_for('adminDashboard'))


        if "delete1submit" in request.form:
            orderNum = request.form['delete1submit']
            delete_db("OrderInfo", "Order_number='" + str(orderNum) + "'")
        if "delete2submit" in request.form:
            orderNum = request.form['delete2submit']
            delete_db("OrderInfo", "Order_number='" + str(orderNum) + "'")
        if "delete3submit" in request.form:
            orderNum = request.form['delete3submit']
            delete_db("OrderInfo", "Order_number='" + str(orderNum) + "'")
        

        return redirect(url_for('adminDashboard'))

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
