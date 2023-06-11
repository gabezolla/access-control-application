from flask import Flask, request
from database.db_handler import saveNotification
import os

app = Flask(__name__)

@app.route('/api/photos', methods=['POST'])
def registerPhoto():
    name = request.form.get('name')
    image = request.files.get('image')

    if image:
        path = f'user-data/{name}/'
        
        if not os.path.exists(path):
            os.makedirs(path)

        image.save(path + image.filename)

        return {'mensagem': 'Foto cadastrada com sucesso'}
    else:
        return {'mensagem': 'Nenhuma imagem foi enviada'}, 400

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