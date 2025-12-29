import cv2
import os

def capture_face():
    # Create directory if not exists
    save_dir = 'known_faces'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print("Starting camera for capture...")
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        # Try index 1 just in case
        cam = cv2.VideoCapture(1)
        if not cam.isOpened():
            print("Error: Could not open camera.")
            return

    print(f"Camera opened. Resolution: {cam.get(3)}x{cam.get(4)}")
    print("Instructions:")
    print("1. Enter the name of the person when prompted in the terminal.")
    print("2. Press 'SPACE' to capture the photo.")
    print("3. Press 'q' to quit without saving.")

    # Ask for ID and Name
    student_id = input("\nEnter Student ID : ").strip()
    if not student_id:
        print("Invalid ID. Exiting.")
        cam.release()
        return

    name = input("Enter Name : ").strip()
    if not name:
        print("Invalid Name. Exiting.")
        cam.release()
        return
        
    # formatted name for file: ID_Name
    # Sanitize just in case
    safe_id = "".join([c for c in student_id if c.isalnum() or c in ('-', '_')])
    safe_name = "".join([c for c in name if c.isalnum() or c in ('-', '_')])
    
    full_identifier = f"{safe_id}_{safe_name}"

    cv2.namedWindow("Capture Face")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("Capture Face", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27 or k % 256 == ord('q'):
            # ESC or q pressed
            print("Escape hit, closing/not saving...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = f"{full_identifier}.jpg"
            save_path = os.path.join(save_dir, img_name)
            cv2.imwrite(save_path, frame)
            print(f"{img_name} written to {save_dir}!")
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_face()
