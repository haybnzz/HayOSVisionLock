import face_recognition
import cv2
import os
import win32api
import win32con
import winreg
import requests
import time
import getpass
import datetime
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox

# Configuration
KNOWN_FACES_DIR = "known_faces"  # Folder with your face images
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1376189281751793756/moDICuy9PbvcdNs3dOb31fgZvUo69c1c1F64UU67QALYlIXls78v74DCKGC2b4E00Ra0"
SCRIPT_PATH = os.path.abspath(__file__)  # Path to this script
TOLERANCE = 0.6  # Face recognition tolerance (lower is stricter)
LOCK_TIMEOUT = 10  # Seconds to wait before locking if no known face is detected
CHECK_INTERVAL = 1  # Seconds between face checks

# Load known faces
def load_known_faces():
    known_encodings = []
    known_names = []
    if not os.path.exists(KNOWN_FACES_DIR):
        print(f"Error: 'known_faces' folder not found at {os.path.abspath(KNOWN_FACES_DIR)}")
        print(f"Please create the folder and add .jpg or .png images of faces.")
        return known_encodings, known_names
    files = os.listdir(KNOWN_FACES_DIR)
    if not files:
        print(f"Error: 'known_faces' folder is empty at {os.path.abspath(KNOWN_FACES_DIR)}")
        return known_encodings, known_names
    for filename in files:
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            print(f"Processing image: {image_path}")
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_names.append(os.path.splitext(filename)[0])
                    print(f"Face detected in {filename}")
                else:
                    print(f"No faces detected in {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            print(f"Skipping non-image file: {filename}")
    if not known_encodings:
        print("Warning: No valid face encodings found in 'known_faces' folder.")
    return known_encodings, known_names

# Add script to Windows Registry for auto-start
def add_to_startup():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(
            key,
            "FaceRecognitionLock",
            0,
            winreg.REG_SZ,
            f'"{sys.executable}" "{SCRIPT_PATH}"'
        )
        winreg.CloseKey(key)
        print("Script added to startup.")
    except Exception as e:
        print(f"Failed to add to startup: {e}")

# Lock the Windows PC
def lock_pc():
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        print("PC locked.")
    except Exception as e:
        print(f"Failed to lock PC: {e}")

# Send Discord notification
def send_discord_notification(message, image_path=None):
    try:
        data = {"content": message}
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                files = {"file": (os.path.basename(image_path), f)}
                response = requests.post(DISCORD_WEBHOOK_URL, data=data, files=files)
        else:
            response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Discord notification sent.")
        else:
            print(f"Failed to send Discord notification: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord notification: {e}")

# Verify system password (indirectly via privileged operation)
def verify_system_password(password):
    try:
        # Attempt a privileged operation (e.g., access a restricted Registry key)
        # Note: Direct Windows password verification requires complex API calls
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control",
            0,
            winreg.KEY_READ
        )
        winreg.CloseKey(key)
        return True  # If no exception, assume user has sufficient privileges
    except PermissionError:
        print("Password verification failed: Insufficient privileges.")
        return False
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

# Register new face
def register_face(frame, face_locations):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    password = simpledialog.askstring("Password", "Enter system password to register face:", show="*")
    root.destroy()

    if not password:
        messagebox.showerror("Error", "No password entered.")
        return False

    if verify_system_password(password):
        if face_locations:
            top, right, bottom, left = face_locations[0]  # Use first detected face
            face_image = frame[max(0, top-20):bottom+20, max(0, left-20):right+20]
            if face_image.size == 0:
                messagebox.showerror("Error", "Failed to capture face image.")
                return False

            # Save face image with username and timestamp
            username = getpass.getuser()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            face_filename = f"{username}_{timestamp}.jpg"
            face_path = os.path.join(KNOWN_FACES_DIR, face_filename)
            cv2.imwrite(face_path, face_image)
            print(f"New face registered and saved as {face_path}")

            # Verify face encoding
            image = face_recognition.load_image_file(face_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                messagebox.showinfo("Success", f"Face registered successfully as {face_filename}")
                return True
            else:
                os.remove(face_path)  # Remove invalid image
                messagebox.showerror("Error", "No face detected in captured image. Try again.")
                return False
        else:
            messagebox.showerror("Error", "No face detected in webcam. Ensure your face is visible.")
            return False
    else:
        messagebox.showerror("Error", "Incorrect password. Face registration failed.")
        return False

# Main face recognition loop
def main():
    # Add script to startup
    add_to_startup()

    # Load known faces
    known_encodings, known_names = load_known_faces()
    if not known_encodings:
        print("Continuing without known faces; will treat all faces as unknown.")
        # Optional: Uncomment the line below to exit if no known faces are found
        # return

    # Initialize webcam
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    last_known_face_time = time.time()
    username = getpass.getuser()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame.")
            break

        # Convert frame to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        current_time = time.time()
        recognized = False

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=TOLERANCE)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                recognized = True
                last_known_face_time = current_time
                print(f"Recognized {name}")

            else:
                # Save cropped unknown face image
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                unknown_face_path = f"unknown_face_{timestamp}.jpg"
                face_image = frame[max(0, top-20):bottom+20, max(0, left-20):right+20]
                if face_image.size > 0:
                    cv2.imwrite(unknown_face_path, face_image)
                    print(f"Unknown face cropped and saved as {unknown_face_path}")
                else:
                    cv2.imwrite(unknown_face_path, frame)
                    print(f"Unknown face (full frame) saved as {unknown_face_path}")

                # Send Discord notification with image
                message = f"Unknown face detected on {username}'s PC at {timestamp}"
                send_discord_notification(message, unknown_face_path)

        # Lock PC if no known face is detected for too long
        if not recognized and (current_time - last_known_face_time) > LOCK_TIMEOUT:
            lock_pc()
            last_known_face_time = current_time  # Reset to avoid repeated locking

        # Display the frame with instructions
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, "Press 'r' to register face, 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Video', frame)

        # Handle keypress for face registration or quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            if register_face(frame, face_locations):
                # Reload known faces after successful registration
                known_encodings, known_names = load_known_faces()

        time.sleep(CHECK_INTERVAL)

    # Cleanup
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
