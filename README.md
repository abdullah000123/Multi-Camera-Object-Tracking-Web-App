# 🎯 YOLOv8 Multi-Camera Object Detection System

A powerful real-time object detection system built with YOLOv8, Flask, and OpenCV. Supports both single image detection and parallel multi-camera live detection with custom zone monitoring.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 📸 Image Detection Mode
- Upload images for instant object detection
- Adjustable confidence threshold (0.1 - 0.9)
- Beautiful gradient UI with drag-and-drop support
- Detailed detection results with class names and confidence scores
- Support for JPG, PNG, GIF, and BMP formats

### 📹 Multi-Camera Live Detection
- **Parallel Processing**: Run multiple cameras simultaneously
- **Independent Tracking**: Each camera has its own YOLO model instance
- **Custom Zone Monitoring**: Draw custom polygons to define detection zones
- **Real-time Statistics**: Live FPS, object counts, and activity logs
- **Global Object Tracking**: Unified tracking across all cameras
- **Per-Camera Controls**: Start, pause, or stop individual cameras
- **Activity Logging**: Track object entry/exit events with timestamps

## 🚀 Quick Start

### Prerequisites

- **macOS** (tested on macOS 10.14+)
- **Homebrew** (will be installed automatically if not present)
- **Python 3.11 or 3.12** (will be installed via Homebrew if needed)
- **Webcam(s)** connected to your Mac

### Installation

1. **Clone or download this project**
   ```bash
   cd /path/to/project
   ```

2. **Make the setup script executable**
   ```bash
   chmod +x setup.sh
   ```

3. **Run the setup script**
   ```bash
   ./setup.sh
   ```

   The script will automatically:
   - ✅ Check/install Homebrew
   - ✅ Check/install Python 3.11 or 3.12
   - ✅ Create a virtual environment
   - ✅ Install PyTorch with MPS (Apple Silicon) support
   - ✅ Install YOLOv8 (Ultralytics)
   - ✅ Install Flask 3.0.0
   - ✅ Start the application

4. **Access the application**
   
   After setup completes, the Flask server will start. You'll see output like:
   ```
   * Running on http://0.0.0.0:5000
   * Running on http://192.168.1.xxx:5000
   ```
   
   Open your browser and navigate to:
   - Local: `http://localhost:5000`
   - Network: `http://YOUR-IP-ADDRESS:5000`

## 📖 Usage Guide

### Image Detection Mode

1. **Navigate to the home page** (`http://localhost:5000`)
2. **Upload an image**:
   - Click "Choose File" button, OR
   - Drag and drop an image onto the upload area
3. **Adjust confidence threshold** (optional)
   - Use the slider to set detection sensitivity (default: 0.25)
4. **Click "🔍 Detect Objects"**
5. **View results**:
   - Annotated image with bounding boxes
   - List of detected objects with confidence scores

### Multi-Camera Detection Mode

1. **Navigate to webcam mode**:
   - Click "📹 Switch to Live Webcam Detection" from home page, OR
   - Go directly to `http://localhost:5000/webcam`

2. **Start cameras**:
   - Click "🚀 Start All Cameras" to activate all detected cameras
   - Individual cameras can be controlled via the Camera Status panel

3. **Select camera to view**:
   - Use the "Select Camera to View" dropdown
   - Only one feed displays at a time, but all run in parallel

4. **Draw detection zone** (optional):
   - Click "✏️ Draw Zone (Current Camera)"
   - Click on the video feed to add polygon points
   - Press **Enter** to complete the polygon
   - Press **Escape** to cancel
   - Only objects inside the zone will be counted

5. **Monitor activity**:
   - **Detection Summary**: Real-time count of objects in zone
   - **Camera Status**: FPS, detection counts per camera
   - **Activity Log**: Entry/exit events with timestamps

6. **Controls**:
   - **Start**: Begin detection on individual camera
   - **Pause**: Temporarily pause camera feed
   - **Stop**: Completely stop camera processing
   - **Clear Zone**: Remove polygon for current camera
   - **Clear All Logs**: Reset activity log

## 🏗️ Project Structure

```
project/
├── app.py                    # Flask backend server
├── setup.sh                  # Automated setup script
├── index.html               # Image detection page
├── webcam_parallel.html     # Multi-camera detection page
├── static/
│   ├── uploads/            # Temporary uploaded images
│   └── results/            # Detection result images
├── venv/                   # Virtual environment (created by setup)
└── README.md              # This file
```

## 🔧 Technical Details

### Backend Architecture

- **Framework**: Flask 3.0.0
- **Object Detection**: YOLOv11s (Ultralytics)
- **Computer Vision**: OpenCV (cv2)
- **Threading**: Independent threads per camera for parallel processing
- **Image Processing**: NumPy for efficient array operations

### Frontend Architecture

- **UI Framework**: Pure HTML5/CSS3/JavaScript
- **Styling**: Gradient design with modern CSS
- **Video Feed**: Continuous JPEG frame polling
- **Real-time Updates**: Periodic AJAX requests for statistics

### Detection Pipeline

1. **Frame Capture**: OpenCV captures frames from webcam
2. **YOLO Inference**: YOLOv11s processes frames (640x480 @ 30fps target)
3. **Polygon Filtering**: Optional zone-based filtering using ray-casting algorithm
4. **Annotation**: Bounding boxes and labels drawn on frames
5. **Global Aggregation**: MAX logic combines detections across cameras
6. **Activity Tracking**: Entry/exit events logged with timestamps

### Polygon Detection Algorithm

- **Method**: Ray Casting Algorithm
- **Purpose**: Determine if object center point is inside custom zone
- **Complexity**: O(n) where n is number of polygon vertices
- **Visual Feedback**: Semi-transparent green overlay on defined zones

## ⚙️ Configuration

### Adjustable Parameters in `app.py`

```python
# File upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'avi', 'mov'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Camera settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
TARGET_FPS = 30

# Tracking settings
TRACK_TIMEOUT = 3.0          # Seconds before track is considered lost
TRACK_LOST_TIMEOUT = 1.0     # Seconds before lost track is removed
CLASS_EXIT_TIMEOUT = 1.0     # Seconds before object exit is logged

# Performance
SHOW_FPS_IN_TERMINAL = False  # Set to True for FPS debugging
```

### YOLO Model Selection

The project uses `yolo11s.pt` by default. You can change the model in `app.py`:

```python
# In get_model_for_camera() function
camera_models[camera_id] = YOLO('yolo11s.pt')  # Options: yolo11n.pt, yolo11s.pt, yolo11m.pt, yolo11l.pt, yolo11x.pt
```

**Model Comparison:**
- **yolo11n**: Fastest, lowest accuracy (~2ms)
- **yolo11s**: Balanced speed/accuracy (~3ms) ✅ **Default**
- **yolo11m**: Medium speed, better accuracy (~6ms)
- **yolo11l**: Slower, high accuracy (~10ms)
- **yolo11x**: Slowest, highest accuracy (~15ms)

## 🐛 Troubleshooting

### Camera Not Detected

```bash
# Check available cameras manually
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

If cameras aren't detected:
1. Check camera permissions in System Preferences > Security & Privacy > Camera
2. Try unplugging and reconnecting cameras
3. Restart the application
4. Check if other apps are using the camera

### Port Already in Use

If port 5000 is occupied:

```python
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)  # Change to 5001 or any available port
```

### Low FPS / Performance Issues

1. **Reduce resolution**:
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # Lower from 640
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Lower from 480
   ```

2. **Use smaller YOLO model**:
   ```python
   YOLO('yolo11n.pt')  # Fastest model
   ```

3. **Reduce number of concurrent cameras**

4. **Increase confidence threshold** to reduce detections

### Module Import Errors

If you see import errors after setup:

```bash
# Manually activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install torch torchvision torchaudio ultralytics flask==3.0.0
```

### macOS Permission Issues

Grant terminal/IDE camera access:
1. Open **System Preferences** > **Security & Privacy** > **Camera**
2. Enable camera access for **Terminal** or your IDE (VS Code, PyCharm, etc.)
3. Restart the application

## 📊 API Endpoints

### Image Detection
- `POST /upload` - Upload image for detection
  - Parameters: `file`, `confidence`
  - Returns: JSON with detections and result image path

### Camera Management
- `POST /start_camera` - Start specific camera
- `POST /pause_camera` - Pause specific camera  
- `POST /stop_camera` - Stop specific camera
- `POST /start_all_cameras` - Start all detected cameras
- `POST /stop_all_cameras` - Stop all cameras
- `GET /get_cameras` - List available camera indices

### Zone Management
- `POST /set_polygon` - Set detection zone polygon
- `GET /get_polygon` - Get current polygon points
- `POST /clear_polygon` - Clear detection zone

### Statistics & Logs
- `GET /get_camera_stats` - Get real-time camera statistics
- `GET /get_logs` - Get activity log entries
- `POST /clear_logs` - Clear all activity logs
- `GET /get_system_status` - Detailed system diagnostic info

### Video Feed
- `GET /video_feed?camera=<index>` - JPEG frame stream for specific camera

## 🎨 Customization

### Change UI Colors

Edit the CSS gradient in `index.html` or `webcam_parallel.html`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Replace color codes with your preferred gradient.

### Adjust Detection Zones

Modify polygon drawing behavior in `webcam_parallel.html`:

```javascript
// Minimum points required for polygon
if (tempPolygonPoints.length >= 3) {  // Change to 4 for rectangles only
    finishDrawing();
}
```

## 🔐 Security Considerations

⚠️ **This application is designed for local/development use only.**

For production deployment:
- Add authentication (Flask-Login, JWT)
- Implement HTTPS with SSL certificates
- Add CORS protection
- Sanitize file uploads more thoroughly
- Rate limit API endpoints
- Use production WSGI server (Gunicorn, uWSGI)

## 📝 Requirements

### Python Packages
```
torch>=2.0.0
torchvision>=0.15.0
ultralytics>=8.0.0
flask==3.0.0
opencv-python>=4.8.0
numpy>=1.24.0
```

### System Requirements
- **OS**: macOS 10.14+
- **RAM**: 8GB minimum, 16GB recommended
- **CPU**: Multi-core processor (Apple M1/M2 preferred)
- **Storage**: 2GB free space for models and dependencies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd <project-directory>

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in debug mode
python app.py
```

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- **Ultralytics** - YOLOv8/YOLOv11 implementation
- **Flask** - Web framework
- **OpenCV** - Computer vision library
- **PyTorch** - Deep learning framework

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section above

---

**Made with ❤️ using YOLOv11 and Flask**

Last Updated: February 2026
