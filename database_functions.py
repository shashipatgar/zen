import mysql.connector
from mysql.connector import Error
from tkinter import messagebox


# Function to create a connection to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            database='Zenmeter_Process_Data'  # Replace with your database name
        )
        return connection
    except Error as e:
         messagebox.showerror("Server Connection Error", f"Failed to connect to database.\nError: {e}")
    

# Function to insert test results into the MySQL database
def insert_test_result(serial_number,pcba_number, status, pc_name, problem, failure_stage):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = '''INSERT INTO Rework_Debug (serial_number,pcba_number, status, pc_name, problem, failure_stage) 
                       VALUES (%s, %s, %s, %s, %s, %s)'''
            data = (serial_number,pcba_number, status, pc_name, problem, failure_stage)
            cursor.execute(query, data)
            connection.commit()
            print("Test result inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        connection.rollback()


# Function to query test results from MySQL database
def query_test_result(serial_number, pcba_number):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
                SELECT serial_number, pcba_number, status, failure_stage, problem,pc_name,test_time FROM Rework_Debug WHERE serial_number = %s OR pcba_number = %s
            """
            cursor.execute(query, (serial_number, pcba_number))
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    else:
        connection.rollback()
