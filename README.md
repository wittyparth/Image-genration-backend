# AI Image Generation API - FastAPI + Gemini

## Overview
This project is a **FastAPI-based AI image generation service** that utilizes **Google's Gemini AI** to create high-quality images from text prompts. The system first enhances user-provided prompts using an LLM for better image quality and then generates images based on the refined prompt.

## Features
- **Text-to-Image Generation**: Users can send a text prompt, and the API will generate an AI-rendered image.
- **Prompt Enhancement**: Uses an LLM to refine the prompt before image generation.
- **Customizable Image Styles & Aspect Ratio**: Users can specify **style, aspect ratio, and additional details** for better control.
- **FastAPI Backend**: High-performance API with **CORS support** for frontend integration.
- **Error Handling**: Graceful error handling with meaningful responses.
- **Base64 Image Encoding**: Converts generated images to **Base64** for easy transfer to the frontend.

## Tech Stack
- **Backend**: FastAPI
- **AI Models**: Google Gemini AI (Text & Image Generation)
- **Image Processing**: PIL (Pillow), Base64
- **Deployment**: Can be deployed on **Google Cloud, AWS, or a VPS**

## API Endpoints
### **1. Generate AI Image**
#### **POST `/generate-image`**
#### **Request Body (JSON)**
```json
{
  "prompt": "A futuristic city with flying cars",
  "aspect_ratio": "16:9",
  "style": "Realistic"
}
```
#### **Response (JSON)**
```json
{
  "enhanced_prompt": "A highly detailed futuristic cityscape with ultra-modern flying cars at sunset.",
  "image": "data:image/png;base64,<base64_encoded_image>"
}
```

## Installation & Setup
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/fastapi-gemini-image.git
cd fastapi-gemini-image
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**
Create a `.env` file and add:
```env
GEMINI_API_KEY=your_google_gemini_api_key
```

### **4. Run the FastAPI Server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **5. Test API in Browser**
Visit: **[http://localhost:8000/docs](http://localhost:8000/docs)** (Swagger UI for testing endpoints)

## Deployment
- **Docker**: Build and deploy using Docker.
- **Cloud Deployment**: Deploy on **Google Cloud Run, AWS Lambda, or a VPS**.

## Future Enhancements
- Add support for **image upscaling and enhancements**.
- Implement **user authentication & API rate limiting**.
- Allow users to generate multiple images per request.

## License
This project is licensed under the **MIT License**.

## Contributors
- **Partha Saradhi** - [GitHub](https://github.com/wittyparth)

---
### **🚀 Ready to Generate Stunning AI Images? Start Using the API Today!**

