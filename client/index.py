import streamlit as st
import requests
import json

typeAuthentication = None

def get_config():
    with open('./config/config.json', 'r') as file:
        config = json.load(file)
    return config

def registerPhoto(name, image):
    url = get_config().get('server_url')  # TODO: Mover para um arquivo de configuração

    data = {'name': name}
    files = {'image': image}

    response = requests.post(url, data=data, files=files)

    st.write(response.json())

def registerNotification(notification_type, contact):
    # saveNotification(notification_type, contact) TODO: check ModuleNotFoundError: No module named 'database' when running streamlit run
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
            
def build_register_tab():
    st.header("Página de Registro")

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
    fistAccessRoute = "/api/admin"
    
    response = requests.get(f"{url}/{fistAccessRoute}")
    user_data = response.json()
    if user_data:
        return True        
    return False

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
        # call API instead of getNotifications()
        notifications = []

        for notification in notifications:
            st.write(f"ID: {notification['id']}")
            st.write(f"Tipo: {notification['type']}")
            st.write(f"Contato: {notification['contact']}")
            st.write("---")

if __name__ == '__main__':
    main()
