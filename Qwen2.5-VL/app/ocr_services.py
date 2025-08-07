from PIL import Image
import base64
import requests
import io

def pil_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_img

def perform_ocr(image: Image.Image) -> str:
    image_base64 = pil_to_base64(image)
    prompt = "What is written in the image?"
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen2.5vl:7b",
        "prompt": prompt,
        "images": [image_base64],
        "stream": False
    })
    
    data = response.json()
    return data.get("response", "No text found")
