import requests
import json
import os

def loadConfig():  
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, 'server_config.json')
    
    with open(config_file_path) as config_file:
        config_data = json.load(config_file)
        return config_data['token']

def getChatsIds():
    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url)
        
        if response.status_code == 200:
            json_msg = response.json()
            chat_ids = []

            if 'result' in json_msg:
                for update in json_msg['result']:
                    chat_id = update['message']['chat']['id']
                    chat_ids.append(chat_id)

            return chat_ids
                
        else:
            print(f'Request failed. StatusCode: {response.status_code}')
            return response.status_code
        
    except Exception as e:
        print("Error trying to execute getUpdates:", e)
        return 500
        
def sendMessage(chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("Message successfully sent")
        else:
            print(f"Failed to send message. StatusCode: {response.status_code}")
        
        return response.status_code
            
    except Exception as e:
        print("Exception triggered while trying to execute sendMessage.", e)
        return 500

token = loadConfig()    
