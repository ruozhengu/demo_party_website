
import mysql.connector as mysql

## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "cs348348"
)

print("======= Display DB =======")

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

## creating a databse called 'datacamp'
## 'execute()' method is used to compile a 'SQL' statement
## below statement is used to create tha 'datacamp' database
try: # if db not created
    cursor.execute("CREATE DATABASE perfect_party")
    print("DB: perfect_party is created.")
except:
    print("DB: perfect_party exists.")



db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "cs348348",
    database = "perfect_party"
)

print("Connection to DB: perfect_party")

cursor = db.cursor()

cursor.execute("SHOW TABLES")

tables = cursor.fetchall() ## it returns list of tables present in the database

## showing all the tables one by one
print("======= print existing tables: =======")
for table in tables:
    print(table)

print("===== Create Tables if miss any: =====")

## creating a table called 'users' in the 'datacamp' database

try:
    cursor.execute("CREATE TABLE OrderInfo( Billingaddr varchar(255) Not NULL, \
                Iscomplete int, \
                Orderitem varchar(255) Not NULL, \
                Paidamount int Not NULL Constraint price_check4 check(Paidamount >= 0), \
                Ispaid bool Not NULL, \
                Paidtype int Not NULL, \
                Order_number char(6) primary key, \
                Cardtype int Not NULL,\
                Event_id char(6) not null, \
                UserId char(6) not null, \
                foreign key (Event_id) references Event(Event_id) on delete cascade, \
                foreign key (UserId) references Customer(UserId) on delete cascade)")
    print("OrderInfo table is created.")
except:
    print("OrderInfo table exists.")

try:
    cursor.execute("CREATE TABLE Customer (\
                    UserId char(6) primary key, \
                    Password varchar(max) NOT NULL, \
                    Firstname varchar(max) NOT NULL, \
                    Lastname varchar(max) NOT NULL, \
                    Phone varchar(max), \
                    Email varchar(max), \
                    Address varchar(max), \
                    Postalcode varchar(max)")
    print("Customer table is created.")
except:
    print("Customer table exists.")

try:
    cursor.execute("CREATE TABLE Venue (\
                    Venue_id char(6) primary key, \
                    Capacity int NOT NULL Constraint Capacity_check check(Capacity >= 0 and Capacity <= 10000), \
                    Location varchar(255), \
                    Postal_code varchar(7),\
                    unique (Venue_id))")
    print("Venue table is created.")
except:
    print("Venue table exists.")

try:
    cursor.execute("create table Supplier( \
                    Supplier_ID Varchar(6) primary key, \
                    Phone char(10), \
                    Supplier_name Varchar(12), \
                    Company_name Varchar(15), \
                    Company_Address Varchar(255), \
                    Email varchar(255))")

    print("Supplier table is created.")
except:
    print("Supplier table exists.")

try:
    cursor.execute("create table Supply_record ( \
                Supplier_ID char(6) primary key, \
                Transaction char(6), \
                Product_ID char(6), \
                Price decimal(8,2) Not NULL \
                Constraint Price_check check(Price >= 0), \
                Quantity int Not NULL \
                Constraint Quantity_check check(Quantity >= 0),\
                foreign key (Supplier_ID) references Supplier(Supplier_ID) )")
    print("Supply_record table is created.")
except:
    print("Supply_record table exists.")

try:
    cursor.execute("create table Menu( \
                Product_ID char(6) Not NULL , \
                Description Varchar(255), \
                Price Decimal(8,2), \
                Constraint Price_check2 check(Price >= 0),\
                Quantity int not null, \
                Constraint Quantity_check2 check(Quantity >= 0))")
    print("Menu table is created.")
except:
    print("Menu table exists.")

try:
    cursor.execute("CREATE TABLE Event (\
                    Event_id char(6) primary key, \
                    Budget decimal(8,2) not null, \
                    Capacity int NOT NULL Constraint Capacity_check3 check(Capacity >= 0 and Capacity <= 10000), \
                    Event_Type int NOT NULL, \
                    Party_open_time timestamp NOT NULL, \
                    Party_close_time timestamp NOT NULL, \
                    Location varchar(255), \
                    Customization varchar(255), \
                    Delivery_time TIME NOT NULL , \
                    Product_ID char(6) not null, \
                    Supplier_ID char(6) unique, \
                    Transaction Varchar(255), \
                    UserId char(6) not null, \
                    Venue_id char(6) not null, \
                    foreign key (Venue_id) references Venue(Venue_id), \
                    foreign key (UserId) references Customer(UserId) on delete cascade)")
    print("Event table is created.")
except:

    print("Event table exists.")

try:
    cursor.execute("create table music_entertainment ( \
             Supplier_id char(6) not null unique, \
             Transaction char(6) not null unique, \
             Music_taste varchar(255), \
             foreign key (Supplier_ID) references Supply_record(Supplier_ID))")
    print("music_entertainment table is created.")
except:

    print("music_entertainment table exists.")

try:
    cursor.execute("create table Flowers_dtor ( \
                    Supplier_id char(6) not null unique, \
                    Transaction char(6) not null unique, \
                    Flower_name varchar(255) Not NULL, \
                    Flower_colour varchar(255) Not NULL, \
                    foreign key (Supplier_ID) references Supply_record(Supplier_ID))")
    print("Flowers_dtor table is created.")
except:

    print("Flowers_dtor table exists.")


print("======================================")
