import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk
import face_recognition
from deepface import DeepFace
import time

def captureImage():
    user_name = name_input.get()
    _, frame = webcam.read()
    
    directory = os.path.join("user-data", user_name)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    archive_name = f"{len(os.listdir(directory)) + 1}.png"
    archive_path = os.path.join(directory, archive_name)
    
    cv2.imwrite(archive_path, frame)
    
    global known_people_encodings, known_names 
    known_people_encodings, known_names = getAndUpdateStoredKnownFaces()
    
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
            tempo_medo = time.time() - start_time
        else:
            tempo_medo = 0
            start_time = time.time()

        # Check if fear has been detected for more than 2 seconds
        if tempo_medo >= 2:
            print("Medo detectado por mais de 2 segundos!")
            
    return
        
def getAndUpdateStoredKnownFaces():
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
            face_encoding = face_recognition.face_encodings(loaded_face)[0]
            known_people_encodings.append(face_encoding)
            known_names.append(known_person_folder_name)
            
    return known_people_encodings, known_names
            
def recognizePerson(frame):
    # Convert from BGR to RGB to use it on face_recognition
    rgb_frame = frame[:, :, ::-1]
    detected_faces = face_recognition.face_locations(rgb_frame)
    
    if len(detected_faces) == 0:
        return
        
    faces_encodings = face_recognition.face_encodings(rgb_frame, detected_faces)
    
    for face_encoding, detected_face in zip(faces_encodings, detected_faces):
        is_known_person = face_recognition.compare_faces(known_people_encodings, face_encoding)
        
        if True in is_known_person:
            index_found = is_known_person.index(True)
            person_name = known_names[index_found]
            print(f"{person_name} identificado. Acesso liberado.")            
    return

def showVideo():
    ret, frame = webcam.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = image.resize((640, 480))
        photo = ImageTk.PhotoImage(image=image)
        image_label.config(image=photo)
        image_label.image = photo
        recognizePerson(frame)
        image_label.after(10, showVideo)
 
known_people_encodings, known_names = getAndUpdateStoredKnownFaces()
webcam = cv2.VideoCapture(0)

interface = tk.Tk()
interface.title("Face Recognition Program")

name_input = tk.Entry(interface)
name_input.pack()

capture_button = tk.Button(interface, text="Capturar Imagem", command=captureImage)
capture_button.pack()
    
image_label = tk.Label(interface)
image_label.pack()
    
showVideo()

interface.mainloop() 