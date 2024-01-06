import os
import face_recognition
import json
from database.db_handler import saveEncoding

def storeAllFaces():        
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
            saveEncoding(known_person_folder_name, face_encoding)

def storeFace(full_path, name, guid):
    loaded_face = face_recognition.load_image_file(full_path)            
    face_locations = face_recognition.face_locations(loaded_face)
    if(len(face_locations) == 0):
        return
    face_encoding = face_recognition.face_encodings(loaded_face)[0]
    json_encoding = json.dumps(face_encoding.tolist())
    saveEncoding(name, json_encoding, guid)
    
    
    