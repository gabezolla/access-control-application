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
def saveEncoding(name, encoding, guid):
    connection = connect()
    if connection:
        try:
            id = str(uuid.uuid4())
            cursor = connection.cursor()
            sql = "INSERT INTO encodings (id, name, encoding, user_id) VALUES (%s, %s, %s, %s)"
            values = (id, name, encoding, guid)
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

# Users
def saveUser(id, user_type, login="", password=""):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            
            type_sql = "INSERT INTO users_type (id, type) VALUES (%s, %s)"
            type_values = (id, user_type)
            
            user_sql = "INSERT INTO users (id, login, password, type_id) VALUES (%s, %s, %s, %s)"
            user_values = (id, login, password, id)
            
            cursor.execute(type_sql, type_values)
            cursor.execute(user_sql, user_values)
            connection.commit()
            print("Data successfully saved")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()

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
    
# Logs - Devices
def registerLog(device_id, time, identified_user, accuracy):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            select = f"SELECT user_id FROM encodings where name = '{identified_user}'"
            cursor.execute(select)
            user_id = cursor.fetchone()
            
            if not user_id:
                user_id = ""
            
            log_id = str(uuid.uuid4())
            
            sql = "INSERT INTO devices_logs (log_id, device_id, time, user_id, accuracy) VALUES (%s, %s, %s, %s, %s)"
            values = (log_id, device_id, time, user_id, accuracy)
            
            cursor.execute(sql, values)
            connection.commit()
            print("Data successfully saved")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()
            
def registerDevice(deviceId):
    connection = connect()
    if connection:
        try:
            id = str(uuid.uuid4())
            cursor = connection.cursor()
            sql = "INSERT INTO devices (id) VALUES (%s)"
            values = (id,)
            cursor.execute(sql, values)
            connection.commit()
            print("Data successfully saved")
        except mysql.connector.Error as error:
            print(f"Error saving data: {error}")
        finally:
            cursor.close()
            connection.close()