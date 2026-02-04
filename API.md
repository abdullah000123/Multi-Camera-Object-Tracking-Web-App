# 🔌 API Documentation

Complete REST API reference for the YOLOv8 Multi-Camera Object Detection System.

## Base URL

```
http://localhost:5000
```

## Table of Contents
1. [Image Detection Endpoints](#image-detection-endpoints)
2. [Camera Management Endpoints](#camera-management-endpoints)
3. [Zone Management Endpoints](#zone-management-endpoints)
4. [Statistics Endpoints](#statistics-endpoints)
5. [Video Feed Endpoints](#video-feed-endpoints)
6. [Error Handling](#error-handling)

---

## Image Detection Endpoints

### Upload Image for Detection

Upload an image and receive object detection results.

**Endpoint:** `POST /upload`

**Request:**
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file` (file, required): Image file to analyze
  - `confidence` (float, optional): Detection confidence threshold (default: 0.25)

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@/path/to/image.jpg" \
  -F "confidence=0.3"
```

**Example using Python requests:**
```python
import requests

url = "http://localhost:5000/upload"
files = {"file": open("image.jpg", "rb")}
data = {"confidence": 0.3}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Example using JavaScript:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('confidence', 0.3);

fetch('http://localhost:5000/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response (Success):**
```json
{
    "success": true,
    "total_objects": 5,
    "result_image": "/static/results/result_1234567890.jpg",
    "detections": [
        {
            "class": "person",
            "confidence": 0.92,
            "bbox": [120.5, 80.3, 350.7, 450.2]
        },
        {
            "class": "car",
            "confidence": 0.87,
            "bbox": [400.1, 200.5, 600.3, 380.9]
        }
    ]
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "No file provided"
}
```

**Status Codes:**
- `200 OK`: Detection successful
- `400 Bad Request`: Invalid file or parameters
- `500 Internal Server Error`: Detection failed

---

## Camera Management Endpoints

### List Available Cameras

Get list of all available camera indices.

**Endpoint:** `GET /get_cameras`

**Request:**
```bash
curl http://localhost:5000/get_cameras
```

**Response:**
```json
[0, 1, 2]
```

**Notes:**
- Scans up to 10 potential camera indices
- Returns only cameras that can capture frames
- Empty array if no cameras detected

---

### Start Specific Camera

Start detection on a single camera.

**Endpoint:** `POST /start_camera`

**Request:**
- **Content-Type:** `application/json`
- **Body:**
  ```json
  {
      "camera_id": 0,
      "confidence": 0.25
  }
  ```

**Example:**
```bash
curl -X POST http://localhost:5000/start_camera \
  -H "Content-Type: application/json" \
  -d '{"camera_id": 0, "confidence": 0.3}'
```

**Response (Success):**
```json
{
    "success": true,
    "message": "Camera 0 started",
    "camera_id": "0"
}
```

**Response (Error):**
```json
{
    "success": false,
    "message": "Camera 0 already running"
}
```

---

### Pause Specific Camera

Temporarily pause a running camera.

**Endpoint:** `POST /pause_camera`

**Request:**
```json
{
    "camera_id": "0"
}
```

**Response:**
```json
{
    "success": true,
    "camera_id": "0"
}
```

**Notes:**
- Camera thread remains alive
- Can be quickly resumed
- Polygon zone preserved

---

### Stop Specific Camera

Completely stop a camera.

**Endpoint:** `POST /stop_camera`

**Request:**
```json
{
    "camera_id": "0"
}
```

**Response:**
```json
{
    "success": true,
    "camera_id": "0"
}
```

**Notes:**
- Camera thread terminated
- Resources fully released
- Requires restart to use again

---

### Start All Cameras

Start detection on all available cameras.

**Endpoint:** `POST /start_all_cameras`

**Request:**
```json
{
    "confidence": 0.25
}
```

**Response:**
```json
{
    "success": true,
    "started_cameras": [0, 1, 2],
    "failed_cameras": []
}
```

---

### Stop All Cameras

Stop all running cameras.

**Endpoint:** `POST /stop_all_cameras`

**Request:** No body required

**Response:**
```json
{
    "success": true,
    "stopped_cameras": ["0", "1", "2"]
}
```

---

## Zone Management Endpoints

### Set Polygon Zone

Define a detection zone polygon for a specific camera.

**Endpoint:** `POST /set_polygon`

**Request:**
```json
{
    "camera_id": "0",
    "points": [
        {"x": 100, "y": 150},
        {"x": 500, "y": 150},
        {"x": 500, "y": 400},
        {"x": 100, "y": 400}
    ]
}
```

**Response:**
```json
{
    "success": true,
    "camera_id": "0"
}
```

**Notes:**
- Minimum 3 points required
- Points in pixel coordinates
- Polygon automatically closed
- Overwrites existing polygon

---

### Get Polygon Zone

Retrieve current polygon for a camera.

**Endpoint:** `GET /get_polygon`

**Parameters:**
- `camera_id` (query string): Camera ID (default: "0")

**Request:**
```bash
curl "http://localhost:5000/get_polygon?camera_id=0"
```

**Response:**
```json
{
    "camera_id": "0",
    "points": [
        [100, 150],
        [500, 150],
        [500, 400],
        [100, 400]
    ]
}
```

---

### Clear Polygon Zone

Remove polygon and reset detection zone.

**Endpoint:** `POST /clear_polygon`

**Request:**
```json
{
    "camera_id": "0"
}
```

**Response:**
```json
{
    "success": true,
    "camera_id": "0"
}
```

**Effects:**
- Polygon removed
- All objects counted (no zone filtering)
- Activity logs for this camera cleared
- Track states reset

---

## Statistics Endpoints

### Get Camera Statistics

Retrieve real-time statistics for all cameras.

**Endpoint:** `GET /get_camera_stats`

**Request:**
```bash
curl http://localhost:5000/get_camera_stats
```

**Response:**
```json
{
    "stats": {
        "0": {
            "is_running": true,
            "in_zone": 3,
            "total_detections": 7,
            "fps": 28.5,
            "active_tracks": 5
        },
        "1": {
            "is_running": false,
            "in_zone": 0,
            "total_detections": 0,
            "fps": 0.0,
            "active_tracks": 0
        }
    }
}
```

**Field Descriptions:**
- `is_running`: Camera actively processing
- `in_zone`: Objects inside polygon zone
- `total_detections`: All objects in frame
- `fps`: Processing frames per second
- `active_tracks`: Number of tracked objects

---

### Get Activity Logs

Retrieve entry/exit event logs.

**Endpoint:** `GET /get_logs`

**Request:**
```bash
curl http://localhost:5000/get_logs
```

**Response:**
```json
{
    "logs": [
        {
            "timestamp": "2026-02-04 14:23:15",
            "camera_id": "GLOBAL",
            "object": "person",
            "action": "ENTERED",
            "max_count": 2
        },
        {
            "timestamp": "2026-02-04 14:23:20",
            "camera_id": "0",
            "object": "car",
            "action": "EXITED",
            "max_count": 1
        }
    ]
}
```

**Log Entry Fields:**
- `timestamp`: ISO format datetime
- `camera_id`: Camera ID or "GLOBAL"
- `object`: Detected class name
- `action`: "ENTERED" or "EXITED"
- `max_count`: Maximum count seen (for GLOBAL logs)

---

### Clear Activity Logs

Delete all activity log entries.

**Endpoint:** `POST /clear_logs`

**Request:** No body required

**Response:**
```json
{
    "success": true
}
```

---

### Get System Status

Detailed diagnostic information.

**Endpoint:** `GET /get_system_status`

**Request:**
```bash
curl http://localhost:5000/get_system_status
```

**Response:**
```json
{
    "available_cameras": [0, 1, 2],
    "initialized_cameras": ["0", "1"],
    "camera_details": {
        "0": {
            "is_running": true,
            "has_frame": true,
            "has_cap": true,
            "thread_alive": true,
            "polygon_points": 4,
            "objects_in_zone": {"person": 2, "car": 1},
            "fps": 28.3
        }
    }
}
```

---

## Video Feed Endpoints

### Get Video Frame

Retrieve current annotated frame from camera.

**Endpoint:** `GET /video_feed`

**Parameters:**
- `camera` (query string): Camera index (default: 0)

**Request:**
```bash
curl "http://localhost:5000/video_feed?camera=0" -o frame.jpg
```

**Response:**
- **Content-Type:** `image/jpeg`
- **Body:** JPEG image binary data

**Status Codes:**
- `200 OK`: Frame available
- `204 No Content`: Camera running but no frame yet
- `404 Not Found`: Camera not initialized
- `500 Internal Server Error`: Frame encoding failed

**Usage in HTML:**
```html
<img src="http://localhost:5000/video_feed?camera=0" id="videoFrame">

<script>
// Auto-refresh every 100ms
setInterval(() => {
    document.getElementById('videoFrame').src = 
        'http://localhost:5000/video_feed?camera=0&t=' + new Date().getTime();
}, 100);
</script>
```

**Notes:**
- Returns single frame (not streaming)
- Includes all annotations (boxes, labels, polygon)
- JPEG quality: 85%
- No caching (always fresh frame)

---

## Static File Endpoints

### Get Result Image

**Endpoint:** `GET /static/results/<filename>`

Retrieve saved detection result image.

**Example:**
```
http://localhost:5000/static/results/result_1234567890.jpg
```

---

### Web Pages

**Home Page (Image Detection):**
```
GET http://localhost:5000/
```

**Webcam Page (Multi-Camera):**
```
GET http://localhost:5000/webcam
```

---

## Error Handling

### Common Error Responses

**Invalid File Type:**
```json
{
    "success": false,
    "error": "File type not allowed. Supported: png, jpg, jpeg, gif, bmp"
}
```

**No File Provided:**
```json
{
    "success": false,
    "error": "No file provided"
}
```

**Camera Not Available:**
```json
{
    "success": false,
    "message": "Camera 5 not available"
}
```

**Camera Already Running:**
```json
{
    "success": false,
    "message": "Camera 0 already running"
}
```

**Detection Failed:**
```json
{
    "success": false,
    "error": "Detection processing failed: [error details]"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `204 No Content`: Success but no data to return
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error during processing

---

## Rate Limiting

**Current Limits:**
- No rate limiting implemented
- Recommended: 10 requests/second per endpoint

**Future Considerations:**
- Implement rate limiting for production use
- Add request queuing for high load
- Use caching for static responses

---

## CORS Configuration

**Current Setting:**
- CORS not enabled by default
- Access from same origin only

**Enable CORS (if needed):**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

---

## WebSocket Support

**Status:** Not implemented

**Alternative:** Use polling with `/video_feed` and `/get_camera_stats`

**Recommended Polling Intervals:**
- Video frames: 100ms (10 FPS display)
- Statistics: 1000ms (1 Hz)
- Logs: 1000ms (1 Hz)

---

## Authentication

**Current Status:** No authentication

**Production Recommendations:**
1. Implement API key authentication
2. Add JWT tokens for session management
3. Use HTTPS for encrypted communication
4. Add user roles and permissions

---

## Example Integration

### Python Client

```python
import requests
import time

class YOLOClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def start_camera(self, camera_id, confidence=0.25):
        response = requests.post(
            f"{self.base_url}/start_camera",
            json={"camera_id": camera_id, "confidence": confidence}
        )
        return response.json()
    
    def get_stats(self):
        response = requests.get(f"{self.base_url}/get_camera_stats")
        return response.json()
    
    def get_frame(self, camera_id):
        response = requests.get(
            f"{self.base_url}/video_feed",
            params={"camera": camera_id}
        )
        return response.content if response.status_code == 200 else None
    
    def detect_image(self, image_path, confidence=0.25):
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'confidence': confidence}
            response = requests.post(
                f"{self.base_url}/upload",
                files=files,
                data=data
            )
        return response.json()

# Usage
client = YOLOClient()
client.start_camera(0)
time.sleep(2)
stats = client.get_stats()
print(stats)
```

### JavaScript Client

```javascript
class YOLOClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
    }
    
    async startCamera(cameraId, confidence = 0.25) {
        const response = await fetch(`${this.baseUrl}/start_camera`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({camera_id: cameraId, confidence})
        });
        return await response.json();
    }
    
    async getStats() {
        const response = await fetch(`${this.baseUrl}/get_camera_stats`);
        return await response.json();
    }
    
    async detectImage(file, confidence = 0.25) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('confidence', confidence);
        
        const response = await fetch(`${this.baseUrl}/upload`, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    }
}

// Usage
const client = new YOLOClient();
await client.startCamera(0);
const stats = await client.getStats();
console.log(stats);
```

---

## Performance Considerations

**Optimal Request Patterns:**
- Batch camera starts instead of sequential
- Poll statistics at 1 Hz, not faster
- Request video frames only when visible
- Clear logs periodically to prevent memory growth

**Scaling:**
- Each camera adds ~20-30% CPU load
- Recommended max: 4 cameras on typical Mac
- Use lower resolution for more cameras
- Consider distributed deployment for >4 cameras

---

**API Version:** 1.0.0  
**Last Updated:** February 2026
