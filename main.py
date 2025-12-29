import cv2
import os
from utils import train_model, mark_attendance, get_face_detector

def main():
    data_path = 'known_faces'
    
    # Train the basic model on startup
    recognizer, label_map = train_model(data_path)
    detector = get_face_detector()
    
    if not label_map:
        print("Warning: No training data found. Recognition will not work until images are added to 'known_faces'.")
        print("Please add 'Name.jpg' images to the known_faces folder and restart.")

    print("Starting camera...")
    
    # Try index 0 and 1
    cap = None
    for index in [0, 1]:
        print(f"Trying camera index {index}...")
        temp_cap = cv2.VideoCapture(index)
        if temp_cap.isOpened():
            cap = temp_cap
            print(f"Connected to camera index {index}.")
            break
            
    if cap is None or not cap.isOpened():
        print("Error: Could not open any camera (tried index 0 and 1).")
        print("Please check if your webcam is connected and not used by another app.")
        return

    print("Camera started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Predict
            id_ = -1
            confidence = 100
            
            if label_map:
                try:
                    id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                    
                    # LBPH Confidence: Lower is better (0 is perfect match)
                    # Heuristic: < 100 might be a match, < 50 is checking goodness
                    if confidence < 100:
                        name_identifier = label_map.get(id_, "Unknown")
                        conf_str = f"  {round(100 - confidence)}%"
                    else:
                        name_identifier = "Unknown"
                        conf_str = f"  {round(100 - confidence)}%"
                        
                    if name_identifier != "Unknown":
                        mark_attendance(name_identifier)
                        
                        # Clean up display (optional, remove ID for video if too long, but user wants ID)
                        # name_identifier is "ID:Name" or "Name"
                        display_text = name_identifier.replace(":", " ")
                    else:
                        display_text = "Unknown"
                        
                except Exception as e:
                    display_text = "Unknown"
                    conf_str = ""
            else:
                display_text = "Unknown"
                conf_str = ""

            cv2.putText(frame, str(display_text), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            # cv2.putText(frame, str(conf_str), (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        cv2.imshow('Face Recognition (OpenCV)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
