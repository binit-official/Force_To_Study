import cv2

# Initialize the camera
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)  # Set video width
cam.set(4, 480)  # Set video height

# Load Haar Cascade for face detection
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Input the user's ID
face_id = input("Enter a Numeric user ID here: ")

print("Taking samples, look at the camera...")
count = 0

while True:
    ret, img = cam.read()
    if not ret:
        break

    # Convert image to grayscale
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(converted_image, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        # Save the captured face in the dataset folder
        cv2.imwrite(f"samplles/face.{str(face_id)}.{str(count)}.jpg", converted_image[y:y+h, x:x+w])
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:  # Press 'ESC' to exit
        break
    elif count >= 10:  # Take 10 samples and then stop
        break

print("Samples taken, now closing the program...")
cam.release()
cv2.destroyAllWindows()
