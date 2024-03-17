import threading
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
        sendLogEvent(name, fear_precision, 'fear')
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
            
def recognizePerson(frame_log_transformed):
    detected_faces = face_recognition.face_locations(frame_log_transformed)
    known_encodings = []
    
    if len(detected_faces) == 0:
        return
    
    print("Face detectada. Checando base de dados...")

    response = requests.get(f'{url}/api/encodings')
    data = response.json()
    
    string_encodings = data['encodings']
    for string_encoding in string_encodings:   
        encoding_data = eval(string_encoding)     
        known_encodings.append(encoding_data)
    
    known_names = np.array(data['names'])
                   
    faces_encodings = face_recognition.face_encodings(frame_log_transformed, detected_faces)
    
    for face_encoding, detected_face in zip(faces_encodings, detected_faces):
        is_known_person = face_recognition.compare_faces(known_encodings, face_encoding, 0.6)
        
        if True in is_known_person:
            index_found = is_known_person.index(True)
            person_encoding = known_encodings[index_found]
            accuracy = (1 - face_recognition.face_distance([person_encoding], face_encoding)[0])*100
            person_name = known_names[index_found]
            recognizeFear(frame_log_transformed, detected_face, person_name)  # Passa o frame transformado
            print(f"{person_name} identificado. Acesso liberado.")
            sendLogEvent(person_name, accuracy, 'identification')            
    return

def log_transform(image):
    blue_channel, green_channel, red_channel = cv2.split(image)

    log_blue_channel = np.log1p(blue_channel)
    log_green_channel = np.log1p(green_channel)
    log_red_channel = np.log1p(red_channel)

    log_blue_channel = (log_blue_channel - np.min(log_blue_channel)) / (np.max(log_blue_channel) - np.min(log_blue_channel)) * 255
    log_green_channel = (log_green_channel - np.min(log_green_channel)) / (np.max(log_green_channel) - np.min(log_green_channel)) * 255
    log_red_channel = (log_red_channel - np.min(log_red_channel)) / (np.max(log_red_channel) - np.min(log_red_channel)) * 255

    log_blue_channel = log_blue_channel.astype(np.uint8)
    log_green_channel = log_green_channel.astype(np.uint8)
    log_red_channel = log_red_channel.astype(np.uint8)

    log_image_bgr = cv2.merge([log_blue_channel, log_green_channel, log_red_channel])

    return log_image_bgr

def showVideo():
    recognize_thread = threading.Thread(target=recognize_person_thread)
    recognize_thread.start()
    
    while True:
        ret, frame = webcam.read()
        frame_equalized = log_transform(frame)
        if ret:
            cv2.imshow("Webcam", frame)
    
        key = cv2.waitKey(1)
        if key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break
        
def recognize_person_thread():
    while True:
        ret, frame = webcam.read()
        frame_equalized = log_transform(frame)
        if ret:
            recognizePerson(frame_equalized)
            time.sleep(3)

def resolveDeviceId():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
    
    device_id = str(uuid.uuid5(uuid.NAMESPACE_X500, mac_address))
    
    data = {
        'device_id': device_id        
    }
        
    requests.post(f"{url}/api/devices", json=data)
    
    return device_id

def sendLogEvent(identified_user, accuracy, type):
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    data = {
        'time': time,
        'device_id': device_id,
        'identified_user': identified_user,
        'accuracy': accuracy,
        'type': type     
    }  
    
    print(data)

    requests.post(f"{url}/api/logs", json=data)

    return 
   

webcam = cv2.VideoCapture(0)
url = get_config().get('server_url')
device_id = resolveDeviceId()
showVideo() 

