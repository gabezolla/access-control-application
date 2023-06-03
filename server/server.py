from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/api/photos', methods=['POST'])
def cadastrar_foto():
    name = request.form.get('nome')
    image = request.files.get('imagem')

    if image:
        caminho = f'user-data/{name}/'
        
        if not os.path.exists(caminho):
            os.makedirs(caminho)

        image.save(caminho + image.filename)

        return {'mensagem': 'Foto cadastrada com sucesso'}
    else:
        return {'mensagem': 'Nenhuma imagem foi enviada'}, 400

if __name__ == '__main__':
    app.run()
