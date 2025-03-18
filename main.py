from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini API client
client = genai.Client(api_key=f"{os.getenv('GEMINI_API_KEY')}")

# Define Request Model
class ImageRequest(BaseModel):
    prompt: str
    enhance_prompt: bool = False
    style: str = "Realistic"
    aspect_ratio: str = "16:9"
    detail_level: str = "High"
    lighting_mood: str = "Bright & Vibrant"
    camera_view: str = "Wide-angle"
    composition: str = "Centered"
    color_palette: str = "Vibrant"
    background: str = "Detailed"
    num_variants: int = 1

@app.post("/generate-image/")
async def generate_image(request: ImageRequest):
    try:
        # Enhance prompt if needed
        final_prompt = request.prompt
        if request.enhance_prompt:
            enhancement_response = client.models.generate_content(
                model="gemini-1.5-pro-latest",
                contents=f"Improve this image generation prompt: {request.prompt} with following parameters , {request.style}, {request.aspect_ratio}, {request.detail_level} , {request.lighting_mood}, {request.camera_view}, {request.composition}, {request.color_palette}, {request.background} within 100 words",
            )
            final_prompt = enhancement_response.candidates[0].content.parts[0].text

        # Generate image using Gemini API
        response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=final_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )

        # Extract image from response
        image_base64 = None
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_data = BytesIO(part.inline_data.data)
                img = Image.open(image_data)
                
                # Convert image to Base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                break
        
        if not image_base64:
            raise HTTPException(status_code=500, detail="Image generation failed.")

        return {"image": f"data:image/png;base64,{image_base64}"}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
