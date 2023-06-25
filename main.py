import cv2
import os
import numpy as np
import face_recognition
from deepface import DeepFace
import time
import json
from database.db_handler import getEncodings, saveEncoding
    
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
            
def recognizePerson(frame):
    # Convert from BGR to RGB to use it on face_recognition
    rgb_frame = frame[:, :, ::-1]
    detected_faces = face_recognition.face_locations(rgb_frame)
    known_encodings = []
    known_names = []
    
    if len(detected_faces) == 0:
        return
    
    name_data, encoding_data = getEncodings()
            
    for data in encoding_data:
        face_encoding = json.loads(data)
        known_encodings.append(np.array(face_encoding)) 
                       
    faces_encodings = face_recognition.face_encodings(rgb_frame, detected_faces)
    
    for face_encoding, detected_face in zip(faces_encodings, detected_faces):
        is_known_person = face_recognition.compare_faces(known_encodings, face_encoding)
        
        if True in is_known_person:
            index_found = is_known_person.index(True)
            person_name = name_data[index_found]
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

# TODO: remove from local storage and store on database 
# known_people_encodings, known_names = getAndUpdateStoredKnownFaces()
webcam = cv2.VideoCapture(0)
showVideo()
