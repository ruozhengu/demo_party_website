import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "cs348348",
    database = "perfect_party"
)

print("Connection to DB: perfect_party")

cursor = db.cursor()

schema_customer = "INSERT INTO perfect_party.Customer (UserId,\
                            Password, \
                            Firstname, \
                            Lastname, \
                            Phone, \
                            Email, \
                            Address, \
                            Postalcode) VALUES \
                            (%s, %s, %s, %s, %s, %s, %s, %s)"


schema_order = "INSERT INTO perfect_party.OrderInfo ( Billingaddr, \
                    Iscomplete ,\
                    Orderitem ,\
                    Paidamount ,\
                    Ispaid ,\
                    Paidtype ,\
                    Order_number ,\
                    Cardtype ,\
                    Event_id ,\
                    UserId ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

schema_event = "INSERT INTO  perfect_party.Event (Event_id , \
                    Budget , \
                    Capacity , \
                    Event_Type , \
                    Party_open_time , \
                    Party_close_time , \
                    Location , \
                    Customization , \
                    Delivery_time , \
                    Product_ID , \
                    Supplier_ID , \
                    Transaction , \
                    UserId , \
                    Venue_id ) VALUES \
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

def insert_db(table, schema, value):
    """
        Insert record into table
        Args: value is tuple, table and schema are strings
    """
    cursor.execute(schema, value)
    db.commit()
    print(cursor.rowcount, "record inserted into db: " + table)

def select_db(table, cond):
    """
        Select all columns from table based on cond
        Args: all strings
        Return: records are list of tuples

    """
    query = "SELECT * FROM " + table + " WHERE " + cond
    cursor.execute(query)
    records = cursor.fetchall()
    return records

def delete_db(table, cond):
    """
        Delete matching rows from table based on cond
        Args: all strings
    """
    query = "DELETE FROM " + table + " WHERE " + cond
    cursor.execute(schema, value)
    db.commit()
    print(cursor.rowcount, "record deleted from db: " + table)


def update_db(table, set, wherecond):
    """
        Update matching rows from table based on cond
        Args: all strings
    """
    query = "UPDATE " + table + " SET " + set + " WHERE " + cond
    cursor.execute(schema, value)
    db.commit()
    print(cursor.rowcount, "record updated in db: " + table)
