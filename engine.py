import whisper
import pyttsx3
import os
import sounddevice as sd
from scipy.io.wavfile import write

print("Loading Whisper model...")
model = whisper.load_model("base")

def record_audio(duration=4):
    """Records audio using modern sounddevice library, bypassing PyAudio."""
    fs = 44100  # Standard audio sample rate
    
    print(f"Listening for {duration} seconds...")
    try:
        # Turn on the mic and record
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait for the recording to finish
        print("Recording complete.")
        
        # Save the audio file for Whisper
        filename = "temp_audio.wav"
        write(filename, fs, recording)
        
        return filename
        
    except Exception as e:
        print(f"Microphone Error: {e}")
        return None

def transcribe(audio_path):
    """Transcribes audio using the Whisper model."""
    if not audio_path or not os.path.exists(audio_path): 
        return ""
    
    # fp16=False prevents warnings on standard CPUs
    result = model.transcribe(audio_path, fp16=False)
    return result["text"].strip().lower()

def speak(text):
    """Speaks the text using the local pyttsx3 engine."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160) 
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS Error: {e}")