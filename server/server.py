from flask import Flask, request, jsonify
from telethon import TelegramClient
from database.db_handler import *
from database.encoding_service import storeFace
from server.message_handler import getChatsIds, sendMessage
import os
import uuid

app = Flask(__name__)

@app.route('/api/encodings', methods=['GET'])
def getEncodings():
    names, encodings = getEncodingsFromDatabase()
    encodings_dict = {"names": names, "encodings": encodings}
    return jsonify(encodings_dict)    

# Change route and everything else to 'user' instead of 'photos'
@app.route('/api/photos', methods=['POST'])
def registerPhoto():
    name = request.form.get('name') # TODO: Change all .form. into .json.
    user_type = request.form.get('user_type')
    image = request.files.get('image')
    guid = str(uuid.uuid4())

    if image:
        path = f'user-data/{name}/'
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        full_path = path + f"{len(os.listdir(path)) + 1}.png"
        image.save(full_path)
        
        saveUser(guid, user_type.lower())        
        storeFace(full_path, name, guid)

        return {'mensagem': 'Foto cadastrada com sucesso'}
    else:
        return {'mensagem': 'Nenhuma imagem foi enviada'}, 400
    
@app.route('/api/photos/<name>/files/<filename>', methods=['DELETE'])
def deletePhoto(name, filename):
    path = f'user-data/{name}/{filename}'

    if os.path.exists(path):
        os.remove(path)
        return {'mensagem': 'Foto deletada com sucesso'}
    else:
        return {'mensagem': 'Foto não encontrada'}, 404

@app.route('/api/notifications', methods=['POST'])
def registerNotification():
    accepted_types = ['telegram']
    type = request.form.get("type")
    contact = request.form.get("contact")
        
    if not type or not contact: 
        return {'mensagem': 'Campo type ou contact não enviado'}, 400

    if type in accepted_types:
        saveNotification(type, contact)
        return {'mensagem': 'Notificação registrada com sucesso'}, 201        
        
    else:
        return {'mensagem': 'Tipo de notificação não permitido'}, 400
    
# TODO: handle errors with database
@app.route('/api/notifications/telegram', methods=['POST'])
def registerChatId():
    chatId = request.json.get("chat_id")
    if not chatId:
        chatId = getChatsIds()
    
    if not chatId or chatId is int:
       return {'mensagem': 'Nenhum chat_id encontrado'}, 404 
          
    try:
        saveChatId(chatId)
        return {'mensagem': 'chat_id registrado com sucesso'}, 201 
    except Exception as error:
        return {'mensagem': f'Erro ao tentar salvar chat_id. {error}'}, 500
    
@app.route('/api/notifications/send', methods=['POST'])
def fireTelegramNotification():
    chat_id = request.json['chat_id']
    message = request.json['message']

    statusCode = sendMessage(chat_id, message)
    
    if statusCode == 200:
        return {'mensagem': 'Mensagem enviada com sucesso'}, statusCode
    
    return {'mensagem': 'Erro ao tentar enviar mensagem no Telegram'}, statusCode
        

@app.route('/api/notifications/telegram/ids', methods=['GET'])
def getTelegramChats():
    result = getChatsIds()
    
    if result is int:
        result = getChatIdsFromDatabase()
    
    if not result or result is int:
        return {'mensagem': 'Erro ao tentar recuperar os chats do Telegram'}, 500
    
    return jsonify(result)

# Authentication
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'mensagem': 'Dados de login ausentes'}), 400

    username = data['username']
    password = data['password']
    
    result = authenticateUser(username, password)
    
    return jsonify(result)

@app.route('/api/admin', methods=['GET'])
def checkAdmin():
    result = searchForAdmin()
    print(result)
    
    return jsonify(result)

# Device Logs
@app.route('/api/logs', methods=['POST'])
def storeLogs():
    data = request.get_json()

    if not data or 'time' not in data or 'device_id' not in data or 'identified_user' not in data or 'accuracy' not in data or 'type' not in data:
        return jsonify({'mensagem': 'Dados para registro de log insuficientes'}), 400

    device_id = data['device_id']
    time = data['time']
    identified_user = data['identified_user']
    accuracy = data['accuracy']
    type = data['type']
    
    result = registerLog(device_id, time, identified_user, accuracy, type)
    
    return jsonify(result)

@app.route('/api/devices', methods=['POST'])
def storeDevice():
    data = request.get_json()

    if not data or 'device_id' not in data:
        return jsonify({'mensagem': 'Dados para registro de dispositivo'}), 400

    device_id = data['device_id']
    
    result = registerDevice(device_id)
    
    return jsonify(result)

# TODO: FINISH
@app.route('/api/user', methods=['POST'])
def registerUser():
    login = request.json.get("login")
    password = request.json.get("password")
    user_type = request.json.get("user_type")
    guid = str(uuid.uuid4())
             
    try:
        saveUser(guid, login, password, user_type)
        return {'mensagem': 'Usuário registrado com sucesso'}, 201 
    except Exception as error:
        return {'mensagem': f'Erro ao tentar salvar usuário. {error}'}, 500
    
if __name__ == '__main__':
    app.run()
    
