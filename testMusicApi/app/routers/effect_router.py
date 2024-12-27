from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from app.handlers.effect_handler import process_reverb

router = APIRouter()

@router.post("/reverb_effect")
async def reverb_effect(file: UploadFile = File(...)):
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Only .wav files are supported")
    
    plugin_path = r"C:\Program Files\Common Files\VST3\ValhallaSupermassive.vst3"
    
    try:
        output_path = process_reverb(file, plugin_path)
        return FileResponse(output_path, media_type="audio/wav", filename="processed-output.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")