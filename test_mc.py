import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

print("Testing microphone... Speak into your laptop now!")
try:
    # Trying to record exactly 3 seconds of audio
    recording = sd.rec(int(3 * 16000), samplerate=16000, channels=1, dtype=np.int16)
    sd.wait()
    write("test_audio.wav", 16000, recording)
    print("SUCCESS! Audio captured and saved.")
except Exception as e:
    print(f"CRASH: {e}")