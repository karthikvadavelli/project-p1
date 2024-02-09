from google.cloud import bigquery
from google.oauth2 import service_account
import json
import os
# from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError
from getpass import getpass
credentials="C:\\Users\\Karthik\\p1_project\\json_con.json"
client = bigquery.Client.from_service_account_json(credentials)
project_id ='theta-cell-406519'

dataset_name = 'karthik_rev_stox'  # Replace with your dataset name

# Initialize BigQuery client
# try:
#     client = bigquery.Client()
# except DefaultCredentialsError:
#     print("Error: Please make sure you have set up your Google Cloud credentials.")
#     exit()

# Function to register a new user
def register_user():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    try:
        # Insert the user into the users table with default role 'normal_user'
        query = f"INSERT INTO `{project_id}.{dataset_name}`.users (username, password, role) VALUES ('{username}', '{password}', 'normal_user')"
        client.query(query).result()

        print("User registration successful! Role: normal_user")
    except Exception as e:
        print(f"Error: {e}\nUser registration failed.")

# Function to register a new admin
def register_admin():
    admin_username = input("Enter admin username: ")
    admin_password = getpass("Enter admin password: ")

    try:
        # Insert the admin into the users table with role 'iam_admin'
        query = f"INSERT INTO `{project_id}.{dataset_name}`.users (username, password, role) VALUES ('{admin_username}', '{admin_password}', 'iam_admin')"
        client.query(query).result()

        print("Admin registration successful! Role: iam_admin")
    except Exception as e:
        print(f"Error: {e}\nAdmin registration failed.")

# Function for admin login and CRUD operations
def admin_login():
    admin_username = input("Enter admin username: ")
    admin_password = getpass("Enter admin password: ")

    # Check if the admin exists and has the correct role
    query = f"SELECT * FROM `{project_id}.{dataset_name}`.users WHERE username='{admin_username}' AND password='{admin_password}' AND role='iam_admin'"
    admin = client.query(query).result()

    if admin:
        print("Admin login successful!")

        # Perform CRUD operations
        while True:
            print("\n1. Create Record")
            print("2. Read Records")
            print("3. Update Record")
            print("4. Delete Record")
            print("5. Back")

            operation = input("Select an operation (1/2/3/4/5): ")

            if operation == '1':
                create_record()
            elif operation == '2':
                read_records()
            elif operation == '3':
                update_record()
            elif operation == '4':
                delete_record()
            elif operation == '5':
                break
            else:
                print("Invalid operation. Please enter 1, 2, 3, 4, or 5.")
    else:
        print("Invalid admin username or password.")

# Function to authenticate a normal user
def normal_user_login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    # Check if the user exists and has the correct role
    query = f"SELECT * FROM `{project_id}.{dataset_name}`.users WHERE username='{username}' AND password='{password}' AND role='normal_user'"
    user = client.query(query).result()

    if user:
        print(f"Login successful! Role: normal_user")

    else:
        print("Invalid username or password.")

# CRUD operations on wipro table
def create_record():
    # Assume you want to add a new record to data_table
    date = input("Enter Date: ")
    prev_close = float(input("Enter Prev_Close: "))
    open_value = float(input("Enter Open: "))
    high = float(input("Enter High: "))
    low = float(input("Enter Low: "))
    last = float(input("Enter Last: "))
    close = float(input("Enter Close: "))
    vwap = float(input("Enter VWAP: "))
    volume = int(input("Enter Volume: "))
    turnover = float(input("Enter Turnover: "))

    try:
        # Insert the record into data_table
        query = f"INSERT INTO `{project_id}.{dataset_name}`.wipro (Date, Prev_Close, Open, High, Low, Last, Close, VWAP, Volume, Turnover) " \
                f"VALUES ('{date}', {prev_close}, {open_value}, {high}, {low}, {last}, {close}, {vwap}, {volume}, {turnover})"
        client.query(query).result()

        print("Record added successfully!")
    except Exception as e:
        print(f"Error: {e}\nRecord creation failed.")

def read_records():
    # Read all records from data_table
    query = f"SELECT * FROM `{project_id}.{dataset_name}`.wipro"
    records = client.query(query).result()

    # Display records
    for record in records:
        print(record)

def update_record():
    record_id = int(input("Enter the ID of the record to update: "))
    new_prev_close = float(input("Enter the new Prev_Close: "))
    new_open = float(input("Enter the new Open: "))
    new_high = float(input("Enter the new High: "))
    new_low = float(input("Enter the new Low: "))
    new_last = float(input("Enter the new Last: "))
    new_close = float(input("Enter the new Close: "))
    new_vwap = float(input("Enter the new VWAP: "))
    new_volume = int(input("Enter the new Volume: "))
    new_turnover = float(input("Enter the new Turnover: "))

    try:
        # Update the record in data_table
        query = f"UPDATE `{project_id}.{dataset_name}`.wipro SET " \
                f"Prev_Close={new_prev_close}, Open={new_open}, High={new_high}, Low={new_low}, Last={new_last}, " \
                f"Close={new_close}, VWAP={new_vwap}, Volume={new_volume}, Turnover={new_turnover} " \
                f"WHERE id={record_id}"
        client.query(query).result()

        print("Record updated successfully!")
    except Exception as e:
        print(f"Error: {e}\nRecord update failed.")

def delete_record():
    record_id = int(input("Enter the ID of the record to delete: "))

    try:
        # Delete the record from data_table
        query = f"DELETE FROM `{project_id}.{dataset_name}`.wipro WHERE id={record_id}"
        client.query(query).result()

        print("Record deleted successfully!")
    except Exception as e:
        print(f"Error: {e}\nRecord deletion failed.")

# Main program
while True:
    print("\n1. Register User")
    print("2. Register Admin")
    print("3. Admin Login")
    print("4. Normal User Login")
    print("5. Exit")

    choice = input("Select an option (1/2/3/4/5): ")

    if choice == '1':
        register_user()
    elif choice == '2':
        register_admin()
    elif choice == '3':
        admin_login()
    elif choice == '4':
        normal_user_login()
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, 5.")
