import os
import sys
import csv
from datetime import datetime

def main():
    while True:
        print("\n=== Face Recognition System ===")
        print("1. Add a New User (Capture Photo)")
        print("2. Delete a User")
        print("3. Start Recognition System")
        print("4. View Today's Attendance")
        print("5. Open Attendance File")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
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
            date_today = datetime.now().strftime('%Y-%m-%d')
            print(f"\n--- Attendance for {date_today} ---")
            found = False
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    # Handle header
                    header = next(reader, None) 
                    if header:
                        # Print header nicely
                        print(f"{header[0]:<15} {header[1]:<20} {header[2]:<15} {header[3]:<15}" if len(header)>=4 else "INVALID HEADER")
                        print("-" * 65)
                        
                    for line in reader:
                        if not line: continue
                        # Check date match (index 2 for new format, 1 for old)
                        if len(line) == 4:
                            if line[2] == date_today:
                                print(f"{line[0]:<15} {line[1]:<20} {line[2]:<15} {line[3]:<15}")
                                found = True
                        elif len(line) == 3:
                             if line[1] == date_today:
                                 print(f"{'N/A':<15} {line[0]:<20} {line[1]:<15} {line[2]:<15}")
                                 found = True
            else:
                print("Attendance file not found.")
            
            if not found:
                print("No records found for today.")
            print("-" * 65)
            input("\nPress Enter to continue...")

        elif choice == '5':
            file_path = 'attendance.xlsx'
            if os.path.exists(file_path):
                print(f"\nOpening {file_path}...")
                os.startfile(file_path) # Windows only
            else:
                file_path_csv = 'attendance.csv'
                if os.path.exists(file_path_csv):
                     print(f"\nExcel not found, opening {file_path_csv}...")
                     os.startfile(file_path_csv)
                else:
                    print("\nAttendance file not found yet.")
                
        elif choice == '6':
            print("Exiting.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
