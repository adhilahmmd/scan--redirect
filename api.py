"""
api.py
FastAPI Server for LKG Literacy Lesson Identification.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import cv2
import numpy as np
import io

# Import your existing modules
from database import LessonDatabase
from processor import PageProcessor
from matcher import LessonMatcher

# Initialize App
app = FastAPI(
    title="LKG Lesson Identifier API",
    description="Upload a book page to identify the lesson.",
    version="1.0"
)

# Initialize Logic Components (Global Scope)
# We load these once when the server starts to save time on every request
try:
    db = LessonDatabase()
    processor = PageProcessor()
    matcher = LessonMatcher(db)
    print("✅ System Loaded Successfully")
except Exception as e:
    print(f"❌ Error loading system: {e}")

@app.get("/")
def home():
    return {"message": "LKG Literacy API is running. Use POST /identify to scan pages."}

@app.post("/identify")
async def identify_lesson(file: UploadFile = File(...)):
    """
    Endpoint: Upload an image file (JPEG/PNG).
    Returns: JSON object with identified lesson details.
    """
    # 1. VALIDATE FILE TYPE
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG allowed.")

    try:
        # 2. READ IMAGE FILE
        # Read the raw bytes from the uploaded file
        contents = await file.read()
        
        # Convert bytes to numpy array (OpenCV format)
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Could not process image data.")

        # 3. RUN PIPELINE (Your existing logic)
        # A. Extract Text & Visuals
        text = processor.extract_text(image)
        visuals = processor.analyze_visual_features(image)

        # B. Match Lesson
        result = matcher.identify_lesson(text, visuals)

        # 4. FORMAT RESPONSE
        response_data = {
            "status": "success",
            "confidence": result['confidence'],
            "extracted_text_preview": text[:100] + "..." if len(text) > 100 else text,
            "visual_features": visuals,
            "match": None
        }

        if result['top_match']:
            response_data["match"] = {
                "lesson_id": result['top_match']['lesson_id'],
                "name": result['top_match']['name'],
                "score": result['top_match']['score'],
                "reasoning": result['top_match']['reasons']
            }
        
        return JSONResponse(content=response_data)

    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)