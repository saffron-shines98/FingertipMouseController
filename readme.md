# Fingertip Mouse Controller

A computer vision-based mouse controller that uses hand gestures to control your computer's cursor and mouse clicks.

## Features

- **Cursor Control**: Move your cursor by pointing your index finger
- **Click Gesture**: Perform mouse clicks by pinching your thumb and index finger together
- **Smooth Movement**: Built-in smoothing to reduce cursor jitter
- **Real-time Processing**: Live camera feed with hand landmark visualization

## Requirements

- Python 3.7 or higher
- Webcam/Camera
- Windows, macOS, or Linux

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python fingertip_mouse_controller.py
```

2. Position yourself in front of your camera with good lighting
3. Hold up one hand in view of the camera
4. Use gestures to control your mouse:
   - **Move Cursor**: Point your index finger where you want the cursor to go
   - **Click**: Bring your thumb and index finger close together (pinch gesture)

## Controls

- **'q'**: Quit the application
- **'ESC'**: Emergency stop
- **Move cursor to top-left corner**: PyAutoGUI failsafe (if enabled)

## Configuration

You can modify these parameters in the code:

- `click_threshold`: Distance threshold for click detection (default: 30)
- `smoothing_factor`: Cursor smoothing intensity (default: 0.3)
- `min_detection_confidence`: Hand detection confidence (default: 0.7)
- `min_tracking_confidence`: Hand tracking confidence (default: 0.5)

## Troubleshooting

- **Camera not working**: Ensure your camera is not being used by another application
- **Hand not detected**: Improve lighting conditions and ensure your hand is clearly visible
- **Cursor too sensitive**: Increase the `smoothing_factor` value
- **Clicks not registering**: Adjust the `click_threshold` value

## System Requirements

- OpenCV for computer vision processing
- MediaPipe for hand landmark detection
- PyAutoGUI for mouse control
- NumPy for mathematical operations

## Notes

- The application uses your default camera (index 0)
- Camera feed is mirrored for natural interaction
- PyAutoGUI failsafe is enabled by default for safety
