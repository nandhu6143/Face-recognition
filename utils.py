import cv2
import os
import numpy as np
import csv
import pandas as pd
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
        basename = os.path.splitext(filename)[0]
        
        # Try to parse ID_Name
        # logic: if underscore exists, split once. If not, use whole as name (ID="").
        parts = basename.split('_', 1)
        if len(parts) == 2:
            student_id = parts[0]
            student_name = parts[1]
            display_name = f"{student_id}:{student_name}"
        else:
            display_name = basename # just name

        if display_name not in name_to_id:
            name_to_id[display_name] = current_id
            label_map[current_id] = display_name
            current_id += 1
            
        label_id = name_to_id[display_name]
        
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

def mark_attendance(name_identifier):
    """
    Logs the attendance to CSV and Excel.
    name_identifier expected format: "ID:Name" or just "Name"
    """
    if ":" in name_identifier:
        student_id, student_name = name_identifier.split(":", 1)
    else:
        student_id = "N/A"
        student_name = name_identifier

    filename_csv = 'attendance.csv'
    filename_xlsx = 'attendance.xlsx'
    
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    time_string = now.strftime('%H:%M:%S')
    
    # --- CSV Handling ---
    # Check/Create CSV
    file_exists = os.path.isfile(filename_csv)
    
    # Check for duplicate in CSV to avoid double logging in session
    # We'll read it first
    already_logged = False
    if file_exists:
        with open(filename_csv, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                if not line: continue
                # CSV Structure: ID, Name, Date, Time (or Name, Date, Time for old)
                # If old format, might crash if we assume index. Let's be robust.
                if len(line) >= 3:
                     # Check date and Name/ID
                     # New format: ID, Name, Date, Time -> indices 0, 1, 2, 3
                     if len(line) == 4:
                         if line[0] == student_id and line[2] == date_string:
                             already_logged = True
                             break
                     # Fallback for mixed/old files
                     elif line[0] == student_name and line[1] == date_string:
                          already_logged = True
                          break

    if not already_logged:
        # Write to CSV
        with open(filename_csv, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Student ID', 'Name', 'Date', 'Time'])
            
            writer.writerow([student_id, student_name, date_string, time_string])
            
        print(f"Attendance marked for {student_name} (CSV)")

        # --- Excel Handling ---
        # We use pandas to append. Reading entire existing excel might be slow for huge files,
        # but for daily attendance it's fine.
        
        new_entry = {
            'Student ID': student_id, 
            'Name': student_name, 
            'Date': date_string, 
            'Time': time_string
        }
        df_new = pd.DataFrame([new_entry])

        if os.path.exists(filename_xlsx):
            try:
                # Read existing to check duplicate (optional, but good)
                # To append without overwriting:
                # We can load, append, save.
                with pd.ExcelWriter(filename_xlsx, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                     # This is tricky because we need to find last row.
                     # Simpler: Read, Concat, Write.
                     pass 
                
                # Simpler Read-Append strategy
                df_existing = pd.read_excel(filename_xlsx)
                
                # Check duplication in DF
                # Safe check
                duplicate = df_existing[
                    (df_existing['Student ID'].astype(str) == str(student_id)) & 
                    (df_existing['Date'] == date_string)
                ]
                
                if duplicate.empty:
                    # Append
                    df_final = pd.concat([df_existing, df_new], ignore_index=True)
                    df_final.to_excel(filename_xlsx, index=False)
                    print(f"Attendance marked for {student_name} (Excel)")
                    
            except Exception as e:
                print(f"Error updating Excel: {e}")
        else:
            # Create new
            df_new.to_excel(filename_xlsx, index=False)
            print(f"Created new Excel attendance file for {student_name}")
            
    else:
        # already logged
        pass
