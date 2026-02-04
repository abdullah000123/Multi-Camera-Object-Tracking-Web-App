# 📦 Installation Guide

Complete step-by-step installation instructions for the YOLOv8 Multi-Camera Object Detection System.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Automated Installation](#automated-installation)
3. [Manual Installation](#manual-installation)
4. [Verification](#verification)
5. [Common Issues](#common-issues)

---

## System Requirements

### Hardware Requirements
- **Processor**: Intel or Apple Silicon (M1/M2/M3)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space
- **Webcam**: Built-in or USB webcam(s)

### Software Requirements
- **Operating System**: macOS 10.14 (Mojave) or later
- **Homebrew**: Package manager for macOS
- **Python**: 3.11 or 3.12
- **Internet Connection**: Required for downloading dependencies

### Permissions Required
- **Camera Access**: For webcam detection
- **Network Access**: For downloading packages
- **File System Access**: For storing uploads and results

---

## Automated Installation

The easiest way to get started is using the provided `setup.sh` script.

### Step 1: Download Project Files

```bash
# Navigate to your desired directory
cd ~/Documents

# If you have the project as a zip file
unzip yolov8-detection-system.zip
cd yolov8-detection-system

# OR if cloning from repository
git clone <repository-url>
cd <project-directory>
```

### Step 2: Make Setup Script Executable

```bash
chmod +x setup.sh
```

### Step 3: Run Setup Script

```bash
./setup.sh
```

### What the Script Does

The `setup.sh` script performs the following actions automatically:

1. **Homebrew Check** (5-10 minutes if installing)
   - Checks if Homebrew is installed
   - Installs Homebrew if not present
   - Updates Homebrew to latest version

2. **Python Installation** (2-3 minutes if installing)
   - Checks for Python 3.11 or 3.12
   - Installs Python 3.11 via Homebrew if needed
   - Verifies Python version

3. **Virtual Environment** (30 seconds)
   - Creates isolated Python environment in `venv/` folder
   - Activates the virtual environment

4. **Package Installation** (5-10 minutes)
   - Updates pip, setuptools, and wheel
   - Installs PyTorch with MPS/CPU support
   - Installs Ultralytics (YOLOv8/YOLOv11)
   - Installs Flask 3.0.0
   - Installs all dependencies

5. **Application Launch**
   - Automatically starts the Flask server
   - Displays access URLs

### Expected Output

```
🚀 Starting setup...
✅ Using Python 3.11.x
📦 Creating virtual environment...
🔥 Installing PyTorch...
📚 Installing Ultralytics and Flask 3.0.0...
✅ Setup complete!
▶️ Starting app.py...
🌐 Open the IP address shown below in your browser

 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.xxx:5000
```

---

## Manual Installation

If you prefer manual control or the automated script fails, follow these steps:

### Step 1: Install Homebrew

If Homebrew is not installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen instructions. After installation, add Homebrew to PATH:

```bash
# For Apple Silicon Macs
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# For Intel Macs
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

### Step 2: Install Python 3.11

```bash
brew install python@3.11
```

Verify installation:

```bash
python3.11 --version
# Output: Python 3.11.x
```

### Step 3: Create Virtual Environment

Navigate to project directory:

```bash
cd /path/to/yolov8-detection-system
```

Create virtual environment:

```bash
python3.11 -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

Your terminal prompt should now show `(venv)`.

### Step 4: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

### Step 5: Install PyTorch

For macOS with MPS (Metal Performance Shaders) support:

```bash
pip install torch torchvision torchaudio
```

This will automatically detect your system and install the appropriate version.

### Step 6: Install Project Dependencies

```bash
pip install ultralytics
pip install flask==3.0.0
```

Additional dependencies will be installed automatically as requirements.

### Step 7: Verify Installation

Check installed packages:

```bash
pip list
```

You should see:
- torch (2.x.x)
- torchvision
- ultralytics (8.x.x)
- flask (3.0.0)
- opencv-python
- numpy
- pillow

### Step 8: Download YOLO Model (Optional)

The YOLO model will download automatically on first run, but you can pre-download:

```python
python3 -c "from ultralytics import YOLO; model = YOLO('yolo11s.pt')"
```

### Step 9: Run Application

```bash
python app.py
```

---

## Verification

### Test Image Detection Mode

1. Open browser: `http://localhost:5000`
2. Upload a test image
3. Click "Detect Objects"
4. Verify detection results appear

### Test Webcam Detection Mode

1. Navigate to: `http://localhost:5000/webcam`
2. Click "🚀 Start All Cameras"
3. Verify video feed appears
4. Check camera statistics update

### Check System Logs

In the terminal where you ran `python app.py`, you should see:

```
Loading YOLO models...
📦 [Camera 0] Loading dedicated YOLO model...
✅ [Camera 0] Model loaded
🚀 PARALLEL MULTI-CAMERA DETECTION SYSTEM
 * Running on http://0.0.0.0:5000
```

---

## Common Issues

### Issue: "Command not found: python3.11"

**Solution:**
```bash
# Check installed Python versions
ls -l /usr/local/bin/python* /opt/homebrew/bin/python*

# Use available version or install Python 3.11
brew install python@3.11
```

### Issue: "No module named 'cv2'"

**Solution:**
```bash
pip install opencv-python
```

### Issue: "Permission denied: setup.sh"

**Solution:**
```bash
chmod +x setup.sh
```

### Issue: PyTorch Installation Fails

**Solution:**
```bash
# Clear pip cache
pip cache purge

# Reinstall with --no-cache-dir
pip install --no-cache-dir torch torchvision torchaudio
```

### Issue: Port 5000 Already in Use

**Solution:**

Option 1: Kill process using port 5000
```bash
lsof -ti:5000 | xargs kill -9
```

Option 2: Change port in `app.py`
```python
# Last line of app.py
app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall Flask
pip install flask==3.0.0
```

### Issue: Camera Access Denied

**Solution:**
1. Open **System Preferences** > **Security & Privacy**
2. Click **Privacy** tab
3. Select **Camera** from left sidebar
4. Enable camera access for **Terminal** or your IDE
5. Restart terminal/IDE and rerun application

### Issue: Virtual Environment Won't Activate

**Solution:**
```bash
# Deactivate if already in a venv
deactivate

# Remove old venv
rm -rf venv

# Create fresh venv
python3.11 -m venv venv

# Activate
source venv/bin/activate
```

### Issue: Slow Installation on Apple Silicon

**Solution:**

If packages are building from source (very slow), ensure you're using the correct architecture:

```bash
# Check architecture
arch

# For Apple Silicon, ensure using ARM Python
which python3.11
# Should show: /opt/homebrew/bin/python3.11

# If showing x86_64 path, reinstall Python:
arch -arm64 brew install python@3.11
```

---

## Post-Installation

### Create Desktop Shortcut (Optional)

Create a file `start_yolo.command` with:

```bash
#!/bin/bash
cd /path/to/your/project
source venv/bin/activate
python app.py
```

Make it executable:
```bash
chmod +x start_yolo.command
```

Double-click to start the application.

### Create Alias (Optional)

Add to `~/.zshrc` or `~/.bash_profile`:

```bash
alias yolo-start='cd /path/to/project && source venv/bin/activate && python app.py'
```

Then simply run:
```bash
yolo-start
```

### Update Dependencies

To update all packages:

```bash
source venv/bin/activate
pip install --upgrade ultralytics flask torch torchvision opencv-python
```

---

## Uninstallation

To completely remove the application:

```bash
# Navigate to project directory
cd /path/to/yolov8-detection-system

# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove static files
rm -rf static/uploads static/results

# Remove YOLO models (optional)
rm -rf ~/.ultralytics

# Remove project directory
cd ..
rm -rf yolov8-detection-system
```

---

## Next Steps

After successful installation:

1. Read [README.md](README.md) for usage instructions
2. Check [USAGE.md](USAGE.md) for detailed feature guide
3. Review [API.md](API.md) for API endpoint documentation
4. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common problems

---

**Installation Support:**
- Check existing GitHub issues
- Review error messages carefully
- Ensure all prerequisites are met
- Try manual installation if automated fails

Last Updated: February 2026
