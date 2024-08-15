import cv2
import time
import pygame

# Load the face detection cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the camera
cap = cv2.VideoCapture(0)

# Ask user for study time and break time
print("Welcome to the Study Buddy!")
study_time = input("How much time do you want to sit for study? (e.g., 1h, 30m, 2h30m): ")
break_time = input("How much break time do you want? (e.g., 10m, 30m): ")
break_interval = input("How often do you want to take a break? (e.g., 30m): ")

# Convert study time, break time, and break interval to seconds
study_time_seconds = 0
break_time_seconds = 0
break_interval_seconds = 0

if "h" in study_time:
    hours = int(study_time.split("h")[0])
    study_time_seconds += hours * 3600
if "m" in study_time:
    minutes = int(study_time.split("m")[0].split("h")[-1])
    study_time_seconds += minutes * 60

if "m" in break_time:
    minutes = int(break_time.split("m")[0])
    break_time_seconds += minutes * 60

if "m" in break_interval:
    minutes = int(break_interval.split("m")[0])
    break_interval_seconds += minutes * 60

print(f"Study time: {study_time_seconds} seconds")
print(f"Break time: {break_time_seconds} seconds")
print(f"Break interval: {break_interval_seconds} seconds")

# Set the alarm MP3 file
ALARM_MP3 = 'E:/Projects/Force_To_Study/alert.mp3'
BREAK_SOUND_MP3 = 'E:/Projects/Force_To_Study/break.mp3'
FINISH_MP3 = 'E:/Projects/Force_To_Study/finish.mp3'

# Load the warning image
WARNING_IMAGE = cv2.imread('E:/Projects/Force_To_Study/warning.jpg')

# Initialize the start time
start_time = time.time()

# Initialize the face detected recently flag
face_detected_recently = True
face_detection_time = time.time()

# Initialize the alarm playing flag
alarm_playing = False

# Initialize the break time flag
break_time_flag = False

# Initialize the pygame mixer
pygame.mixer.init()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if a face is detected
    if len(faces) > 0:
        # Draw a green rectangle around the face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Set the face detected recently flag to True
        face_detected_recently = True
        face_detection_time = time.time()

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        # Draw the timer on the frame
        cv2.putText(frame, f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)

        # If the alarm was playing, stop it
        if alarm_playing:
            pygame.mixer.music.stop()
            alarm_playing = False
    else:
        # Check if 10 seconds have passed since the last face detection
        if time.time() - face_detection_time >= 10:
            # Play the alarm MP3 if it's not already playing
            if not alarm_playing:
                pygame.mixer.music.load(ALARM_MP3)
                pygame.mixer.music.play()
                alarm_playing = True

            # Display the warning image
            frame = WARNING_IMAGE

        # Check if the study time has elapsed
    current_time = time.time()
    if current_time - start_time >= study_time_seconds:
        print("Study time is over!")
        pygame.mixer.music.load(FINISH_MP3)
        pygame.mixer.music.play()
        break

    # Check if the break time has elapsed
    if break_time_flag and current_time - break_start_time >= break_time_seconds:
        print("Break time is over!")
        pygame.mixer.music.load(BREAK_SOUND_MP3)
        pygame.mixer.music.play()
        break_time_flag = False
        start_time = current_time

    # Check if the break interval has elapsed
    if current_time - start_time >= break_interval_seconds:
        print("Time for a break!")
        pygame.mixer.music.load(BREAK_SOUND_MP3)
        pygame.mixer.music.play()
        break_time_flag = True
        break_start_time = current_time

    # Display the frame
    cv2.imshow('Study Buddy', frame)

    # Exit on key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Stop the pygame mixer
pygame.mixer.quit()