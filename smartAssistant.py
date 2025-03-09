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


# Transcription Model

# Thread 1: Transcribe the recorded request
def transcription():
    print("Task One Started")
    for i in range(5):
        print(f"Task One Running... {i}")
        time.sleep(1)
    print("Task One Completed")

# Thread 2: Determine if there is a person present in the environment/setting
def human_detection():
    print("Task Two Started")
    for i in range(5):
        print(f"Task Two Running... {i}")
        time.sleep(1)
    print("Task Two Completed")

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
    thread1 = threading.Thread(target=transcription)
    thread2 = threading.Thread(target=human_detection)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

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
