import pyaudio
import wave
import webrtcvad
import time

# Recording settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # CPX microphone sample rate
CHUNK = 1024  # Buffer size
FRAME_DURATION = 30  # Frame size in ms (10, 20, or 30)
WAVE_OUTPUT_FILENAME = "cpx_voice_activity.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Find Circuit Playground Express microphone
device_index = None
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if "Circuit Playground" in info['name']:
        device_index = i
        print(f"Using CPX microphone at index {device_index}")
        break

if device_index is None:
    print("CPX microphone not found. Check the connection.")
    p.terminate()
    exit()

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

# Initialize webrtcvad
vad = webrtcvad.Vad(2)  # Set aggressiveness level (0-3)

print("Waiting for voice...")

frames = []
recording = False

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)

        # Convert raw audio to 16-bit samples
        is_speech = vad.is_speech(data, RATE)

        if is_speech:
            if not recording:
                print("* Voice detected, starting recording...")
                recording = True

            frames.append(data)

        elif recording and len(frames) > 10:  # Stop if silence persists
            print("* Silence detected, stopping recording.")
            break

except KeyboardInterrupt:
    print("\nRecording stopped manually.")

# Stop the stream
stream.stop_stream()
stream.close()
p.terminate()

# Save the recording only if frames exist
if frames:
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio saved as {WAVE_OUTPUT_FILENAME}")
else:
    print("No speech detected. No file saved.")
