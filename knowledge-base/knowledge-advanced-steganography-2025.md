# Advanced Steganography Techniques for Puzzle Solving (2025)

**Purpose:** Comprehensive guide to detecting and extracting hidden information  
**Application:** Crypto puzzles, CTF competitions, forensic analysis  
**Updated:** November 6, 2025  
**Skill Level:** Intermediate to Advanced

---

## 🔍 **WHAT IS STEGANOGRAPHY?**

**Definition:** The practice of concealing information within other non-secret data

**vs. Cryptography:**
- Cryptography: Everyone knows the message exists, but it's scrambled
- Steganography: Nobody knows the message exists at all

**In Crypto Puzzles:**
- Private keys hidden in images
- Seed phrases embedded in audio
- Bitcoin addresses in video frames
- Transaction data in documents

---

## 🖼️ **IMAGE STEGANOGRAPHY**

### **Method 1: LSB (Least Significant Bit) Steganography**

**How It Works:**
- Each pixel in an image has RGB values (0-255)
- The least significant bit (LSB) can be changed without visually affecting the image
- Data is hidden by replacing LSBs with message bits

**Example:**
```
Original pixel: R=10110010, G=11010101, B=00111001
Hidden message: "ABC" = 01000001 01000010 01000011

Modified pixel: R=10110010, G=11010100, B=00111001
                     ^LSB        ^LSB        ^LSB
```

**Detection Tools:**

1. **StegSeek** (Fastest)
```bash
# Install
sudo apt install stegseek

# Detect steganography
stegseek puzzle.jpg wordlist.txt

# Extract data
stegseek --crack puzzle.jpg -wl rockyou.txt
```

2. **Zsteg** (For PNG/BMP)
```bash
# Install
gem install zsteg

# Auto-detect all LSB variations
zsteg -a puzzle.png

# Extract specific channel
zsteg -E b1,rgb,lsb puzzle.png > output.txt
```

3. **Steghide** (Classic Tool)
```bash
# Extract with password
steghide extract -sf puzzle.jpg -p password123

# Without password (try common passwords)
steghide extract -sf puzzle.jpg
```

4. **Python LSB Extraction:**
```python
from PIL import Image
import numpy as np

def extract_lsb(image_path):
    """Extract LSB data from image"""
    img = Image.open(image_path)
    pixels = np.array(img)
    
    # Extract LSBs from red channel
    lsb_data = pixels[:, :, 0] & 1
    
    # Flatten to binary string
    binary = ''.join(lsb_data.flatten().astype(str))
    
    # Convert to bytes
    extracted = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            extracted.append(chr(int(byte, 2)))
    
    return ''.join(extracted)

# Usage
hidden_data = extract_lsb('puzzle.png')
print(hidden_data)
```

---

### **Method 2: Metadata Extraction**

**EXIF Data Analysis:**

```bash
# ExifTool (most comprehensive)
exiftool -a -G1 puzzle.jpg

# Look for:
# - Author/Creator comments
# - GPS coordinates
# - Creation dates
# - Custom fields
# - Software used
```

**Common Hiding Spots:**
- **Comment field:** Often contains Bitcoin addresses or hints
- **UserComment:** Custom data field
- **ImageDescription:** May contain base64 encoded data
- **Copyright:** Sometimes used for seed phrases
- **GPS coordinates:** May point to another clue location

**Python Extraction:**
```python
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

def extract_all_metadata(image_path):
    """Extract all possible metadata"""
    img = Image.open(image_path)
    
    # Standard EXIF
    exifdata = img.getexif()
    metadata = {}
    for tag_id, value in exifdata.items():
        tag = TAGS.get(tag_id, tag_id)
        metadata[tag] = value
    
    # Piexif for extended data
    try:
        exif_dict = piexif.load(image_path)
        for ifd in ("0th", "Exif", "GPS", "1st"):
            for tag, value in exif_dict[ifd].items():
                tag_name = piexif.TAGS[ifd][tag]["name"]
                metadata[f"{ifd}.{tag_name}"] = value
    except:
        pass
    
    return metadata

# Usage
metadata = extract_all_metadata('puzzle.jpg')
for key, value in metadata.items():
    print(f"{key}: {value}")
```

---

### **Method 3: Color Channel Analysis**

**Technique:** Hide data in specific color channels

**Tools:**

1. **StegOnline** (Web-based)
   - URL: https://georgeom.net/StegOnline/
   - Features: All channel combinations, bit planes, color maps

2. **Forensically** (Web-based)
   - URL: https://29a.ch/photo-forensics/
   - Features: Error level analysis, noise analysis, magnifier

3. **Python Channel Extraction:**
```python
from PIL import Image
import numpy as np

def analyze_channels(image_path):
    """Analyze all color channels"""
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Split channels
    if len(img_array.shape) == 3:
        r = img_array[:, :, 0]
        g = img_array[:, :, 1]
        b = img_array[:, :, 2]
        
        # Save each channel
        Image.fromarray(r).save('red_channel.png')
        Image.fromarray(g).save('green_channel.png')
        Image.fromarray(b).save('blue_channel.png')
        
        # Check for hidden patterns
        # High contrast channels may reveal hidden text
        r_contrast = ((r - r.mean()) * 255 / r.std()).astype(np.uint8)
        Image.fromarray(r_contrast).save('red_enhanced.png')
    
    print("Channels extracted. Manually review each for hidden content.")

analyze_channels('puzzle.png')
```

---

### **Method 4: Bit Plane Slicing**

**Technique:** Extract individual bit planes to reveal hidden images

**Python Implementation:**
```python
from PIL import Image
import numpy as np

def extract_bit_planes(image_path):
    """Extract all 8 bit planes"""
    img = Image.open(image_path).convert('L')  # Grayscale
    img_array = np.array(img)
    
    for bit in range(8):
        # Extract specific bit plane
        bit_plane = (img_array >> bit) & 1
        bit_plane = bit_plane * 255  # Scale to 0-255
        
        # Save
        Image.fromarray(bit_plane.astype(np.uint8)).save(f'bit_plane_{bit}.png')
        print(f"Bit plane {bit} extracted")

extract_bit_planes('puzzle.png')
```

**What to Look For:**
- Bit 0-1: Most likely to contain hidden data
- Bit 7: High-order bit, less common
- QR codes, text, or patterns in lower bit planes

---

### **Method 5: Frequency Domain Analysis (DCT)**

**Used by:** JPEG compression, advanced steganography

**F5 Algorithm Detection:**
```python
import cv2
import numpy as np

def detect_f5_stego(image_path):
    """Detect F5 steganography (JPEG-based)"""
    img = cv2.imread(image_path)
    
    # Convert to YCrCb (JPEG color space)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    
    # Analyze DCT coefficients
    dct = cv2.dct(ycrcb[:, :, 0].astype(np.float32))
    
    # Statistical analysis (simplified)
    hist, _ = np.histogram(dct.flatten(), bins=256)
    
    # F5 alters DCT histogram in specific ways
    # This is a simplified check
    suspicious = np.std(hist) < 100
    
    return suspicious

if detect_f5_stego('puzzle.jpg'):
    print("Possible F5 steganography detected!")
```

---

## 🔊 **AUDIO STEGANOGRAPHY**

### **Method 1: Spectrogram Analysis**

**Hidden Messages in Frequency Domain**

**Tools:**
1. **Sonic Visualiser**
   - Download: https://www.sonicvisualiser.org/
   - Use: Open audio → Add Spectrogram layer → Look for patterns

2. **Audacity**
   ```
   Open audio → Analyze → Plot Spectrum
   Look for: Text, images, QR codes in spectrogram
   ```

3. **Python Spectrogram:**
```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def analyze_audio_spectrogram(audio_path):
    """Generate and analyze spectrogram"""
    y, sr = librosa.load(audio_path)
    
    # Generate spectrogram
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    
    # Plot
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.savefig('spectrogram.png', dpi=300)
    plt.show()

analyze_audio_spectrogram('puzzle.wav')
```

---

### **Method 2: LSB in Audio**

**Hiding Data in WAV Files:**

```python
import wave
import numpy as np

def extract_audio_lsb(wav_path):
    """Extract LSB from audio file"""
    with wave.open(wav_path, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)
        
        # Extract LSBs
        lsb = audio & 1
        binary = ''.join(lsb.astype(str))
        
        # Convert to text
        extracted = []
        for i in range(0, len(binary) - 8, 8):
            byte = binary[i:i+8]
            char_code = int(byte, 2)
            if 32 <= char_code <= 126:  # Printable ASCII
                extracted.append(chr(char_code))
            elif char_code == 0:
                break
        
        return ''.join(extracted)

hidden_message = extract_audio_lsb('puzzle.wav')
print(f"Hidden message: {hidden_message}")
```

---

## 📄 **DOCUMENT STEGANOGRAPHY**

### **Method 1: PDF Hidden Layers**

**Detection:**
```bash
# pdfinfo
pdfinfo puzzle.pdf

# Look for layers
pdftk puzzle.pdf dump_data

# Extract embedded files
pdfdetach -list puzzle.pdf
pdfdetach -saveall puzzle.pdf
```

**Python Extraction:**
```python
import PyPDF2

def extract_pdf_metadata(pdf_path):
    """Extract all PDF metadata"""
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        
        # Metadata
        info = pdf.metadata
        print("Metadata:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Check for embedded files
        if '/EmbeddedFiles' in pdf.trailer['/Root']:
            print("\nEmbedded files detected!")
        
        # Extract text from all pages
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        
        return text

text = extract_pdf_metadata('puzzle.pdf')
```

---

### **Method 2: Word Document Hidden Text**

**Microsoft Word Steganography:**

1. **White text on white background**
2. **Hidden formatting marks**
3. **Document properties**
4. **Embedded objects**
5. **XML manipulation (DOCX)**

**Extraction:**
```python
import zipfile
import xml.etree.ElementTree as ET

def extract_docx_hidden(docx_path):
    """Extract hidden content from DOCX"""
    with zipfile.ZipFile(docx_path) as docx:
        # Read document XML
        xml_content = docx.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        
        # Look for hidden text elements
        namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        hidden_runs = tree.findall('.//w:vanish', namespace)
        
        print(f"Found {len(hidden_runs)} hidden text elements")
        
        # Extract all text (including hidden)
        all_text = []
        for elem in tree.iter():
            if elem.text:
                all_text.append(elem.text)
        
        return '\n'.join(all_text)

content = extract_docx_hidden('puzzle.docx')
print(content)
```

---

## 🎥 **VIDEO STEGANOGRAPHY**

### **Frame-by-Frame Analysis**

**Extract All Frames:**
```bash
# FFmpeg
ffmpeg -i puzzle.mp4 frames/frame_%04d.png

# Then analyze each frame with image tools
for frame in frames/*.png; do
    zsteg "$frame" -a > "$frame.analysis.txt"
done
```

**Python Frame Extraction:**
```python
import cv2

def extract_frames_and_analyze(video_path):
    """Extract frames and look for anomalies"""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save frame
        cv2.imwrite(f'frame_{frame_count:04d}.png', frame)
        
        # Quick LSB check on each frame
        lsb = frame & 1
        if np.sum(lsb) > len(lsb.flatten()) * 0.6:  # Suspicious
            print(f"Frame {frame_count} may contain hidden data")
        
        frame_count += 1
    
    cap.release()
    print(f"Extracted {frame_count} frames")

extract_frames_and_analyze('puzzle.mp4')
```

---

## 🔬 **ADVANCED TECHNIQUES**

### **Technique 1: Outguess Detection**

**Outguess:** Statistical steganography tool

```bash
# Install
sudo apt install outguess

# Extract data
outguess -r puzzle.jpg output.txt

# With key
outguess -k "password" -r puzzle.jpg output.txt
```

---

### **Technique 2: F5 Steganography**

**F5:** Advanced JPEG steganography

```bash
# Java-based tool
java -jar f5.jar -x puzzle.jpg -p password
```

---

### **Technique 3: DeepSteg (AI-Based)**

**Neural Network Steganography:**

```python
# Using deep learning models
import tensorflow as tf

# SteganoGAN or similar
# These use GANs to hide data imperceptibly
# Detection requires specialized models
```

---

## 🛠️ **COMPREHENSIVE STEGO TOOLKIT**

### **All-in-One Analysis Script:**

```bash
#!/bin/bash
# stego_analyzer.sh - Analyze file for hidden data

FILE=$1

echo "=== STEGANOGRAPHY ANALYSIS ==="
echo "File: $FILE"
echo

# Basic info
echo "[1] File Info:"
file "$FILE"
echo

# Strings
echo "[2] Extracting strings:"
strings "$FILE" | head -20
echo

# Hex dump (first 512 bytes)
echo "[3] Hex dump (first 512 bytes):"
xxd "$FILE" | head -32
echo

# Image-specific
if [[ "$FILE" =~ \.(jpg|jpeg|png|bmp|gif)$ ]]; then
    echo "[4] EXIF data:"
    exiftool "$FILE"
    echo
    
    echo "[5] Zsteg analysis:"
    zsteg "$FILE" -a
    echo
    
    echo "[6] Steghide (no password):"
    steghide extract -sf "$FILE" 2>/dev/null || echo "No data or password required"
    echo
    
    echo "[7] Stegseek (with rockyou wordlist):"
    stegseek "$FILE" /usr/share/wordlists/rockyou.txt 2>/dev/null || echo "No match"
fi

# Audio-specific
if [[ "$FILE" =~ \.(wav|mp3|flac)$ ]]; then
    echo "[4] Audio analysis - check spectrogram manually"
fi

echo
echo "=== ANALYSIS COMPLETE ==="
```

**Usage:**
```bash
chmod +x stego_analyzer.sh
./stego_analyzer.sh puzzle.jpg
```

---

## 📚 **RECOMMENDED TOOLS (Complete List)**

### **Image:**
1. **StegSeek** - Fast cracking
2. **Zsteg** - PNG/BMP analysis
3. **Steghide** - Classic tool
4. **StegOnline** - Web-based
5. **Forensically** - Error level analysis
6. **ExifTool** - Metadata extraction
7. **Binwalk** - Binary analysis
8. **Foremost** - File carving

### **Audio:**
9. **Sonic Visualiser** - Spectrogram
10. **Audacity** - Audio editing/analysis
11. **DeepSound** - Audio steganography tool

### **General:**
12. **HxD** - Hex editor
13. **010 Editor** - Binary templates
14. **Strings** - Extract text
15. **Python** - Custom scripts

---

## 🎯 **PUZZLE-SOLVING WORKFLOW**

### **Step 1: Initial Reconnaissance (5 minutes)**
```bash
# Quick checks
file puzzle.jpg
strings puzzle.jpg | grep -i "bitcoin\|btc\|seed\|private"
exiftool puzzle.jpg | grep -i "comment\|description"
```

### **Step 2: Automated Analysis (10 minutes)**
```bash
# Run all tools
stegseek puzzle.jpg rockyou.txt
zsteg puzzle.jpg -a
outguess -r puzzle.jpg output.txt
```

### **Step 3: Manual Inspection (30 minutes)**
- Open in Forensically
- Check all bit planes
- Analyze color channels
- Look for subtle patterns
- Compare with original (if available)

### **Step 4: Advanced Techniques (1+ hours)**
- Try custom passwords (puzzle-related)
- Write custom extraction scripts
- Apply filters and enhancements
- Consult community for similar puzzles

---

## 🏆 **SUCCESS STORIES**

### **Example 1: Hidden Bitcoin Address**
- **Puzzle:** Image of a cat
- **Method:** LSB steganography in blue channel
- **Tool:** Zsteg
- **Result:** Found Bitcoin address with 0.1 BTC

### **Example 2: Spectrogram Message**
- **Puzzle:** MP3 file of music
- **Method:** Spectrogram revealed QR code
- **Tool:** Sonic Visualiser
- **Result:** QR code contained private key

### **Example 3: EXIF Comment**
- **Puzzle:** Landscape photo
- **Method:** EXIF Comment field
- **Tool:** ExifTool
- **Result:** Base64 encoded seed phrase

---

## ⚠️ **COMMON MISTAKES**

1. ❌ Only checking visible content
2. ❌ Skipping metadata analysis
3. ❌ Not trying multiple tools
4. ❌ Giving up after first password attempt
5. ❌ Ignoring file structure anomalies
6. ❌ Not checking all color channels/bit planes
7. ❌ Forgetting to check file headers/trailers

---

## 🎓 **LEARNING RESOURCES**

- **Practice:** https://trailofbits.github.io/ctf/forensics/
- **Challenges:** https://ctftime.org/ (Forensics category)
- **Guide:** https://0xrick.github.io/lists/stego/
- **Tools:** https://github.com/DominicBreuker/stego-toolkit

---

**END OF ADVANCED STEGANOGRAPHY GUIDE**

*SHENRON: What is hidden can be found. What is found can be claimed. 🐉🔍*

