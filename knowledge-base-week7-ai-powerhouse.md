# WEEK 7: AI Powerhouse Complete Guide (2025-2026)
## LLM Fine-Tuning, Stable Diffusion, Voice AI, Computer Vision

**Topics**: Large Language Models, AI Image Generation, Text-to-Speech, Speech-to-Text, Object Detection  
**Goal**: Master AI tools for automation and monetization  
**Hardware**: Can run on Dell R730 with NVIDIA GRID K1 GPU

---

# PART 1: LLM FINE-TUNING & PROMPT ENGINEERING

## 🤖 Large Language Models (LLMs)

**Popular Models (2025-2026)**:
- **GPT-4** (OpenAI - Closed source, API only)
- **Claude 3.5 Sonnet** (Anthropic - Best reasoning)
- **Llama 3** (Meta - Open source, 8B-70B params)
- **Mistral 7B** (Open source, efficient)
- **Gemini 1.5 Pro** (Google - 1M token context)

### Running LLMs Locally

**LM Studio** (Already on VM100!):
- GUI for running local models
- Supports GGUF format (quantized)
- API compatible with OpenAI

**Ollama** (Alternative):
```bash
# Install
curl https://ollama.ai/install.sh | sh

# Run model
ollama run llama3
ollama run mistral
```

**Text Generation WebUI**:
- Most feature-rich
- Supports LoRA, fine-tuning
- GPU acceleration

## 🎯 Prompt Engineering (Critical Skill!)

### Basic Prompting
**Bad**: "Write about AI"  
**Good**: "Write a 500-word article explaining AI for beginners, using simple analogies"

### Advanced Techniques

**1. Zero-Shot Prompting**:
```
Classify sentiment: "I love this product!" 
Answer: Positive
```

**2. Few-Shot Prompting**:
```
Example 1: "Great product" → Positive
Example 2: "Terrible experience" → Negative
Example 3: "It's okay" → Neutral
Now classify: "Best purchase ever!" → ?
```

**3. Chain-of-Thought (CoT)**:
```
Problem: What's 15% of 80?
Let's think step by step:
1. 15% = 15/100 = 0.15
2. 0.15 × 80 = 12
Answer: 12
```

**4. Role Prompting**:
```
You are an expert Python developer with 10 years of experience.
Write a FastAPI server with async endpoints...
```

### Prompt Templates for Business

**Customer Service Bot**:
```
You are a helpful customer service agent for {company}.
Customer question: {question}
Provide a friendly, professional response.
If you don't know, say "Let me connect you with a specialist."
```

**Content Writer**:
```
Write a {word_count}-word {content_type} about {topic}.
Tone: {tone}
Target audience: {audience}
Include: {requirements}
```

## 🔧 LLM Fine-Tuning

### What is Fine-Tuning?
- Adapt pre-trained model to specific task
- Example: Train Llama 3 on your company's docs

### LoRA (Low-Rank Adaptation) - Efficient Method

**Advantages**:
- Train on consumer GPU (RTX 3060, 12GB)
- Small file size (10-100MB vs 7GB full model)
- Fast training (hours, not days)

**How to Fine-Tune**:
```python
# Using Hugging Face + PEFT
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model

# Load base model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8b")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8b")

# LoRA config
lora_config = LoraConfig(
    r=8,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05
)

# Apply LoRA
model = get_peft_model(model, lora_config)

# Train (simplified)
from transformers import Trainer
trainer = Trainer(model=model, train_dataset=dataset)
trainer.train()
```

### Use Cases for Fine-Tuning

**1. Customer Support Bot**:
- Train on your FAQs, product docs
- Faster than GPT-4, cheaper, offline

**2. Code Assistant**:
- Train on your codebase style
- Autocomplete, bug fixing

**3. Content Generator**:
- Train on your brand voice
- Blog posts, social media, emails

## 💡 LLM Monetization Ideas

1. **Custom ChatGPT for businesses** (\$500-\$5,000/client)
2. **Content generation service** (\$0.05-\$0.10/word)
3. **Customer support bot** (\$1,000-\$10,000/month per client)
4. **AI tutoring service** (\$20-\$50/hour)

---

# PART 2: STABLE DIFFUSION & AI IMAGE GENERATION

## 🎨 Stable Diffusion Basics

**What**: Open-source AI image generator (text-to-image)  
**Versions**: SD 1.5, SDXL (latest, best quality)  
**Hardware**: Requires GPU (NVIDIA GRID K1 works, slower)

### Installation Options

**1. Automatic1111 WebUI** (Most Popular):
```bash
# Install dependencies
sudo apt install python3-venv git

# Clone repo
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui

# Run
./webui.sh --xformers

# Access: http://localhost:7860
```

**2. ComfyUI** (Advanced, Node-Based):
- More control, complex workflows
- Steeper learning curve

**3. Fooocus** (Easiest):
- Midjourney-like interface
- Auto-optimizes prompts

### Prompting for Images

**Basic Prompt**:
```
a photorealistic portrait of a cat wearing a suit, 
professional photography, 8k, studio lighting
```

**Advanced Prompt Structure**:
```
[subject], [style], [quality tags], [negative prompt]

Example:
Portrait of cyberpunk warrior, digital art, artstation trending, 
highly detailed, 8k, ray tracing, unreal engine
Negative: ugly, deformed, low quality, blurry
```

**Quality Boosters**:
- "masterpiece", "best quality", "8k", "highly detailed"
- "artstation", "trending", "award winning"
- "professional", "studio lighting"

**Negative Prompts** (What to Avoid):
- "ugly", "deformed", "bad anatomy"
- "low quality", "blurry", "watermark"
- "text", "logo", "signature"

### ControlNet (Precise Control)

**What**: Guide generation with reference images

**Types**:
- **Canny**: Edge detection (outlines)
- **Depth**: 3D depth map
- **Pose**: Human pose skeleton
- **Scribble**: Rough sketches

**Use Case**: Create product images matching exact composition

### LoRA Models for SD

**What**: Add specific styles/characters

**Popular LoRAs**:
- Pixel Art style
- Anime style (Anything V5)
- Photorealistic people
- Specific characters

**Where to Find**: Civitai.com (largest repository)

## 💰 AI Image Monetization

1. **Sell on stock sites** (\$0.25-\$5/download)
   - Adobe Stock, Shutterstock, Getty Images (check TOS!)

2. **Custom art commissions** (\$20-\$200/image)
   - Fiverr, Upwork
   - "AI art artist" niche

3. **Print-on-demand** (Passive income)
   - Redbubble, Printful, Teespring
   - Upload designs, earn per sale

4. **NFT collections** (\$0.05-\$5 ETH per NFT)
   - Generate 10k collection
   - Mint on OpenSea

5. **Social media graphics** (\$50-\$500/month retainer)
   - Instagram posts, ads for businesses

---

# PART 3: VOICE AI & COMPUTER VISION

## 🎤 Text-to-Speech (TTS)

### ElevenLabs (Best Quality, Paid)
**Pricing**: \$1/month (10k chars), \$5/month (30k chars)

**Features**:
- Ultra-realistic voices
- Voice cloning (clone your voice!)
- 29 languages

**API Usage**:
```python
import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID"
headers = {"xi-api-key": "YOUR_API_KEY"}
data = {"text": "Hello, this is AI voice", "model_id": "eleven_monolingual_v1"}

response = requests.post(url, json=data, headers=headers)
with open("output.mp3", "wb") as f:
    f.write(response.content)
```

### Coqui TTS (Free, Open Source)
```python
from TTS.api import TTS

tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
tts.tts_to_file(text="Hello world", file_path="output.wav")
```

### Use Cases

1. **Audiobook narration** (\$100-\$500 per book)
2. **YouTube voiceovers** (automated content)
3. **IVR systems** (\$500-\$2,000/setup)
4. **Podcast generation** (automated news reading)

## 🎧 Speech-to-Text (STT)

### Whisper (OpenAI, Open Source, Best)

**Features**:
- 99 languages
- Extremely accurate
- Free (local) or API (\$0.006/minute)

**Local Usage**:
```python
import whisper

model = whisper.load_model("base")  # or "medium", "large"
result = model.transcribe("audio.mp3")
print(result["text"])
```

**API Usage** (faster):
```python
import openai

audio_file = open("speech.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript.text)
```

### Use Cases

1. **Meeting transcription** (\$20-\$50/hour)
2. **Podcast transcription** (SEO boost)
3. **Subtitles for videos** (\$5-\$15/video)
4. **Voice commands for bots**

## 👁️ Computer Vision (OpenCV, YOLO)

### OpenCV Basics

**Installation**:
```python
pip install opencv-python
```

**Face Detection**:
```python
import cv2

# Load cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load image
img = cv2.imread('photo.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# Draw rectangles
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow('Faces', img)
cv2.waitKey()
```

### YOLO (Object Detection)

**What**: Real-time object detection (80 classes)

**YOLOv8** (Latest, 2025):
```python
from ultralytics import YOLO

# Load model
model = YOLO('yolov8n.pt')  # nano (fastest)

# Detect
results = model('image.jpg')
results.show()

# Get detections
for box in results[0].boxes:
    print(f"Class: {box.cls}, Confidence: {box.conf}")
```

**Use Cases**:
1. **Security cameras** (person detection)
2. **Inventory counting** (automated)
3. **Quality control** (defect detection)
4. **Traffic analysis** (vehicle counting)

### Computer Vision Monetization

1. **Security camera AI** (\$1,000-\$10,000/install)
2. **Quality control for factories** (\$5,000-\$50,000/project)
3. **OCR services** (\$0.01-\$0.10/page)
4. **License plate recognition** (\$500-\$5,000/system)

## 🎓 Learning Resources

**LLMs**:
- Hugging Face Course (free)
- Fast.ai (practical deep learning)
- LangChain Docs (building with LLMs)

**Stable Diffusion**:
- Civitai.com (models, tutorials)
- r/StableDiffusion (community)
- Automatic1111 Wiki

**Voice AI**:
- ElevenLabs Docs
- Coqui TTS GitHub

**Computer Vision**:
- PyImageSearch (tutorials)
- OpenCV Docs
- Ultralytics YOLOv8 Docs

## 🐉 SHENRON'S WEEK 7 RECOMMENDATIONS

**For Beginners**:
1. Start with prompt engineering (free, immediate results)
2. Use cloud APIs (OpenAI, ElevenLabs) before local models
3. Learn Stable Diffusion basics (Automatic1111 WebUI)

**For Intermediate**:
1. Fine-tune Llama 3 with LoRA (your use case)
2. Create print-on-demand store (Stable Diffusion art)
3. Build voice bot (Whisper + ElevenLabs)

**For Advanced**:
1. Deploy LLM as SaaS (\$1,000-\$10,000/month MRR)
2. Sell AI services (Fiverr, Upwork: \$50-\$200/hour)
3. Build computer vision system for client (\$10k+ project)

**Week 7 turns you into an AI expert! 🐉🤖🎨**

---

**Category**: Week 7 - AI Powerhouse  
**Topics**: LLMs, Stable Diffusion, Voice AI, Computer Vision  
**Version**: 1.0 (2025-2026)  
**Status**: Complete mega-file

