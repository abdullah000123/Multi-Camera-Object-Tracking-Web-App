# ⚡ Quick Start Guide

Get up and running with YOLOv8 Object Detection in 5 minutes.

## Prerequisites Check

✅ macOS 10.14+  
✅ Webcam connected  
✅ Terminal access  

## Installation (2 minutes)

```bash
# 1. Navigate to project
cd /path/to/yolov8-detection-system

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run automated setup
./setup.sh
```

The script will:
- Install Homebrew (if needed)
- Install Python 3.11/3.12
- Create virtual environment
- Install all dependencies
- Start the application

## Access the Application

Open browser: **http://localhost:5000**

---

## Image Detection (30 seconds)

1. **Upload**: Drag image onto upload area
2. **Adjust**: Set confidence threshold (default 0.25 is good)
3. **Detect**: Click "🔍 Detect Objects"
4. **View**: See results with bounding boxes

**Supported formats:** JPG, PNG, GIF, BMP

---

## Webcam Detection (2 minutes)

### Basic Setup

1. Click **"📹 Switch to Live Webcam Detection"**
2. Click **"🚀 Start All Cameras"**
3. Wait 5-10 seconds for initialization
4. View live detection feed

### Add Detection Zone (Optional)

1. Click **"✏️ Draw Zone"**
2. Click 3+ points on video to draw polygon
3. Press **Enter** to complete
4. Only objects in zone will be counted

### Monitor Activity

**Right panel shows:**
- Camera status and FPS
- Object counts in zone
- Entry/exit activity log

---

## Quick Commands

### Start Application
```bash
cd /path/to/project
source venv/bin/activate
python app.py
```

### Stop Application
- Press `Ctrl+C` in terminal

### Restart After Changes
```bash
# Stop with Ctrl+C, then:
python app.py
```

---

## Essential Controls

| Button | Action |
|--------|--------|
| 🚀 Start All Cameras | Begin detection on all cameras |
| 🛑 Stop All Cameras | Stop all processing |
| ✏️ Draw Zone | Create detection polygon |
| 🗑️ Clear Zone | Remove polygon |
| 🗑️ Clear Logs | Reset activity log |

### Drawing Hotkeys
- **Enter** - Complete polygon
- **Escape** - Cancel drawing

---

## Common Quick Fixes

### No video feed?
```bash
# Check camera permissions:
# System Preferences > Security & Privacy > Camera
# Enable for Terminal
```

### Port 5000 in use?
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in app.py line 629:
# app.run(... port=5001)
```

### Low FPS?
1. Stop some cameras (use fewer)
2. Lower confidence threshold
3. Close other apps

---

## First Time Tips

✅ **DO:**
- Start with 1 camera first
- Keep confidence at 0.25 initially
- Draw simple 4-point zones
- Monitor FPS in camera stats

❌ **DON'T:**
- Start 10 cameras at once
- Set confidence too low (<0.15)
- Draw complex polygons (>8 points)
- Ignore low FPS warnings

---

## URLs Quick Reference

| Page | URL |
|------|-----|
| Image Detection | http://localhost:5000/ |
| Webcam Detection | http://localhost:5000/webcam |
| API Stats | http://localhost:5000/get_camera_stats |
| API Cameras | http://localhost:5000/get_cameras |

---

## Performance Targets

### Excellent
- **FPS:** 25-30
- **Cameras:** 1-2
- **Latency:** <100ms

### Good
- **FPS:** 15-25
- **Cameras:** 2-3
- **Latency:** 100-200ms

### Acceptable
- **FPS:** 10-15
- **Cameras:** 3-4
- **Latency:** 200-300ms

If below these targets, see [USAGE.md](USAGE.md#performance-optimization) for optimization tips.

---

## Network Access (Optional)

Share with other devices on same WiFi:

```bash
# Find your IP
ipconfig getifaddr en0

# Access from phone/tablet:
# http://YOUR-IP-ADDRESS:5000
```

---

## Next Steps

📖 **Full Documentation:**
- [README.md](README.md) - Complete overview
- [INSTALLATION.md](INSTALLATION.md) - Detailed setup
- [USAGE.md](USAGE.md) - Feature guide
- [API.md](API.md) - API reference

🎯 **Try These:**
1. Upload different images to test detection
2. Draw zones and monitor activity
3. Run multiple cameras simultaneously
4. Adjust confidence and observe changes

---

## Emergency Reset

If something breaks:

```bash
# 1. Stop application (Ctrl+C)

# 2. Remove virtual environment
rm -rf venv

# 3. Re-run setup
./setup.sh
```

---

## Support

🐛 **Issues?**
- Check [USAGE.md](USAGE.md) troubleshooting
- Review terminal error messages
- Verify camera permissions

💡 **Questions?**
- Read full documentation
- Check API endpoints in [API.md](API.md)

---

**That's it! You're ready to detect objects. 🎉**

Start with image detection to test, then move to webcam for live monitoring.
