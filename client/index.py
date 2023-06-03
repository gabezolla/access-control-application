import streamlit as st
import requests

def cadastrar_foto(nome, imagem):
    url = 'http://localhost:5000/api/photos'
    
    data = {'nome': nome}
    
    files = {'imagem': imagem}
    response = requests.post(url, data=data, files=files)
    
    st.write(response.json())

def main():
    st.title('Cadastro de Fotos')
    
    nome = st.text_input("Nome:")
    
    imagem = st.file_uploader("Imagem:", type=['jpg', 'jpeg', 'png'])
    
    if st.button('Cadastrar'):
        if nome and imagem:
            cadastrar_foto(nome, imagem)
        else:
            st.warning('Por favor, preencha o nome e selecione uma imagem.')

if __name__ == '__main__':
    main()
