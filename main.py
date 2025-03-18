from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
client = genai.Client(api_key=f"{os.getenv('GEMINI_API_KEY')}")

@app.post("/generate-image/")
async def generate_image(data: dict):
    """
    Generates an AI-enhanced image based on user input.
    
    Request JSON:
    {
        "prompt": "A futuristic flying car in a neon cyberpunk city",
        "aspect_ratio": "16:9",
        "style": "Realistic"
    }
    """
    try:
        user_prompt = data.get("prompt")
        aspect_ratio = data.get("aspect_ratio", "1:1")  # Default to square
        style = data.get("style", "Default")
        print("Request received")

        if not user_prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        # Step 1: Enhance the prompt using Gemini LLM
        enhancement_prompt = (
            f"Enhance this image prompt with more vivid details while keeping the meaning intact: "
            f"{user_prompt}, Style: {style}, Aspect Ratio: {aspect_ratio}"
        )

        try:
            enhanced_response = client.models.generate_content(
                model="gemini-1.5-pro",  # Use a strong LLM for text enhancement
                contents=enhancement_prompt
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error enhancing prompt: {str(e)}")

        if not enhanced_response.candidates:
            raise HTTPException(status_code=500, detail="Failed to enhance prompt")

        enhanced_prompt = enhanced_response.candidates[0].content.parts[0].text

        # Step 2: Generate the image with the enhanced prompt
        try:
            image_response = client.models.generate_content(
                model="gemini-2.0-flash-exp-image-generation",
                contents=enhanced_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

        image_data = None
        for part in image_response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                break

        if not image_data:
            raise HTTPException(status_code=500, detail="Image generation failed")

        # Save image
        image = Image.open(BytesIO(image_data))
        image_path = "generated_image.png"
        image.save(image_path)

        # Option 1: Send as Base64 JSON Response
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return JSONResponse(content={"enhanced_prompt": enhanced_prompt, "image_base64": img_str})

        # Option 2: Serve as a File
        # return FileResponse(image_path, media_type="image/png")

    except HTTPException as http_err:
        return JSONResponse(status_code=http_err.status_code, content={"error": http_err.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unexpected error: {str(e)}"})
