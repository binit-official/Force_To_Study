import cv2
import time
import numpy as np
import pygame
import face_recognition

# Load the trained face recognition model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('E:/Projects/Force_To_Study/trainer/trainer.yml')

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

# Initialize the pygame mixer
pygame.mixer.init()

# Set the alarm MP3 file
ALARM_MP3 = 'E:/Projects/Force_To_Study/alert.mp3'
BREAK_SOUND_MP3 = 'E:/Projects/Force_To_Study/break.mp3'
FINISH_MP3 = 'E:/Projects/Force_To_Study/finish.mp3'

# Load the warning image
WARNING_IMAGE = cv2.imread('E:/Projects/Force_To_Study/warning.jpg')

# Initialize flags
face_verified = False
alarm_playing = False
delay_time = 20  # 20 seconds for initial face verification
initial_verification_done = False

# Initial face verification step
print("Please ensure your face is visible to verify before starting the session...")
start_time = time.time()  # Initialize start_time for the initial face verification
while not initial_verification_done:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_found = False

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        id, accuracy = recognizer.predict(gray_frame[top:bottom, left:right])

        if accuracy < 100:  # Face is recognized
            face_found = True
            if not face_verified:
                face_verified = True
                print("Face Verified!")
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Face Verified", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            id = "unknown"
            accuracy = " {0}%".format(round(100 - accuracy))
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    if face_found and face_verified:
        print("Initial face verification successful. Please enter your study details.")
        initial_verification_done = True
        break

    if time.time() - start_time >= delay_time:
        print("Different face detected or face not verified. Program will terminate.")
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()
        exit()

    cv2.imshow('Initial Face Verification', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the initial face verification window
cv2.destroyAllWindows()

# Prompt for study time, break time, and break interval after verification
print("Welcome to the Study Buddy!")
study_time = input("How much time do you want to sit for study? (e.g., 1h, 30m, 2h30m): ")
break_time = input("How much break time do you want? (e.g., 10m, 30m): ")
break_interval = input("How often do you want to take a break? (e.g., 30m): ")

# Convert study time, break time, and break interval to seconds
def convert_to_seconds(time_str):
    seconds = 0
    if "h" in time_str:
        hours = int(time_str.split("h")[0])
        seconds += hours * 3600
    if "m" in time_str:
        minutes = int(time_str.split("m")[0].split("h")[-1])
        seconds += minutes * 60
    return seconds

study_time_seconds = convert_to_seconds(study_time)
break_time_seconds = convert_to_seconds(break_time)
break_interval_seconds = convert_to_seconds(break_interval)

print(f"Study time: {study_time_seconds} seconds")
print(f"Break time: {break_time_seconds} seconds")
print(f"Break interval: {break_interval_seconds} seconds")

# Start the timer here after user input
start_time = time.time()
break_time_flag = False
break_start_time = start_time

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_found = False

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        id, accuracy = recognizer.predict(gray_frame[top:bottom, left:right])

        if accuracy < 100:
            face_found = True
            if not face_verified:
                face_verified = True
                print("Face Verified!")
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Face Verified", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            id = "unknown"
            accuracy = " {0}%".format(round(100 - accuracy))
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    if face_found:
        face_detected_recently = True
        face_detection_time = time.time()
        elapsed_time = time.time() - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        cv2.putText(frame, f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)

        if alarm_playing:
            pygame.mixer.music.stop()
            alarm_playing = False
    else:
        if face_verified:
            if time.time() - face_detection_time >= delay_time:
                if not alarm_playing:
                    pygame.mixer.music.load(ALARM_MP3)
                    pygame.mixer.music.play()
                    alarm_playing = True
                frame = WARNING_IMAGE
                face_verified = False

    current_time = time.time()
    if current_time - start_time >= study_time_seconds:
        print("Study time is over!")
        pygame.mixer.music.load(FINISH_MP3)
        pygame.mixer.music.play()
        break

    if break_time_flag and current_time - break_start_time >= break_time_seconds:
        print("Break time is over!")
        pygame.mixer.music.load(BREAK_SOUND_MP3)
        pygame.mixer.music.play()
        break_time_flag = False
        start_time = current_time

    if current_time - start_time >= break_interval_seconds:
        print("Time for a break!")
        pygame.mixer.music.load(BREAK_SOUND_MP3)
        pygame.mixer.music.play()
        break_time_flag = True
        break_start_time = current_time

    cv2.imshow('Study Buddy', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
