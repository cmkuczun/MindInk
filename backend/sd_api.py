#!/usr/bin/env python3
import requests
from PIL import Image
from io import BytesIO
import time
import os

# # API endpoint and your API key
# url = "https://stablediffusionapi.com/api/v3/text2img"
# api_key = ""

# # Text input for generating an image
# text = "rose flower"

# # Request headers with your API key
# headers = {
#     "Content-Type": "application/json",
# }

# # Request body as a dictionary
# data = {
#     "key": "",
#     "prompt": text,
#     "width": "512",
#     "height": "512",
#     "samples": "1",
#     "num_inference_steps": "20",
#     "guidance_scale": 7.5,
#     "safety_checker":"yes"
# }

# # Send a POST request to the Text2Img API
# response = requests.request("POST", url, headers=headers, json=data)

# if response.status_code == 200:
#     # Parse the response JSON to get the image URL
#     response_data = response.json()
#     image_url = response_data.get("image_url")

#     # Download the image
#     image_response = requests.get(image_url)
#     if image_response.status_code == 200:
#         # Open and display the image
#         image_bytes = BytesIO(image_response.content)
#         image = Image.open(image_bytes)
#         image.show()
#     else:
#         print("Failed to download the image.")
# else:
#     print(f"API request failed with status code {response.status_code}: {response.text}")



import requests
import json

def get_image(prompt):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    
    payload = {
        "key": "",
        "prompt": prompt,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "guidance_scale": 7.5,
        "safety_checker":"yes"
        }

    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    json_data = json.loads(response.text)
    if response.status_code == 200:
        response_data = response.json()
        image_url = response_data.get("output")

        # Download the image
        image_response = requests.get(image_url[0])
        if image_response.status_code == 200:
            # Open and display the image
            image_bytes = BytesIO(image_response.content)
            image = Image.open(image_bytes)
            image.show()

            filename = os.path.basename(image_url[0])

            # Open the file in binary write mode and save the image
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded as {filename}")
        else:
            print("Failed to download the image.")

        return json_data["output"]

if __name__ == "__main__":
    prompt = "daisy flower"
    print(f"response = {get_img(prompt)}")

