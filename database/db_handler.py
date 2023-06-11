import mysql.connector
import json

def connect():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="control-access"
        )
        
        print("Successfully connected to database")
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to database: {error}")
        return None

def saveNotification(type, contact):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO notifications (type, contact) VALUES (%s, %s)"
            values = (type, contact)
            cursor.execute(sql, values)
            inserted_id = cursor.lastrowid
            connection.commit()
            print(f"Data successfully saved. Id: {inserted_id}")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()

def saveEncoding(name, encoding):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO encodings (name, encoding) VALUES (%s, %s)"
            values = (name, encoding)
            cursor.execute(sql, values)
            connection.commit()
            print("Data successfully saved")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()