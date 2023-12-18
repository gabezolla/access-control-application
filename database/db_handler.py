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

# ChatIds        
def saveChatId(chat_id):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO chat_ids (chat_id) VALUES (%s)"
            values = (chat_id,)
            cursor.execute(sql, values)
            connection.commit()
            print(f"Data successfully saved.")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()

def getChatIdsFromDatabase():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "SELECT chat_id FROM chat_ids"
            cursor.execute(sql)
            results = cursor.fetchall()
            chatIds = []
            for result in results:
                chatIds.append(result[0])
            return chatIds
        except mysql.connector.Error as error:
            print(f"Error retrieving chatIds: {error}")
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
            return {'mensagem': 'Encoding successfully deleted'}
        except mysql.connector.Error as error:
            print(f"Error retrieving data: {error}")
        finally:
            cursor.close()
            connection.close()

    return encodings

def authenticateUser(username, password):
    connection = connect()
    
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            sql = "SELECT users.id, users.type_id, users_type.type FROM users JOIN users_type ON users.type_id = users_type.id WHERE users.login = %s AND users.password = %s"
            values = (username, password)
            cursor.execute(sql, values)
            user_data = cursor.fetchone()
            
            if user_data:
                return user_data
            else:
                return None
        except mysql.connector.Error as error:
            print(f"Error retrieving data: {error}")
        finally:
            cursor.close()
            connection.close()
    return None

def searchForAdmin():
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "SELECT users.id, users.type_id, users_type.type FROM users JOIN users_type ON users.type_id = users_type.id WHERE users_type.type = 'admin'"
            cursor.execute(sql)
            user_data = cursor.fetchone()
                        
            if user_data:
                return user_data
            else:
                return None
        except mysql.connector.Error as error:
                print(f"Error retrieving data: {error}")
        finally:
            cursor.close()
            connection.close()
        return None
    


    