from flask import Flask, render_template, request, jsonify, send_from_directory, make_response, Response
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import time
import threading
from queue import Queue, Empty
from collections import deque

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
RESULTS_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Load YOLO models - one per camera for independent tracking
print("Loading YOLO models...")
camera_models = {}  # Store separate model instance per camera
model_lock = threading.Lock()

def get_model_for_camera(camera_id):
    """Get or create a YOLO model instance for a specific camera"""
    with model_lock:
        if camera_id not in camera_models:
            print(f"📦 [Camera {camera_id}] Loading dedicated YOLO model...")
            camera_models[camera_id] = YOLO('yolo11s.pt')
            print(f"✅ [Camera {camera_id}] Model loaded")
        return camera_models[camera_id]

# Global variables
camera_data = {}
camera_threads = {}
camera_locks = {}
camera_stop_events = {}  # Use threading.Event for clean shutdown
global_activity_logs = deque(maxlen=500)
TRACK_TIMEOUT = 3.0
TRACK_LOST_TIMEOUT = 1.0

# FPS reporting control
SHOW_FPS_IN_TERMINAL = False

def init_camera_data(camera_id):
    """Initialize data for a specific camera if not exists"""
    if camera_id not in camera_data:
        camera_data[camera_id] = {
            'polygon_points': [],
            'objects_in_zone': {},
            'activity_logs': [],
            'last_seen_tracks': {},
            'latest_frame': None,
            'is_running': False,
            'fps': 0,
            'total_detections': 0,
            'cap': None,
            'track_states': {}
        }
        camera_locks[camera_id] = threading.Lock()
        camera_stop_events[camera_id] = threading.Event()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def point_in_polygon(point, polygon):
    """Check if a point is inside a polygon using ray casting algorithm"""
    if len(polygon) < 3:
        return False
    
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def get_box_center(box):
    """Get center point of bounding box"""
    x1, y1, x2, y2 = box
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def process_camera_stream(camera_index, confidence=0.25):
    camera_id = str(camera_index)
    init_camera_data(camera_id)

    print(f"🎥 [Camera {camera_id}] Starting processing thread...")

    model = get_model_for_camera(camera_id)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"❌ [Camera {camera_id}] Failed to open")
        with camera_locks[camera_id]:
            camera_data[camera_id]['is_running'] = False
        return

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    with camera_locks[camera_id]:
        camera_data[camera_id]['cap'] = cap
        camera_data[camera_id]['is_running'] = True

    # Clear the stop event
    camera_stop_events[camera_id].clear()

    prev_time = time.time()

    print(f"✅ [Camera {camera_id}] Started successfully")

    while not camera_stop_events[camera_id].is_set():
        try:
            ret, frame = cap.read()
            if not ret:
                print(f"⚠️  [Camera {camera_id}] Failed to read frame")
                time.sleep(0.05)
                continue

            # FPS
            now = time.time()
            fps = 1 / (now - prev_time) if now != prev_time else 0
            prev_time = now

            # YOLO DETECTION (NO TRACKING)
            results = model(frame, conf=confidence, verbose=False)
            result = results[0]
            annotated_frame = result.plot()

            # Get polygon
            with camera_locks[camera_id]:
                polygon_points = camera_data[camera_id]['polygon_points'].copy()

            safe_points = [[int(p[0]), int(p[1])] for p in polygon_points] if len(polygon_points) >= 3 else []

            # Draw polygon
            if len(safe_points) >= 3:
                pts = np.array(safe_points, np.int32).reshape((-1, 1, 2))
                overlay = annotated_frame.copy()
                cv2.fillPoly(overlay, [pts], (0, 255, 0))
                cv2.addWeighted(overlay, 0.25, annotated_frame, 0.75, 0, annotated_frame)
                cv2.polylines(annotated_frame, [pts], True, (0, 255, 0), 2)

            # PURE DETECTION + POLYGON LOGIC
            class_counts_local = {}
            total_detections = 0

            if result.boxes is not None:
                total_detections = len(result.boxes)

                for box in result.boxes:
                    bbox = box.xyxy[0].tolist()
                    center = get_box_center(bbox)
                    class_name = result.names[int(box.cls[0])]

                    if len(safe_points) >= 3 and point_in_polygon(center, safe_points):
                        class_counts_local[class_name] = (
                            class_counts_local.get(class_name, 0) + 1
                        )

                        cv2.circle(
                            annotated_frame,
                            (int(center[0]), int(center[1])),
                            5,
                            (0, 255, 0),
                            -1
                        )

            # Store per-camera data (UI only)
            with camera_locks[camera_id]:
                camera_data[camera_id]['objects_in_zone'] = class_counts_local
                camera_data[camera_id]['fps'] = fps
                camera_data[camera_id]['total_detections'] = total_detections
                camera_data[camera_id]['latest_frame'] = annotated_frame.copy()

            # GLOBAL AGGREGATION - MAX LOGIC
            global_class_counts = {}

            for cam_id in camera_data.keys():
                with camera_locks[cam_id]:
                    if camera_data[cam_id]['is_running']:
                        cam_counts = camera_data[cam_id].get('objects_in_zone', {})
                        for cls, cnt in cam_counts.items():
                            global_class_counts[cls] = max(global_class_counts.get(cls, 0), cnt)

            update_global_class_state(global_class_counts)

            # Info overlay
            info = f"Cam {camera_id} | InZone: {sum(class_counts_local.values())} | Total: {total_detections}"
            cv2.putText(
                annotated_frame,
                info,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        except Exception as e:
            print(f"❌ [Camera {camera_id}] Error: {e}")
            time.sleep(0.05)

    # Clean shutdown
    cap.release()
    with camera_locks[camera_id]:
        camera_data[camera_id]['cap'] = None
        camera_data[camera_id]['is_running'] = False
        camera_data[camera_id]['latest_frame'] = None
        camera_data[camera_id]['objects_in_zone'] = {}  # Clear detections

    print(f"🛑 [Camera {camera_id}] Processing stopped cleanly")

@app.route('/')
def index():
    # Directly serve the webcam page as the landing page
    response = make_response(render_template('webcam_parallel.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/start_all_cameras', methods=['POST'])
def start_all_cameras():
    """Start all available cameras"""
    data = request.json
    confidence = float(data.get('confidence', 0.25))
    cameras = list_available_cameras(5)
    
    print(f"\n{'='*50}")
    print(f"🚀 Starting all cameras...")
    print(f"📋 Detected cameras: {cameras}")
    print(f"{'='*50}")
    
    started_cameras = []
    
    for cam_idx in cameras:
        camera_id = str(cam_idx)
        init_camera_data(camera_id)
        
        with camera_locks[camera_id]:
            if camera_data[camera_id]['is_running']:
                print(f"⏭️  [Camera {camera_id}] Already running, skipping")
                started_cameras.append(cam_idx)
                continue
        
        # Stop existing thread if any
        if camera_id in camera_threads and camera_threads[camera_id].is_alive():
            print(f"🔄 [Camera {camera_id}] Stopping existing thread...")
            camera_stop_events[camera_id].set()
            camera_threads[camera_id].join(timeout=2.0)
        
        print(f"▶️  [Camera {camera_id}] Starting new thread...")
        thread = threading.Thread(target=process_camera_stream, args=(cam_idx, confidence), daemon=True)
        camera_threads[camera_id] = thread
        thread.start()
        started_cameras.append(cam_idx)
        time.sleep(0.5)
    
    print(f"✅ Started {len(started_cameras)} camera(s): {started_cameras}")
    print(f"{'='*50}\n")
    
    return jsonify({'success': True, 'cameras_started': started_cameras})

@app.route('/stop_all_cameras', methods=['POST'])
def stop_all_cameras():
    """Stop all running cameras"""
    print(f"\n🛑 Stopping all cameras...")
    
    for camera_id in list(camera_data.keys()):
        camera_stop_events[camera_id].set()
        
        # Wait for thread to finish
        if camera_id in camera_threads and camera_threads[camera_id].is_alive():
            camera_threads[camera_id].join(timeout=2.0)
    
    print("✅ All cameras stopped\n")
    
    return jsonify({'success': True})

@app.route('/start_camera', methods=['POST'])
def start_camera():
    """Start a specific camera"""
    data = request.json
    camera_index = int(data.get('camera_id', 0))
    camera_id = str(camera_index)
    confidence = float(data.get('confidence', 0.25))
    
    print(f"\n{'='*50}")
    print(f"🎥 Start camera request for Camera {camera_id}")
    
    init_camera_data(camera_id)
    
    with camera_locks[camera_id]:
        if camera_data[camera_id]['is_running']:
            print(f"⚠️  [Camera {camera_id}] Already running!")
            print(f"{'='*50}\n")
            return jsonify({'success': False, 'message': 'Camera already running'})
    
    # Stop existing thread if any
    if camera_id in camera_threads and camera_threads[camera_id].is_alive():
        print(f"🔄 [Camera {camera_id}] Stopping existing thread...")
        camera_stop_events[camera_id].set()
        camera_threads[camera_id].join(timeout=2.0)
        print(f"✅ [Camera {camera_id}] Existing thread stopped")
    
    print(f"▶️  [Camera {camera_id}] Creating new thread...")
    thread = threading.Thread(target=process_camera_stream, args=(camera_index, confidence), daemon=True)
    camera_threads[camera_id] = thread
    thread.start()
    
    # Wait a moment and verify it started
    time.sleep(0.5)
    
    with camera_locks[camera_id]:
        is_running = camera_data[camera_id]['is_running']
    
    if is_running:
        print(f"✅ [Camera {camera_id}] Started successfully")
    else:
        print(f"❌ [Camera {camera_id}] Failed to start - check if camera exists")
    
    print(f"{'='*50}\n")
    
    return jsonify({'success': True, 'camera_id': camera_id, 'is_running': is_running})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    """Stop a specific camera completely"""
    data = request.json
    camera_id = str(data.get('camera_id', '0'))
    
    if camera_id in camera_data:
        # Signal thread to stop
        camera_stop_events[camera_id].set()
        
        # Wait for thread to finish
        if camera_id in camera_threads and camera_threads[camera_id].is_alive():
            camera_threads[camera_id].join(timeout=2.0)
        
        print(f"🛑 Stopped Camera {camera_id}")
        return jsonify({'success': True, 'camera_id': camera_id})
    
    return jsonify({'success': False, 'message': 'Camera not found'})

@app.route('/pause_camera', methods=['POST'])
def pause_camera():
    """Pause a specific camera (stops thread, keeps data)"""
    data = request.json
    camera_id = str(data.get('camera_id', '0'))
    
    if camera_id in camera_data:
        # Signal thread to stop
        camera_stop_events[camera_id].set()
        
        # Wait for thread to finish
        if camera_id in camera_threads and camera_threads[camera_id].is_alive():
            camera_threads[camera_id].join(timeout=2.0)
        
        print(f"⏸️  Paused Camera {camera_id}")
        return jsonify({'success': True, 'camera_id': camera_id})
    
    return jsonify({'success': False, 'message': 'Camera not found'})

@app.route('/set_polygon', methods=['POST'])
def set_polygon():
    data = request.json
    camera_id = str(data.get('camera_id', '0'))
    
    init_camera_data(camera_id)
    
    with camera_locks[camera_id]:
        camera_data[camera_id]['polygon_points'] = [
            [int(p["x"]), int(p["y"])]
            for p in data.get("points", [])
        ]
    
    print(f"✓ [Camera {camera_id}] Polygon set: {len(camera_data[camera_id]['polygon_points'])} points")
    
    return jsonify({'success': True, 'camera_id': camera_id})

@app.route('/get_polygon', methods=['GET'])
def get_polygon():
    camera_id = str(request.args.get('camera_id', '0'))
    init_camera_data(camera_id)
    
    with camera_locks[camera_id]:
        polygon_points = camera_data[camera_id]['polygon_points'].copy()
    
    return jsonify({'camera_id': camera_id, 'points': polygon_points})

@app.route('/clear_polygon', methods=['POST'])
def clear_polygon():
    data = request.json
    camera_id = str(data.get('camera_id', '0'))
    
    init_camera_data(camera_id)
    
    with camera_locks[camera_id]:
        camera_data[camera_id]['polygon_points'] = []
        camera_data[camera_id]['objects_in_zone'] = {}
        camera_data[camera_id]['activity_logs'] = []
        camera_data[camera_id]['last_seen_tracks'] = {}
        camera_data[camera_id]['track_states'] = {}
    
    print(f"✗ [Camera {camera_id}] Polygon cleared")
    
    return jsonify({'success': True, 'camera_id': camera_id})

@app.route('/get_logs', methods=['GET'])
def get_logs():
    """Get unified activity logs from all cameras"""
    logs = list(global_activity_logs)
    return jsonify({'logs': logs})

@app.route('/get_camera_stats', methods=['GET'])
def get_camera_stats():
    """Get stats for all running cameras"""
    stats = {}
    
    for camera_id in camera_data.keys():
        with camera_locks[camera_id]:
            stats[camera_id] = {
                'is_running': camera_data[camera_id]['is_running'],
                'in_zone': sum(camera_data[camera_id]['objects_in_zone'].values()),
                'total_detections': camera_data[camera_id]['total_detections'],
                'fps': camera_data[camera_id]['fps'],
                'active_tracks': len(camera_data[camera_id].get('track_states', {}))
            }
    
    return jsonify({'stats': stats})

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    global global_activity_logs
    global_activity_logs.clear()
    
    for camera_id in camera_data.keys():
        with camera_locks[camera_id]:
            camera_data[camera_id]['activity_logs'] = []
    
    print("🗑️  All logs cleared")
    
    return jsonify({'success': True})

@app.route('/video_feed')
def video_feed():
    """Video streaming route - returns latest frame from requested camera - IMPROVED VERSION"""
    camera_index = int(request.args.get('camera', 0))
    camera_id = str(camera_index)
    
    print(f"📹 Video feed requested for Camera {camera_id}")
    
    def generate():
        """Generate frames from camera's latest_frame buffer"""
        last_frame_time = 0
        frame_interval = 0.033  # ~30 fps
        no_frame_count = 0
        max_no_frame_retries = 100  # ~3 seconds at 30fps
        
        while True:
            try:
                current_time = time.time()
                
                if camera_id not in camera_data:
                    print(f"⚠️  Camera {camera_id} not initialized")
                    time.sleep(0.1)
                    no_frame_count += 1
                    if no_frame_count > max_no_frame_retries:
                        print(f"❌ Camera {camera_id} timeout - not initialized")
                        break
                    continue
                
                with camera_locks[camera_id]:
                    is_running = camera_data[camera_id]['is_running']
                    frame = camera_data[camera_id]['latest_frame']
                
                if not is_running:
                    print(f"⚠️  Camera {camera_id} not running, stopping feed")
                    break
                
                if frame is None:
                    # Camera is running but no frame yet - wait a bit
                    no_frame_count += 1
                    if no_frame_count > max_no_frame_retries:
                        print(f"❌ Camera {camera_id} timeout - no frames after {max_no_frame_retries} attempts")
                        break
                    time.sleep(0.033)  # Wait for next frame
                    continue
                
                # Reset counter when we get a frame
                no_frame_count = 0
                
                if current_time - last_frame_time >= frame_interval:
                    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    if ret:
                        yield (
                            b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' +
                            buffer.tobytes() +
                            b'\r\n'
                        )
                        last_frame_time = current_time
                
                time.sleep(0.01)
            
            except GeneratorExit:
                print(f"🛑 Video feed closed for Camera {camera_id}")
                break
            except Exception as e:
                print(f"❌ Stream error for camera {camera_id}: {e}")
                time.sleep(0.1)
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

import sys

def list_available_cameras(max_failures=5):
    """
    Detect connected cameras dynamically.
    Works on Linux, macOS, Windows.
    Returns list of indices that return a real frame.
    """
    available = []
    index = 0
    failures = 0

    if sys.platform.startswith('darwin'):
        backend = cv2.CAP_AVFOUNDATION  # macOS
    elif sys.platform.startswith('win'):
        backend = cv2.CAP_DSHOW       # Windows
    else:
        backend = cv2.CAP_V4L2        # Linux

    while failures < max_failures:
        cap = cv2.VideoCapture(index, backend)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                available.append(index)
                failures = 0
            else:
                failures += 1
        else:
            failures += 1
        index += 1

    return available


@app.route('/get_cameras')
def get_cameras():
    cams = list_available_cameras(5)
    print("🎥 Available cameras right now:", cams)
    return jsonify(cams)

@app.route('/get_system_status')
def get_system_status():
    """Get detailed system status for debugging"""
    status = {
        'available_cameras': list_available_cameras(5),
        'initialized_cameras': list(camera_data.keys()),
        'camera_details': {}
    }
    
    for camera_id in camera_data.keys():
        with camera_locks[camera_id]:
            status['camera_details'][camera_id] = {
                'is_running': camera_data[camera_id]['is_running'],
                'has_frame': camera_data[camera_id]['latest_frame'] is not None,
                'has_cap': camera_data[camera_id]['cap'] is not None,
                'thread_alive': camera_id in camera_threads and camera_threads[camera_id].is_alive(),
                'polygon_points': len(camera_data[camera_id]['polygon_points']),
                'objects_in_zone': camera_data[camera_id]['objects_in_zone'],
                'fps': camera_data[camera_id]['fps']
            }
    
    print("🔍 System Status:", json.dumps(status, indent=2))
    return jsonify(status)

@app.route('/debug_camera/<camera_id>')
def debug_camera(camera_id):
    """Debug endpoint to check camera state"""
    if camera_id not in camera_data:
        return jsonify({'error': 'Camera not initialized'})
    
    with camera_locks[camera_id]:
        return jsonify({
            'camera_id': camera_id,
            'is_running': camera_data[camera_id]['is_running'],
            'has_frame': camera_data[camera_id]['latest_frame'] is not None,
            'has_cap': camera_data[camera_id]['cap'] is not None,
            'fps': camera_data[camera_id]['fps'],
            'thread_alive': camera_id in camera_threads and camera_threads[camera_id].is_alive(),
            'stop_event_set': camera_stop_events[camera_id].is_set() if camera_id in camera_stop_events else None
        })

# ===== GLOBAL CLASS-LEVEL STATE =====
class_global_state = {}
CLASS_EXIT_TIMEOUT = 1.0  # seconds

def update_global_class_state(class_counts):
    """
    class_counts: dict {class_name: MAX_count_across_all_cameras}
    """
    now = time.time()

    # ENTER / UPDATE
    for cls, count in class_counts.items():
        if cls not in class_global_state:
            class_global_state[cls] = {
                "inside": False,
                "max_count": 0,
                "last_seen": now
            }

        state = class_global_state[cls]

        if not state["inside"]:
            print(f"🟢 [GLOBAL] {cls} ENTERED | Max count: {count}")
            global_activity_logs.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "camera_id": "GLOBAL",
                "object": cls,
                "action": "ENTERED",
                "max_count": count
            })
            state["inside"] = True
            state["max_count"] = count
        else:
            # Update max count if we see more
            if count > state["max_count"]:
                old_max = state["max_count"]
                state["max_count"] = count
                print(f"📈 [GLOBAL] {cls} count increased: {old_max} → {count}")

        state["last_seen"] = now

    # EXIT
    for cls, state in list(class_global_state.items()):
        if cls not in class_counts:
            if state["inside"] and (now - state["last_seen"]) > CLASS_EXIT_TIMEOUT:
                print(f"🔴 [GLOBAL] {cls} EXITED | Max seen: {state['max_count']}")
                global_activity_logs.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "camera_id": "GLOBAL",
                    "object": cls,
                    "action": "EXITED",
                    "max_count": state["max_count"]
                })
                state["inside"] = False
                state["max_count"] = 0


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 PARALLEL MULTI-CAMERA DETECTION SYSTEM")
    print("=" * 60)
    print("✨ Independent tracking per camera")
    print("📦 Dedicated YOLO model per camera")
    print("🎯 No cross-camera interference")
    print("💡 Stable tracking IDs")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)