'''
Smart AI assistants have been subject to Dolphin Attacks. We propose a vision based defense in which a camera is used to detect if there is a person visible within the environment.

The Smart AI assistant is typically linked to a network, hence enabling us to perform a cloud-based defense.


'''

import time
import threading
import queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from openai import OpenAI
from ObjectDetection import CloudHumanDetection, LocalHumanDetection
# from devices import LidarCamera

# File to monitor
TARGET_FILE = "audio.mp3"
currentWorkingDirectory = os.getcwd() + '/'
environ_image = currentWorkingDirectory + 'environmentImage.jpg'
depth_image = currentWorkingDirectory + 'depthImage.jpg'

# Human Detection Model
# humanDetector = CloudHumanDetection(currentWorkingDirectory+"key.txt", environ_image)
humanDetector = LocalHumanDetection(environ_image)
# camera = LidarCamera(environ_image, depth_image)

# Shared flag for human detection
person_detected_flag = threading.Event()

# Queue to store transcription result
transcription_queue = queue.Queue()

# Transcription service
with open(currentWorkingDirectory+"ObjectDetection/key.txt", "r") as file:
    api_key = file.read().strip()
client = OpenAI(api_key=api_key)

# Thread 1: Transcribe the recorded request
def transcription():
    print("Starting Whisper AI transcription...")
    try:
        with open(TARGET_FILE, "rb") as audio_file:
            response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            transcription_queue.put(response.text)  # Store result in queue
            print("Transcription Completed")
    except Exception as e:
        print(f"Error in transcription: {e}")
        transcription_queue.put("Transcription failed.")

# Thread 2: Determine if there is a person present in the environment/setting
def human_detection():
    # Take Image


    # Run Cloud Human Detection
    if humanDetector.identify_person() :
        print("Person detected!")
        person_detected_flag.set()  # Set flag if a person is detected
        
    print("Human Detection Completed")

# Custom Event Handler for file monitoring
class AudioFileHandler(FileSystemEventHandler):
    last_execution_time = 0
    cooldown_time = 1  # Cooldown period in seconds

    def on_modified(self, event):
        if event.src_path.endswith(TARGET_FILE):
            current_time = time.time()
            if current_time - self.last_execution_time > self.cooldown_time:
                print(f"{TARGET_FILE} modified! Running tasks...")
                self.last_execution_time = current_time
                run_threads()

    def on_created(self, event):
        if event.src_path.endswith(TARGET_FILE):
            current_time = time.time()
            if current_time - self.last_execution_time > self.cooldown_time:
                print(f"{TARGET_FILE} created! Running tasks...")
                self.last_execution_time = current_time
                run_threads()

# Function to run two threads and retrieve transcription result
def run_threads():
    global person_detected_flag
    person_detected_flag.clear()  # Reset flag before new detection
    transcription_queue.queue.clear()  # Clear queue to avoid old values

    thread1 = threading.Thread(target=transcription)
    thread2 = threading.Thread(target=human_detection)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for human detection first
    thread2.join()

    # If a person is detected, exit early
    if not person_detected_flag.is_set():
        print("Exiting early from run_threads(). Person not detected.")
        return

    # Otherwise, continue transcription
    thread1.join()

    # Retrieve the transcription result
    if not transcription_queue.empty():
        transcription_result = transcription_queue.get()
        print(f"Transcription Result:\n{transcription_result}")  # Use the returned transcription

    print("Both threads finished")

# Watchdog observer setup
def monitor_directory():
    path = os.getcwd()  # Monitor current directory
    event_handler = AudioFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    print(f"Monitoring {TARGET_FILE} for changes...")

    try:
        while True:
            time.sleep(1)  # Keep script running
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

# Run the directory monitor
if __name__ == "__main__":
    monitor_directory()
