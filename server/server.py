from flask import Flask, request, jsonify
from database.db_handler import saveNotification, getEncodingsFromDatabase
from database.encoding_service import storeFace
import os

app = Flask(__name__)

@app.route('/api/encodings', methods=['GET'])
def getEncodings():
    names, encodings = getEncodingsFromDatabase()
    encodings_dict = {"names": names, "encodings": encodings}
    return jsonify(encodings_dict)    

@app.route('/api/photos', methods=['POST'])
def registerPhoto():
    name = request.form.get('name')
    image = request.files.get('image')

    if image:
        path = f'user-data/{name}/'
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        full_path = path + f"{len(os.listdir(path)) + 1}.png"
        image.save(full_path)
        
        storeFace(full_path, name)

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

if __name__ == '__main__':
    app.run()