import os
import sys

def main():
    while True:
        print("\n=== Face Recognition System ===")
        print("1. Add a New User (Capture Photo)")
        print("2. Delete a User")
        print("3. Start Recognition System")
        print("4. Open Attendance File")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            print("\nLaunching Capture Tool...")
            os.system('python capture_face.py')

        elif choice == '2':
            print("\nLaunching Delete Tool...")
            os.system('python delete_user.py')
        
        elif choice == '3':
            print("\nLaunching Recognition System...")
            os.system('python main.py')
            
        elif choice == '4':
            file_path = 'attendance.csv'
            if os.path.exists(file_path):
                print(f"\nOpening {file_path}...")
                os.startfile(file_path) # Windows only
            else:
                print("\nAttendance file not found yet (runs need to be made first).")
                
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
