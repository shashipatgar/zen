import mysql.connector
from mysql.connector import Error

# Function to create a connection to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',  # Replace with your MySQL username
            password='your_password',  # Replace with your MySQL password
            database='test_db'  # Replace with your database name
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to insert test results into the MySQL database
def insert_test_result(serial_number,PCBA_Number, status, pc_name, problem, Failure_stage):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = '''INSERT INTO test_results (serial_number,PCBA_Number, status, pc_name, problem, failure_reason) 
                       VALUES (%s, %s, %s, %s, %s, %s)'''
            data = (serial_number,PCBA_Number, status, pc_name, problem, Failure_stage)
            cursor.execute(query, data)
            connection.commit()
            print("Test result inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to query test results from MySQL database
def query_test_result(serial_number):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = "SELECT serial_number, status, failure_reason, problem, pc_name, test_time FROM test_results WHERE serial_number = %s"
            cursor.execute(query, (serial_number,))
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
