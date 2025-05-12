import pandas as pd
import mysql.connector 
from datetime import datetime

DB_HOST = "localhost"
DB_USER = "user" 
DB_PASSWORD = "password@" 
DB_NAME = "littlelemon"

excel_file_path = 'LittleLemon_data.xlsx' # Make sure this file is in the same directory
df = pd.read_excel(excel_file_path).dropna()

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        try:
            # Add other formats if necessary or handle invalid dates
            return pd.to_datetime(date_str).strftime('%Y-%m-%d')
        except Exception:
            return None # Or a default date

df['Order Date'] = df['Order Date'].apply(parse_date)
df['Delivery Date'] = df['Delivery Date'].apply(parse_date)

# Rename columns to match DB schema
df.rename(columns={
    'Order ID': 'BookingID_Excel', #
    'Customer ID': 'CustomerID',
    'Customer Name': 'CustomerName',
    'Postal Code': 'PostalCode',
    'Country Code': 'CountryCode',
    ' Cost': 'ItemCost', # Note the spaces in the original column name
    'Sales': 'ItemSales',
    'Quantity': 'Quantity',
    'Discount': 'Discount',
    'Delivery Cost': 'DeliveryCost_Excel', # Temporary
    'Course Name': 'CourseName',
    'Cuisine Name': 'CuisineName',
    'Starter Name': 'StarterName',
    'Desert Name': 'DesertName',
    'Drink': 'Drink',
    'Sides': 'Sides'
}, inplace=True)

try:
    mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = mydb.cursor()
    print("Successfully connected to database.")
    
    # --- Populate Customers Table (unique customers) ---
    customers_df = df[['CustomerID', 'CustomerName', 'City', 'Country', 'PostalCode', 'CountryCode']].drop_duplicates(subset=['CustomerID'])
    customer_sql = "INSERT IGNORE INTO Customers (CustomerID, CustomerName, City, Country, PostalCode, CountryCode) VALUES (%s, %s, %s, %s, %s, %s)"
    for index, row in customers_df.iterrows():
        cursor.execute(customer_sql, tuple(row))
    print(f"{cursor.rowcount} customers inserted or already exist.")
    
    # --- Populate Bookings Table (unique orders) ---
    # The Excel BookingID is called 'Order ID'
    bookings_df = df[['BookingID_Excel', 'Order Date', 'Delivery Date', 'CustomerID', 'DeliveryCost_Excel']].drop_duplicates(subset=['BookingID_Excel'])
    booking_sql = "INSERT IGNORE INTO Bookings (BookingID, OrderDate, DeliveryDate, CustomerID, DeliveryCost) VALUES (%s, %s, %s, %s, %s)"
    for index, row in bookings_df.iterrows():
        # Handle potential NaT values for dates if parse_date returned None
        order_date = row['Order Date'] if pd.notna(row['Order Date']) else None
        delivery_date = row['Delivery Date'] if pd.notna(row['Delivery Date']) else None
        cursor.execute(booking_sql, (row['BookingID_Excel'], order_date, delivery_date, row['CustomerID'], row['DeliveryCost_Excel']))
    print(f"{cursor.rowcount} bookings inserted or already exist.")
    
    # --- Populate OrderItems Table ---
    order_items_sql = """
    INSERT INTO OrderItems
    (BookingID, CourseName, CuisineName, StarterName, DesertName, Drink, Sides, ItemCost, ItemSales, Quantity, Discount)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for index, row in df.iterrows():
        cursor.execute(order_items_sql, (
            row['BookingID_Excel'], row['CourseName'], row['CuisineName'], row['StarterName'],
            row['DesertName'], row['Drink'], row['Sides'], row['ItemCost'],
            row['ItemSales'], row['Quantity'], row['Discount']
        ))
    print(f"{cursor.rowcount} order items inserted.")
    
    mydb.commit()
    print("Data population complete.")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'mydb' in locals() and mydb.is_connected():
        cursor.close()
        mydb.close()
        print("MySQL connection is closed.")

  
