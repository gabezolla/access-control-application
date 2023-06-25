import streamlit as st
import requests
# from database.db_handler import saveNotification, getNotifications TODO: check ModuleNotFoundError: No module named 'database' when running streamlit run

def registerPhoto(name, image):
    url = 'http://localhost:5000/api/photos'  # TODO: Mover para um arquivo de configuração

    data = {'name': name}
    files = {'image': image}

    response = requests.post(url, data=data, files=files)

    st.write(response.json())

def registerNotification(notification_type, contact):
    # saveNotification(notification_type, contact) TODO: check ModuleNotFoundError: No module named 'database' when running streamlit run
    st.write(f"Notificação do tipo '{notification_type}' cadastrada para o contato '{contact}'.")

def main():
    st.title('Sistema de Cadastro')

    tabs = st.sidebar.radio("Selecione a opção:", ("Cadastro de Fotos", "Cadastro de Notificações"))

    if tabs == "Cadastro de Fotos":
        build_upload_photo_tab()

    elif tabs == "Cadastro de Notificações":
        build_notification_tab()

def build_upload_photo_tab(): 
    st.header("Cadastro de Fotos")
    first_name = st.text_input("Nome:")
    last_name = st.text_input("Sobrenome:")
    name = f"{first_name.lower()}-{last_name.lower()}"
    image = st.file_uploader("Imagem:", type=['jpg', 'jpeg', 'png'])

    if st.button('Cadastrar'):
        if first_name and last_name and image:
            registerPhoto(name, image)
        else:
            st.warning('Por favor, preencha o nome e selecione uma imagem.')
            
def build_notification_tab():
    st.header("Cadastro de Notificações")
    notification_type = st.selectbox("Tipo de Notificação:", ["Telegram"])
    contact = st.text_input("Contato:")

    if st.button('Cadastrar'):
        if notification_type and contact:
            registerNotification(notification_type, contact)
        else:
            st.warning('Por favor, selecione um tipo de notificação e preencha o contato.')

        st.header("Lista de Notificações")
        # notifications = getNotifications() TODO: check ModuleNotFoundError: No module named 'database' when running streamlit run
        notifications = []

        for notification in notifications:
            st.write(f"ID: {notification['id']}")
            st.write(f"Tipo: {notification['type']}")
            st.write(f"Contato: {notification['contact']}")
            st.write("---")

if __name__ == '__main__':
    main()
