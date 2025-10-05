# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import uuid
from analysis.movement_analyzer import analyze_video_movement

# Setup
app = FastAPI(title="Callus AI ML Dance Server", version="1.0.0")
UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "AI ML Server Engineer Assessment"}

@app.post("/analyze")
async def analyze_video(video_file: UploadFile = File(...)):
    """Accepts a video file, analyzes movement, and returns a JSON summary."""
    
    # 1. Input Validation and Saving
    if not video_file.filename.lower().endswith(('.mp4', '.mov')):
        raise HTTPException(status_code=400, detail="Only MP4 or MOV files are supported.")
    
    # Generate a unique filename to prevent conflicts
    unique_filename = f"{uuid.uuid4()}_{video_file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        # Save the uploaded file to the local directory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
            
        # 2. Run Analysis
        analysis_result = analyze_video_movement(file_path)
        
        # 3. Handle Errors
        if "error" in analysis_result:
            raise HTTPException(status_code=500, detail=f"Analysis Error: {analysis_result['error']}")
            
        # 4. Return Result
        return JSONResponse(content=analysis_result)

    except Exception as e:
        # 5. General Error Handling
        print(f"An error occurred during processing: {e}")
        raise HTTPException(status_code=500, detail=f"Server Processing Error: {str(e)}")
        
    finally:
        # 6. Cleanup (Crucial for a production server)
        if os.path.exists(file_path):
            os.remove(file_path)
            