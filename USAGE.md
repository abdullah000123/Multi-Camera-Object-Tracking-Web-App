# 📘 Usage Guide

Complete guide to using all features of the YOLOv8 Multi-Camera Object Detection System.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Image Detection Mode](#image-detection-mode)
3. [Multi-Camera Detection Mode](#multi-camera-detection-mode)
4. [Advanced Features](#advanced-features)
5. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### Starting the Application

1. **Open Terminal** and navigate to project directory:
   ```bash
   cd /path/to/yolov8-detection-system
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Start the server**:
   ```bash
   python app.py
   ```

4. **Open browser** and navigate to:
   - `http://localhost:5000` (local access)
   - `http://YOUR-IP-ADDRESS:5000` (network access from other devices)

### Stopping the Application

- Press `Ctrl+C` in the terminal to stop the server
- Close the terminal window
- Or deactivate virtual environment: `deactivate`

---

## Image Detection Mode

### Accessing Image Detection

- Navigate to: `http://localhost:5000/`
- Or click "YOLOv8n Object Detection" header from webcam mode

### Uploading Images

**Method 1: File Browser**
1. Click the purple "Choose File" button
2. Select an image from your computer
3. Supported formats: JPG, PNG, GIF, BMP
4. Maximum file size: 16MB

**Method 2: Drag and Drop**
1. Drag an image file from your computer
2. Drop it onto the upload area
3. The border will highlight when hovering

### Adjusting Detection Settings

**Confidence Threshold Slider**
- **Default**: 0.25 (25%)
- **Range**: 0.1 to 0.9
- **Lower values**: More detections (may include false positives)
- **Higher values**: Fewer detections (only high-confidence objects)

**Recommended Settings:**
- General use: 0.25 - 0.35
- High precision needed: 0.50 - 0.70
- Maximum detection: 0.10 - 0.20

### Running Detection

1. Upload an image using either method
2. Adjust confidence threshold if desired
3. Click "🔍 Detect Objects" button
4. Wait for processing (1-3 seconds typically)

### Understanding Results

**Detection Summary Display:**
```
Objects Found: 5

1. person
   Confidence: 92.45%

2. car
   Confidence: 87.23%

3. dog
   Confidence: 76.89%
```

**Annotated Image:**
- **Bounding boxes**: Colored rectangles around detected objects
- **Labels**: Object class name above each box
- **Confidence scores**: Percentage shown with class name
- **Color coding**: Each object class has a unique color

### Detecting Multiple Images

1. Click "🔄 New Image" button to reset
2. Upload a new image
3. Repeat detection process

---

## Multi-Camera Detection Mode

### Accessing Multi-Camera Mode

- Navigate to: `http://localhost:5000/webcam`
- Or click "📹 Switch to Live Webcam Detection" from image mode

### Interface Overview

The webcam interface has three main sections:

1. **Top Controls**: Camera selection, confidence, and action buttons
2. **Main Video Feed**: Live camera stream with annotations
3. **Right Panel**: Statistics, camera status, and activity logs

### Starting Detection

**Option 1: Start All Cameras**
1. Click "🚀 Start All Cameras" button
2. All detected cameras will start processing
3. View will show Camera 0 by default
4. Processing happens in parallel for all cameras

**Option 2: Start Individual Camera**
1. Find the camera in "Camera Status" panel
2. Click the "▶️ Start" button for specific camera
3. Only selected camera will start

**Initial Setup Time:**
- First camera: 5-10 seconds (model loading)
- Additional cameras: 2-3 seconds each

### Viewing Different Cameras

1. Use **"Select Camera to View"** dropdown at top
2. Select desired camera number
3. Video feed switches immediately
4. All cameras continue processing in background

**Important**: You can only view ONE camera at a time, but all cameras are processing simultaneously.

### Understanding the Video Feed

**On-Screen Information:**
- **Top left corner**: 
  ```
  Cam 0 | InZone: 3 | Total: 7
  ```
  - `Cam 0`: Current camera ID
  - `InZone`: Objects inside drawn polygon
  - `Total`: Total objects detected in frame

**Bounding Boxes:**
- Red/blue/green boxes around detected objects
- Class labels above boxes
- Confidence percentages shown

**Polygon Zone:**
- Semi-transparent green overlay
- Green boundary line
- Green dots on object centers inside zone

### Drawing Detection Zones

Detection zones allow you to count objects only in specific areas.

**Step 1: Enter Drawing Mode**
1. Ensure a camera is running
2. Select camera you want to draw on
3. Click "✏️ Draw Zone (Current Camera)"
4. Cursor changes to crosshair

**Step 2: Draw Polygon**
1. Click on video feed to place points
2. Minimum 3 points required
3. Points automatically connect in order
4. A message shows point count

**Step 3: Complete Polygon**
- **Press Enter**: Finalize polygon
- **Press Escape**: Cancel drawing
- Polygon automatically closes between last and first point

**Step 4: Verify Zone**
- Green overlay appears on defined area
- Only objects with centers inside zone are counted
- Zone persists until cleared

**Tips for Drawing:**
- Start from a corner and work clockwise/counterclockwise
- Use 4-6 points for simple rectangular zones
- More points = more complex shapes (but slower processing)
- Click precisely on desired boundaries

### Managing Zones

**Clear Zone for Current Camera:**
1. Click "🗑️ Clear Zone" button
2. Polygon removed immediately
3. Detection continues for all objects

**Clear Zone for Different Camera:**
1. Switch to that camera using dropdown
2. Click "🗑️ Clear Zone"

**Important**: Each camera has its own independent polygon zone.

### Individual Camera Controls

Located in the "Camera Status" panel:

**▶️ Start Button**
- Begins detection on stopped camera
- Takes 2-3 seconds to initialize
- Becomes disabled when camera is running

**⏸️ Pause Button**
- Temporarily stops camera processing
- Preserves polygon zone
- Quick resume available
- Useful for reducing CPU usage

**⏹️ Stop Button**
- Completely stops camera
- Releases camera resource
- Clears detection data
- Requires restart to resume

### Reading Camera Statistics

**Per-Camera Stats** (Right Panel):
```
Camera 0 [Running]
In Zone: 3 | Total: 5 | FPS: 28.5

Camera 1 [Stopped]
In Zone: 0 | Total: 0 | FPS: 0.0
```

**Meanings:**
- **Running/Stopped**: Current camera state
- **In Zone**: Objects inside polygon (if drawn)
- **Total**: All detected objects in frame
- **FPS**: Processing speed (higher is better)

**Typical FPS Values:**
- 25-30 FPS: Excellent performance
- 15-25 FPS: Good performance
- 10-15 FPS: Acceptable performance
- <10 FPS: Poor performance (reduce load)

### Detection Summary Panel

Shows real-time counts of objects in zones:

```
📊 Detection Summary

Objects Inside Zone

person: 2
car: 1
bicycle: 1

Current Status
Inside Zone: 4 | Outside: 3
```

**Object Counts:**
- Lists each detected class
- Shows MAX count across all cameras
- Updates in real-time
- Only counts objects in zones (if zones are drawn)

### Activity Log

Tracks entry/exit events with timestamps:

```
GLOBAL | person ENTERED | Max: 2
Camera: GLOBAL
2026-02-04 14:23:15

Camera 0 | car EXITED
Camera: Camera 0  
2026-02-04 14:23:20
```

**Log Entry Types:**

1. **ENTERED (Green)**
   - Object class first detected in zone
   - Shows maximum count seen
   - Global or per-camera event

2. **EXITED (Red)**  
   - Object class no longer in zone
   - Triggered after 1-second timeout
   - Shows max count that was present

3. **GLOBAL (Orange)**
   - Aggregated across all cameras
   - Uses MAX logic (highest count from any camera)
   - Unified tracking for entire system

**Understanding Global Logs:**

The system uses intelligent global tracking:
- If Camera 0 sees 2 people and Camera 1 sees 3 people
- Global count = 3 (maximum)
- When both cameras drop to 0, one EXIT event logged

**Clearing Logs:**
- Click "🗑️ Clear All Logs" button
- Removes all entries
- Does not affect current detections
- Cannot be undone

### System Status Check

**Purpose**: Debug and verify system state

**How to Use:**
1. Click "🔍 Check System Status" button
2. Popup shows detailed diagnostics

**Information Displayed:**
```
=== SYSTEM STATUS ===

Available Cameras: 0, 1, 2
Initialized Cameras: 0, 1

Camera Details:

Camera 0:
  Running: true
  Thread Alive: true
  Has Frame: true
  Has Capture: true
  FPS: 28.3
  Objects in Zone: {"person": 2, "car": 1}

Camera 1:
  Running: false
  Thread Alive: false
  Has Frame: false
  Has Capture: false
  FPS: 0.0
  Objects in Zone: {}
```

**Use Cases:**
- Troubleshooting camera issues
- Verifying camera detection
- Checking thread health
- Monitoring performance

---

## Advanced Features

### Adjusting Confidence During Detection

1. **While cameras are running**, you can adjust confidence
2. Move the slider to new value
3. Stop and restart cameras for changes to take effect
4. Each camera uses confidence set at start time

### Network Access

**Accessing from Other Devices:**

1. Find your Mac's IP address:
   ```bash
   ipconfig getifaddr en0  # WiFi
   ipconfig getifaddr en1  # Ethernet
   ```

2. On another device (phone, tablet, laptop):
   - Connect to same WiFi network
   - Open browser
   - Navigate to: `http://YOUR-MAC-IP:5000`

**Use Cases:**
- Monitor from across the room
- Multiple people viewing same feed
- Mobile device control panel

### Multiple Browser Windows

You can open multiple browser windows/tabs:
- Each can view a different camera
- All use same backend processing
- Statistics synchronized across all windows
- Useful for monitoring multiple views

### Hotkeys (Drawing Mode Only)

- **Enter**: Complete polygon drawing
- **Escape**: Cancel polygon drawing
- **Click**: Add polygon point

---

## Tips & Best Practices

### Optimal Camera Placement

**For Best Detection:**
- Mount camera at 45° angle looking down
- Avoid extreme angles (straight down = poor detection)
- Ensure good lighting
- Minimize camera shake
- Clear field of view

**Zone Drawing:**
- Draw zones in well-lit areas
- Avoid edges of frame (distortion)
- Test with actual objects before deployment

### Performance Optimization

**If FPS is low (<15):**

1. **Reduce resolution** in `app.py`:
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```

2. **Use smaller model**:
   ```python
   YOLO('yolo11n.pt')  # Fastest
   ```

3. **Increase confidence threshold** (fewer detections)

4. **Run fewer cameras simultaneously**

5. **Close other applications**

6. **Use wired cameras** instead of wireless

### Accuracy Improvements

**For Better Detection:**

1. **Increase confidence threshold** (0.4 - 0.6)
2. **Use larger model** (yolo11m.pt or yolo11l.pt)
3. **Improve lighting** conditions
4. **Reduce camera motion**
5. **Position objects clearly** in frame

### Battery/Power Management

**For Laptops:**
- Expect higher power consumption
- Connect to power adapter for extended use
- Disable unused cameras to save battery
- Lower FPS target if needed

### Deployment Scenarios

**Retail Store:**
- Use zones for entry/exit counting
- Monitor customer flow
- Track high-traffic areas

**Security:**
- Multiple camera coverage
- Zone-based alerts
- Activity logging for review

**Warehouse:**
- Package counting
- Worker presence detection
- Vehicle tracking

**Research:**
- Animal behavior tracking
- Crowd counting
- Object flow analysis

### Data Management

**Activity Logs:**
- Download/export not built-in (future feature)
- Copy from browser for record-keeping
- Regularly clear logs to prevent memory issues

**Detection Images:**
- Single images saved to `static/results/`
- Webcam frames not saved (real-time only)
- Manually save results if needed

---

## Keyboard Shortcuts Reference

| Key | Action | Context |
|-----|--------|---------|
| Enter | Complete polygon | Drawing mode |
| Escape | Cancel polygon | Drawing mode |
| Ctrl+C | Stop server | Terminal |

---

## Troubleshooting Common Usage Issues

### "No cameras detected"
- Check camera connections
- Grant camera permissions
- Restart application
- Try clicking "🔍 Check System Status"

### Polygon won't complete
- Ensure 3+ points placed
- Press Enter key
- Check if drawing mode is active
- Try clicking "✏️ Draw Zone" again

### Video feed frozen
- Check FPS in camera stats
- Stop and restart camera
- Refresh browser page
- Check terminal for errors

### Objects not being detected
- Lower confidence threshold
- Improve lighting
- Ensure objects in frame
- Check if camera is actually running

### Count seems wrong
- Verify polygon includes target area
- Check if objects' centers are in zone
- Review "Total" vs "In Zone" numbers
- Objects must be >confidence% to count

---

**Need More Help?**
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Check [API.md](API.md) for technical details
- Review [README.md](README.md) for overview

Last Updated: February 2026
