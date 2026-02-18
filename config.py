import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysqlpassword", 
        database="climacore_db"
    )
    return connection
