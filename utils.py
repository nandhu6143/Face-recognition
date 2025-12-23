import cv2
import os
import numpy as np
import csv
from datetime import datetime

def get_face_detector():
    """Returns the Haar Cascade face detector."""
    # Use the XML file from the cv2 data path
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    return cv2.CascadeClassifier(cascade_path)

def train_model(data_path):
    """
    Trains the LBPH Face Recognizer using images in data_path.
    Folder structure: named images (e.g. 'PersonName.jpg') directly in data_path.
    Returns: trained recognizer, label_map (id -> name)
    """
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = get_face_detector()
    
    face_samples = []
    ids = []
    label_map = {} # id -> name
    current_id = 0
    name_to_id = {} # name -> id

    print(f"Training model from {data_path}...")
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        return recognizer, label_map

    files = [f for f in os.listdir(data_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print("No images found to train.")
        return recognizer, label_map

    for filename in files:
        image_path = os.path.join(data_path, filename)
        name = os.path.splitext(filename)[0]
        
        if name not in name_to_id:
            name_to_id[name] = current_id
            label_map[current_id] = name
            current_id += 1
            
        label_id = name_to_id[name]
        
        # Read image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
            
        faces = detector.detectMultiScale(img)
        
        for (x, y, w, h) in faces:
            face_samples.append(img[y:y+h, x:x+w])
            ids.append(label_id)
            
    if face_samples:
        recognizer.train(face_samples, np.array(ids))
        print(f"Model trained with {len(face_samples)} faces for {len(label_map)} people.")
    else:
        print("No faces found in the training images.")

    return recognizer, label_map

def mark_attendance(name):
    """Logs the name and current timestamp to attendance.csv"""
    filename = 'attendance.csv'
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    time_string = now.strftime('%H:%M:%S')
    
    # Check/Create file
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Date', 'Time'])
            
    # Avoid duplicate
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if not line: continue
            if line[0] == name and line[1] == date_string:
                return 

    # Log
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, date_string, time_string])
        print(f"Attendance marked for {name}")
