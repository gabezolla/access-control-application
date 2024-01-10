import cv2
import os
import numpy as np
import face_recognition
from deepface import DeepFace
import time
import uuid
import json
import requests
from datetime import datetime

def get_config():
    with open('config/config.json', 'r') as file:
        config = json.load(file)
    return config
    
def recognizeFear(frame, face_location, name):
    # Convert from BGR to RGB to use it on face_recognition
    rgb_frame = frame[:, :, ::-1]
    
    top, right, bottom, left = face_location
    face_image = rgb_frame[top:bottom, left:right]
        
    emotion_prediction = DeepFace.analyze(face_image, actions=['emotion'], enforce_detection = False, silent=True)
    dominant_emotion = emotion_prediction[0]['dominant_emotion']
    fear_precision = emotion_prediction[0]['emotion']['fear']
        
    if dominant_emotion == 'fear' and fear_precision > 85:
        print(emotion_prediction[0]['emotion']['fear'])
        print(f"Fear detected for user {name}!")
        sendLogEvent(name, fear_precision)
        sendNotification(f"Fear detected for user {name}!")
    return

""" def getAndUpdateStoredKnownFaces():
    known_people_encodings = []
    known_names = []
    main_directory = "user-data"  
    known_person_folders = os.listdir(main_directory)
      
    for known_person_folder_name in known_person_folders:
        known_person_folder = os.path.join(main_directory, known_person_folder_name)
        if not os.path.isdir(known_person_folder):
            continue
        
        known_face_files = os.listdir(known_person_folder)
        
        for known_face_file in known_face_files:
            image_path = os.path.join(known_person_folder, known_face_file)
            loaded_face = face_recognition.load_image_file(image_path)
            
            face_locations = face_recognition.face_locations(loaded_face)
            
            if(len(face_locations) == 0):
                continue
                         
            face_encoding = face_recognition.face_encodings(loaded_face)[0]
            known_people_encodings.append(face_encoding)
            known_names.append(known_person_folder_name)
            
    return known_people_encodings, known_names """
    
def sendNotification(message):
    getIdsPath = "api/notifications/telegram/ids"
    sendMessagePath = "api/notifications/send"
    
    ids = requests.get(f"{url}/{getIdsPath}").json()
    
    for id in ids:
        data = {
        'chat_id': id,
        'message': message
        }
        message_result = requests.post(f"{url}/{sendMessagePath}", json=data)
        print(message_result.json())
    return
            
def recognizePerson(frame):
    # Convert from BGR to RGB to use it on face_recognition
    rgb_frame = frame[:, :, ::-1]
    detected_faces = face_recognition.face_locations(rgb_frame)
    known_encodings = []
    
    if len(detected_faces) == 0:
        return

    response = requests.get(f'{url}/api/encodings')
    data = response.json()
    
    string_encodings = data['encodings']
    for string_encoding in string_encodings:   
        encoding_data = eval(string_encoding)     
        known_encodings.append(encoding_data)
    
    known_names = np.array(data['names'])
                       
    faces_encodings = face_recognition.face_encodings(rgb_frame, detected_faces)
    
    for face_encoding, detected_face in zip(faces_encodings, detected_faces):
        is_known_person = face_recognition.compare_faces(known_encodings, face_encoding)
        
        if True in is_known_person:
            index_found = is_known_person.index(True)
            person_name = known_names[index_found]
            recognizeFear(rgb_frame, detected_face, person_name)
            print(f"{person_name} identificado. Acesso liberado.")            
    return

def showVideo():
    ret, frame = webcam.read()
    if ret:
        recognizePerson(frame)
        cv2.imshow("Webcam", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
    else:
        cv2.waitKey(10)
        showVideo() 

def resolveDeviceId():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
    
    device_id = str(uuid.uuid5(uuid.NAMESPACE_X500, mac_address))
    
    data = {
        'device_id': device_id        
    }
        
    requests.post(f"{url}/api/devices", json=data)
    
    return device_id

def sendLogEvent(identified_user, accuracy):
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        'time': time,
        'device_id': device_id,
        'identified_user': identified_user,
        'accuracy': accuracy        
    }  
    
    print(data)  

    requests.post(f"{url}/api/logs", json=data)

    return 
   

webcam = cv2.VideoCapture(0)
url = get_config().get('server_url')
device_id = resolveDeviceId()
showVideo() 
