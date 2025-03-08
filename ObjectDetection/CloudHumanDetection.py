import base64
from openai import OpenAI

# Read the API key from key.txt
with open("key.txt", "r") as file:
    api_key = file.read().strip()

client = OpenAI(api_key=api_key)  # Pass the API key

# Convert the image to base64
with open("environmentImage.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

prompt = '''
Here is a photo taken by a camera. Tell me:
Is there a person present in the setting? A person featured in a canvas or photo does not count. If there is a person present, they must be directly facing and looking at the camera. Answer "yes" or "no".
'''

# Send the image in base64 format
completion = client.chat.completions.create(
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

print(completion.choices[0].message)

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