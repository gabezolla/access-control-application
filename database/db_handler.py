from flask import jsonify
import mysql.connector
import uuid
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

# Notifications
def saveNotification(type, contact):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            id = str(uuid.uuid4())
            sql = "INSERT INTO notifications (type, contact) VALUES (%s, %s, %s)"
            values = (id, type, contact)
            cursor.execute(sql, values)
            connection.commit()
            print(f"Data successfully saved.")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()
            
def getNotifications():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "SELECT * FROM notifications"
            cursor.execute(sql)
            results = cursor.fetchall()
            notifications = []
            for result in results:
                notification = {
                    "id": result[0],
                    "type": result[1],
                    "contact": result[2]
                }
                notifications.append(notification)
            return notifications
        except mysql.connector.Error as error:
            print(f"Error retrieving notifications: {error}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database")

# Encodings
def saveEncoding(name, encoding):
    connection = connect()
    if connection:
        try:
            id = str(uuid.uuid4())
            cursor = connection.cursor()
            sql = "INSERT INTO encodings (id, name, encoding) VALUES (%s, %s, %s)"
            values = (id, name, encoding)
            cursor.execute(sql, values)
            connection.commit()
            print("Data successfully saved")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()

def getEncodingsFromDatabase():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "SELECT name, encoding FROM encodings"
            cursor.execute(sql)
            results = cursor.fetchall()
            names = [result[0] for result in results]
            encodings = [result[1] for result in results]
            return names, encodings
        except mysql.connector.Error as error:
            print(f"Error retrieving encodings: {error}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database")
    return [], []
            
def deleteEncodings(id):
    connection = connect()
    encodings = []

    if connection:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM encodings WHERE id = %s"
            values = (id,)
            cursor.execute(sql, values)
            connection.commit()
            cursor.close()
            connection.close()
            return {'mensagem': 'Encoding deletado com sucesso'}
        except mysql.connector.Error as error:
            print(f"Error retrieving data: {error}")
        finally:
            cursor.close()
            connection.close()

    return encodings

    