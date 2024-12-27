import shutil
from fastapi import FastAPI
from pedalboard import Pedalboard, load_plugin 
from pedalboard.io import AudioFile
from fastapi import UploadFile
import tempfile
import os

def process_reverb(file: UploadFile, plugin_path: str):
     with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, f"temp_{file.filename}")
        output_path = os.path.join(temp_dir, f"processed-{file.filename}.wav")
        permanent_output_path = os.path.join("processed_files", f"processed-{file.filename}.wav")  # Permanent location
        
        # Ensure the permanent directory exists
        os.makedirs(os.path.dirname(permanent_output_path), exist_ok=True)
        
        with open(input_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Process and return the path to the output file
        sample_rate = 44100.0
        with AudioFile(input_path) as f:
            audio = f.read(f.frames)
        
        effect = load_plugin(plugin_path)
        effect.delay_ms = 267.0
        effect.feedback = 50.1
        effect.mix = 75.0
        effect.width = 72.4
        
        effected = effect(audio, sample_rate)
        with AudioFile(output_path, 'w', sample_rate, effected.shape[0]) as f:
            f.write(effected)
        
        # Copy the processed file to the permanent location
        shutil.copy(output_path, permanent_output_path)
        
        return permanent_output_path
        