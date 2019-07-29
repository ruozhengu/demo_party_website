## "Perfect Party Company" Web Application


#### 1. Technology and File Description

_`the_perfect_party` is a website demo created for CS348 course at University of Waterloo._

--

**The main features listed below:**

**Customer Side:**

* Interactice dashboard created using Javascript
* Reponsive shopping cart with real-time tax, shipping, subtotal price calculation
* Automatic customer information fillin and order status verification
* Customer's ability to delete, escalate any exisiting order infomration
* Customer login and signup support with validation

**Administrator Side:**

* Secure login page
* All in one infomormation displayed by each order creation time and status
* Active order notification system
* Search engine based on customer username
* Modification, Escalation, Deletion and Insertion of any past/new orders or events
* Supplier and Stock availability monitoring and modification support.

--
**Technology Breakdown:**

Backend: `/app.py`

`the_perfect_party` web app is deployed as a `flask app` with backend written in `python` and connected through `GET` & `POST` requests with frontend.

Frontend: `/templates/*`

Adopted traditional frontend technology including: `JQuery(JS)`, `HTML`,`CSS` with stylesheet from `Twitter Boostrap`

Database: `/dbConnect.py` and `/db_helper.py`

Connected with a `Mysql` server through `mysql.connector`

#### 2. File Hierarchy Visualization
<pre>
the_perfect_party/
├─── app.py                     
├─── dbConnect.py		   
├─── db_helper.py				    
├─── templates/
│    ├─── admin.html
│    ├─── adminDashboard.html
│    ├─── dashboard.html
│    ├─── event.html
│    ├─── index.html
│    ├─── login.html
│    ├─── login2.html
│    ├─── order.html
│    ├─── payment.html
│    ├─── shoppingcart.html
│    ├─── success.html
│    ├─── supplier.html
│    ├─── supplyRecord.html
│    ├─── userDashboard.html
│    └─── orderInfo.html
├─── static
│    ├─── .. contain all javascript files ..
│    └─── .. contain all css files ..
├─── bootstrap/
├─── env/
├─── requirements.txt
...
</pre>


#### 3. SQL Demonstration

Three are three main parts of SQL code to demonstrate. **_Please refer to file `dbConnect.py` and `db_helper,py` for details._**

1. Database and table creation query
2. Creation, deletion and update operations on record
3. Select operations with/without specific conditions

--


