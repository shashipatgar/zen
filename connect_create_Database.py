import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def verify_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            database='Zenmeter_Process_Data'  # Replace with your database name
        )
        if connection.is_connected():
            messagebox.showinfo("Success", "Database connection successful!")
        return connection
    except Error as e:
        messagebox.showerror("Connection Error", f"Failed to connect to database.\nError: {e}")
        return None

# Connect to MySQL server and create database if not exists
def create_server_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password='root'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection, db_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rework_Debug (
            id INT AUTO_INCREMENT PRIMARY KEY,
            serial_number VARCHAR(25) NOT NULL,
            pcba_number VARCHAR(20) NOT NULL,
            status VARCHAR(50) NOT NULL,
            failure_stage TEXT,
            problem TEXT,
            test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pc_name VARCHAR(255) NOT NULL,
            UNIQUE(serial_number, pcba_number)
        )
        ''')
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

# Connect to MySQL server and create the database and table
connection = create_server_connection()
if connection:
    create_database(connection, 'Zenmeter_Process_Data')
    connection.database = 'Zenmeter_Process_Data'
    create_table(connection)
    connection.close()

