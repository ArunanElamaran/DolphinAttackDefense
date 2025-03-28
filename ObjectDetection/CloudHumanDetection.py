# Imports for OpenAI and Image
import base64
from openai import OpenAI

# General Imports
from typing import Any, Dict, List, Tuple

class CloudHumanDetection:
    
    # Constructor
    def __init__(self, key_file, image_file) -> None:
        
        self.type = "CloudHumanDetection"

        # Image file that will get updated upon each new request
        self.image_file = image_file

        # Read the API key from key.txt
        with open(key_file, "r") as file:
            api_key = file.read().strip()

        self.client = OpenAI(api_key=api_key)

    # Call this function to determine if there is a person in the environment/setting
    def identify_person(self) -> bool:

        # Convert the image to base64
        with open(self.image_file, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        prompt = '''
        Here is a photo taken by a camera. Tell me:
        Is there a person present in the setting? A person featured in a canvas or photo does not count. If there is a person present, they must be directly facing and looking at the camera. Answer "yes" or "no".
        '''

        # prompt = '''
        # Here is a photo taken by a camera. Tell me:
        # Is there a person in the photo? Answer "yes" or "no".
        # '''

        # Send the image in base64 format
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ],
                }
            ],
        )

        # Extract the content only
        response_text = completion.choices[0].message.content.strip()
        return response_text.lower() == "yes."

# Example Usage
def test():
    import os
    import time
    image_dir = "../pictureSamples/"
    sub_dirs = ["D435", "Internet"]
    image_files = []
    
    # Collect all image file paths
    for sub_dir in sub_dirs:
        full_path = os.path.join(image_dir, sub_dir)
        for file in os.listdir(full_path):
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(full_path, file))
    
    detector = CloudHumanDetection("key.txt", image_files[0])  # Initialize with the first image
    
    for image_file in image_files:
        detector.image_file = image_file  # Update image file path
        
        start_time = time.time()
        output = detector.identify_person()
        end_time = time.time()
        
        print(f"Image: {image_file}")
        print("Person detected:", output)
        print(f"Human detection took {end_time - start_time:.2f} seconds.\n")


if __name__ == "__main__":
    test()

'''
--------------------------- Prompts to select from and test with ------------------

--- Simple Prompt: 
I will provide you with photos. Tell me:
Is there a person in the photo? Answer "yes" or "no".

--- Accounting for photos of people (no real human present in setting):
I will provide you with photos. Tell me: 
Is there a person present in the setting? A person featured in a canvas or photo does not count. Answer "yes" or "no".

--- Accounting for facing camera:
I will provide you with photos. Tell me:
Is there a person present in the setting? A person featured in a canvas or photo does not count. If there is a person present, they must be directly facing and looking at the camera. Answer "yes" or "no".

'''