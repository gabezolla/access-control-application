import cv2
import os
import numpy as np
import face_recognition
from deepface import DeepFace
import time
import json
import requests
    
def recognizeFear(frame, face_locations):
    # Convert from BGR to RGB to use it on face_recognition
    rgb_frame = frame[:, :, ::-1]
    
    fear_time = 0
    start_time = time.time()
    
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = rgb_frame[top:bottom, left:right]
        
        emotion_prediction = DeepFace.analyze(face_image, actions=['emotion'])
        dominant_emotion = emotion_prediction[0]['dominant_emotion']
        
        if dominant_emotion == 'fear':
            fear_time = time.time() - start_time
        else:
            fear_time = 0
            start_time = time.time()

        # Check if fear has been detected for more than 2 seconds
        if fear_time >= 2:
            print("Medo detectado por mais de 2 segundos!")
            
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
    url = "http://127.0.0.1:5000" # Migrar para appSettings
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

    response = requests.get('http://127.0.0.1:5000/api/encodings') # Migrar para appSettings
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

# sendNotification("Hello")
webcam = cv2.VideoCapture(0)
showVideo()
