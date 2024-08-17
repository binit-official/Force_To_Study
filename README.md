# Study Buddy 📚

**Study Buddy** is a productivity tool designed to help you stay focused during study sessions. It uses facial detection to ensure you remain seated at your desk, and it reminds you to take breaks at regular intervals. With the added feature of alarm sounds and visual warnings, Study Buddy keeps you on track and helps you manage your time effectively.

## Features
- **Face Detection**: The program starts with the face detection and also detects if you are present during study sessions. If you leave, an alarm will sound after 20 seconds.
- **Model Training**: The program is designed in a way that new faces/user can also enroll their faces so that they can use it.
- **Customizable Timers**: Set your desired study time, break time, and break intervals.
- **Break Reminders**: Alerts you when it's time to take a break.
- **Warning Image**: Displays a warning image if you leave your study space.
- **Sound Alerts**: Plays different sounds for study completion, break reminders, and when you've left your seat.

## Getting Started

### Prerequisites
- Python 3.x
- OpenCV (`cv2`)
- Pygame (`pygame`)

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/study-buddy.git
    cd study-buddy
    ```

2. Install the required libraries:
    ```bash
    pip install opencv-python pygame
    ```

3. Place your alarm sounds and warning image in the project directory:
    - `alert.mp3`: Sound for when you leave your seat.
    - `break.mp3`: Sound for break reminders.
    - `finish.mp3`: Sound for when the study time is over.
    - `warning.jpg`: Warning image displayed when you leave your seat.

### Usage
1. Run the script:
    ```bash
    python study_buddy.py
    ```

2. Enter your desired study time, break time, and break interval when prompted. Example inputs:
    - Study time: `1h30m`
    - Break time: `10m`
    - Break interval: `30m`

3. The program will start, and you'll see the camera feed with a timer overlay. Make sure your face is visible to the camera.

4. **Study Time**: The timer will track your study session. If you leave your seat, the alarm will sound after 10 seconds, and a warning image will be displayed.

5. **Break Time**: When it's time for a break, a sound alert will notify you.

6. Press `q` to quit the program at any time.

## File Structure

YourProjectFolder/

    
    |
    ├── samplles/                  # Contains face samples for training
    │   ├── face.1.1.jpg
    │   ├── face.1.2.jpg
    │   └── ...
    │
    ├── trainer/                   # Contains the trained model file
    │   └── trainer.yml
    │
    ├── haarcascade_frontalface_default.xml  # Haar Cascade XML file
    │
    ├── samplergenerator.py        # Face sample generation script
    ├── modeltrainer.py            # Model training script
    ├── main.py             # Study Buddy script and Original face recognition script





## Customization
- You can change the alarm and break sounds by replacing the `alert.mp3`, `break.mp3`, and `finish.mp3` files.
- Modify the face detection parameters (`scaleFactor`, `minNeighbors`) to adjust the sensitivity.

## Contributing
Feel free to fork this repository and contribute by submitting a pull request. Improvements, new features, and bug fixes are welcome!

## License
This project is licensed under the MIT License.

## Acknowledgements
- OpenCV for providing an easy-to-use face detection library.
- Pygame for handling audio playback.
