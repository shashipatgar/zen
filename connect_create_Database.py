import mysql.connector
from mysql.connector import Error

# Function to create a connection to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            user='your_username',  # Replace with your MySQL username
            password='your_password',  # Replace with your MySQL password
            database='test_db'  # Replace with your database name
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Connect to MySQL database
conn = create_connection()

if conn:
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table to store test results
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        serial_number VARCHAR(255) NOT NULL,
        status VARCHAR(50) NOT NULL,
        failure_reason TEXT,
        test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        pc_name VARCHAR(255) NOT NULL,
        UNIQUE(serial_number, status, test_time)
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
else:
    print("Failed to connect to the database")
