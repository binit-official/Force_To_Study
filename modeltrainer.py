import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'E:/Projects/Force_To_Study/samplles'

# Initialize the LBPH face recognizer and Haar Cascade for face detection
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def Images_and_labels(path):
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    facesamples = []
    ids = []

    for imagepath in imagepaths:
        gray_img = Image.open(imagepath).convert('L')  # Convert to grayscale
        img_arr = np.array(gray_img, 'uint8')

        # Extract the ID from the image filename
        id = int(os.path.split(imagepath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x, y, w, h) in faces:
            facesamples.append(img_arr[y:y+h, x:x+w])
            ids.append(id)

    return facesamples, ids

print("Training faces... It will take a few seconds. Please wait...")

faces, ids = Images_and_labels(path)
recognizer.train(faces, np.array(ids))

# Save the trained model
recognizer.write('trainer/trainer.yml')

print("Model trained, now we can recognize your face...")
