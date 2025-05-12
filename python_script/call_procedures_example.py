import pandas as pd
import mysql.connector 
from datetime import datetime

DB_HOST = "localhost"
DB_USER = "user" 
DB_PASSWORD = "Password@" 
DB_NAME = "littlelemon"

def call_add_booking(cursor, booking_id, order_date, delivery_date, customer_id, delivery_cost):
    try:
        cursor.callproc('AddBooking', [booking_id, order_date, delivery_date, customer_id, delivery_cost])
        print(f"Called AddBooking for {booking_id}.")
        # Stored procedures might return results; fetch them if necessary
        for result in cursor.stored_results():
            print(result.fetchall())
        mydb.commit() # Commit if AddBooking performs DML
    except mysql.connector.Error as err:
        print(f"Error calling AddBooking: {err}")

def call_get_max_quantity(cursor):
    try:
        cursor.callproc('GetMaxQuantity')
        print("Called GetMaxQuantity.")
        for result in cursor.stored_results():
            print("Max Quantity:", result.fetchone()[0]) # Accessing the first column of the first row
    except mysql.connector.Error as err:
        print(f"Error calling GetMaxQuantity: {err}")

  # Example Usage
try:
    mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = mydb.cursor()
 
    # # Ensure customer 'CUST-NEW' exists for AddBooking example
    # cursor.execute("INSERT IGNORE INTO Customers (CustomerID, CustomerName) VALUES ('CUST-NEW', 'New Python Customer')")
    # mydb.commit()
    # call_add_booking(cursor, 'PY-ORDER-001', '2025-06-01', '2025-06-02', 'CUST-NEW', 12.00)
    
    call_get_max_quantity(cursor)

except mysql.connector.Error as e:
    print(f"Database connection error: {e}")
finally:
    if 'mydb' in locals() and mydb.is_connected():
        cursor.close()
        mydb.close()
      
