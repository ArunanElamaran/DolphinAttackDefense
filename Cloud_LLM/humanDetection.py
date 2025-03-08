import base64
from openai import OpenAI

# Read the API key from key.txt
with open("key.txt", "r") as file:
    api_key = file.read().strip()

client = OpenAI(api_key=api_key)  # Pass the API key

# Convert the image to base64
with open("environmentImage.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

# Send the image in base64 format
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
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
