import cv2
import os

# --- Create the Dataset Folder ---
dataset_folder = 'dataset'
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)
# ---------------------------------

# --- Get User Name and Roll Number ---
person_name = input("Enter the person's name: ")
roll_no = input(f"Enter {person_name}'s roll number: ")

# We will save the folder as "Name_RollNo"
person_folder_name = f"{person_name}_{roll_no}"
person_folder = os.path.join(dataset_folder, person_folder_name)

if not os.path.exists(person_folder):
    os.makedirs(person_folder)
    print(f"Created folder for: {person_folder_name}")
else:
    print(f"Folder for {person_folder_name} already exists. Adding images.")
# ---------------------

# --- Initialize Webcam and Face Detector ---
cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print("\n[INFO] Initializing face capture. Look at the camera and wait...")
count = 0

while True:
    ret, img = cam.read()
    if not ret:
        print("[ERROR] Failed to grab frame")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1
        
        # Save the captured face image to the person's folder
        img_path = os.path.join(person_folder, f"{person_name}_{count}.jpg")
        cv2.imwrite(img_path, gray[y:y+h, x:x+w])
        
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' to exit
    if k == 27:
        break
    elif count >= 30: # Take 30 face samples
         break

print(f"\n[INFO] {count} images saved for {person_folder_name}.")
print("[INFO] Exiting Program.")
cam.release()
cv2.destroyAllWindows()