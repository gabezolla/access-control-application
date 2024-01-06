import streamlit as st
import requests
import json

def get_config():
    with open('./config/config.json', 'r') as file:
        config = json.load(file)
    return config

# TODO: mover para um handler?
def registerPhoto(name, image, user_type, login="", password=""):
    url = f"{get_config().get('server_url')}/api/photos"

    data = {
        'name': name,
        'user_type': user_type
    }
    
    files = {'image': image}

    response = requests.post(url, data=data, files=files)
    print("User registered")

def registerNotification(notification_type, contact):
    st.write(f"Notificação do tipo '{notification_type}' cadastrada para o contato '{contact}'.")

def main():
    st.title('Sistema de Cadastro')
    
    if hasNoAdmin():
        tabs = st.sidebar.radio("Selecione a opção:", {"Registro": "Registro"})
        build_register_tab()        
    
    elif not checkAuthenticated():
        tabs = st.sidebar.radio("Selecione a opção:", {"Login": "Login"})
        build_login_tab()
        
    else:
        user_type = getAuthenticationType()
        
        if user_type == 'admin':
            tabs = st.sidebar.radio("Selecione a opção:", ("Cadastro de Fotos", "Cadastro de Notificações"))
            if tabs == "Cadastro de Fotos":
                build_upload_photo_tab()

            elif tabs == "Cadastro de Notificações":
                build_notification_tab()

# Create folders for each page        
def build_login_tab():
    st.header("Página de Login")
    username = st.text_input("Nome de usuário:")
    password = st.text_input("Senha:", type="password")

    if st.button('Entrar'):
        if authenticateUser(username, password):
            st.success("Login bem-sucedido!")
            st.experimental_rerun()
        else:
            st.error("Nome de usuário ou senha incorretos. Tente novamente.")
         
# TODO: DEVELOP THIS TAB   
def build_register_tab():
    st.header("Página de Registro")
    username = st.text_input("Nome de usuário:")
    password = st.text_input("Senha:", type="password")
    user_type = st.selectbox("Tipo de Usuário:", ["Common", "Admin", "Temporary"])    

def createUser(username, password, user_type):
    url = get_config().get('server_url')
    registerRoute = "/api/user"
    data = {
        'username': username,
        'password': password,
        'user_type': user_type
    }
    
    response = requests.post(f"{url}/{registerRoute}", json=data)
    

def checkAuthenticated():
    return getattr(st.session_state, 'is_authenticated', False)

def getAuthenticationType():
    return getattr(st.session_state, 'user_type', None)

def authenticateUser(username, password):
    url = get_config().get('server_url')
    loginRoute = "/api/login"
    
    data = {
        'username': username,
        'password': password
    }
    
    response = requests.post(f"{url}/{loginRoute}", json=data)
    user_data = response.json()
    if user_data:
        st.session_state.is_authenticated = True
        st.session_state.user_type = user_data['type']
        return True
        
    return False

def hasNoAdmin():
    url = get_config().get('server_url')
    firstAccessRoute = "/api/admin"
    
    response = requests.get(f"{url}/{firstAccessRoute}")
    user_data = response.json()
    if user_data:
        return False        
    return True

def build_upload_photo_tab(): 
    st.header("Cadastro de Fotos")
    
    first_name = st.text_input("Nome:")
    last_name = st.text_input("Sobrenome:")
    name = f"{first_name.lower()}-{last_name.lower()}"
    
    image = st.file_uploader("Imagem:", type=['jpg', 'jpeg', 'png'])
    
    user_type = st.selectbox("Tipo de Usuário:", ["Common", "Admin", "Temporary"])

    if user_type == "Admin":
        login = st.text_input("Login:")
        password = st.text_input("Senha:", type="password")
    else:
        login = None
        password = None

    if st.button('Cadastrar'):
        if first_name and last_name and image and user_type:
            registerPhoto(name, image, user_type, login, password)
        else:
            st.warning('Por favor, preencha o nome, selecione uma imagem e escolha um tipo de usuário.')
            
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
        # call API instead of getNotifications()
        notifications = []

        for notification in notifications:
            st.write(f"ID: {notification['id']}")
            st.write(f"Tipo: {notification['type']}")
            st.write(f"Contato: {notification['contact']}")
            st.write("---")

if __name__ == '__main__':
    main()
