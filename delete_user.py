import os

def delete_user():
    data_path = 'known_faces'
    
    if not os.path.exists(data_path):
        print(f"Directory '{data_path}' does not exist.")
        return

    # List all image files
    files = [f for f in os.listdir(data_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print("No users found to delete.")
        return

    print("\n--- Select User to Delete ---")
    for i, filename in enumerate(files, 1):
        name = os.path.splitext(filename)[0]
        print(f"{i}. {name}")

    print("c. Cancel")

    choice = input("\nEnter choice: ").strip()

    if choice.lower() == 'c':
        print("Cancelled.")
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            file_to_delete = files[idx]
            full_path = os.path.join(data_path, file_to_delete)
            
            confirm = input(f"Are you sure you want to delete {files[idx]}? (y/n): ").strip().lower()
            if confirm == 'y':
                os.remove(full_path)
                print(f"Successfully deleted {file_to_delete}")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    delete_user()
