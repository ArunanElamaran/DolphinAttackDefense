'''
Smart AI assistants have been subject to Dolphin Attacks. We propose a vision based defense in which a camera is used to detect if there is a person visible within the environment.

The Smart AI assistant is typically linked to a network, hence enabling us to perform a cloud-based defense.


'''

from ObjectDetection.CloudHumanDetection import CloudHumanDetection
# from ObjectDetection.LocalHumanDetection import LocalHumanDetection

import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# File to monitor
TARGET_FILE = "audio.wav"

# Human Detection Model
humanDetector = CloudHumanDetection("ObjectDetection/key.txt", "ObjectDetection/environmentImage.jpg")
# humanDetector = LocalHumanDetection("ObjectDetection/environmentImage.jpg")

# Shared flag to indicate if a person is detected
person_detected_flag = threading.Event()

# Thread 1: Transcribe the recorded request
def transcription():
    print("Task One Started")
    for i in range(5):
        print(f"Task One Running... {i}")
        time.sleep(1)
    print("Transcription Completed")

# Thread 2: Determine if there is a person present in the environment/setting
def human_detection():
    if humanDetector.identify_person():
        print("Person detected! Exiting early.")
        person_detected_flag.set()  # Set flag if a person is detected
    print("Human Detection Completed")

# Custom Event Handler for file monitoring
class AudioFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(TARGET_FILE):
            print(f"{TARGET_FILE} modified! Running tasks...")
            run_threads()

    def on_created(self, event):
        if event.src_path.endswith(TARGET_FILE):
            print(f"{TARGET_FILE} created! Running tasks...")
            run_threads()

# Function to run two threads
def run_threads():
    global person_detected_flag
    person_detected_flag.clear()  # Reset flag before new detection

    thread1 = threading.Thread(target=transcription)
    thread2 = threading.Thread(target=human_detection)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for human detection first
    thread2.join()

    # If a person is detected, exit early
    if person_detected_flag.is_set():
        print("Exiting early from run_threads(). Transcription skipped.")
        return

    # Otherwise, continue transcription
    thread1.join()

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
