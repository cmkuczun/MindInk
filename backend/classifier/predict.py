#!/usr/bin/env python3

# imports
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions 
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import time
import os
import json 
import requests
import io
from urllib.request import urlopen, Request
import urllib.request


# constants
CLASSIFIER = "/Users/claudia/ai-proj-mindink/MindInk/backend/classifier/resnet50_model"


# format image for prediction
def format_image(image_path):
    # process the image
    # image_path = img_path
    img = image.load_img(image_path, target_size=(180, 180))  # adjust target size to match model's input size
    # img = Image.open(BytesIO(img))
    # resized_img = img.resize(target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0 # normalize
    return img


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None
    
# actually get the image with prompt
def get_image(prompt):
    path = "/Users/claudia/ai-proj-mindink/MindInk/backend/classifier/sd-images/curr_img.jpg"
    url = "https://stablediffusionapi.com/api/v3/text2img"
    
    payload = {
        "key": "Jct9YahzVLelCHXwiZZlI0pk7HsPBKwNv88Xs4KZHF0gBhTmMl14hfQ4PIpY",
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
            
            # b = BytesIO()
            # image = Image.open(path_to_image)
            # image.save(b, format='PNG')
            # b.seek(0)
            # b.read()
            # return image_bytes
            # filename = os.path.basename(image_url[0])
            # image_path = os.path.join(path, filename)

            # # print(f"content = {response.content}")
            # # Open the file in binary write mode and save the image
            # with open(image_path, 'wb') as file:
            #     file.write(response.content)
            # print(f"Image saved at {image_path}")

        else:
            print("Failed to download the image.")
            # return None
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
        req = Request(url=json_data["output"][0], headers=headers) 
        html = urlopen(req).read() 
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36')

        # urllib.request.urlretrieve(json_data["output"][0], path)
        
        # print(json_data["output"])
        return path

        
    

# get model instance
def get_model():
    # get trained classifier
    model = load_model(CLASSIFIER)
    # model.summary() # TODO
    return model
    

# query standard diffusion for image to be generated
def query_sd_api(prompt):
    # send request to SD api with user input & reformat img
    img = get_image(prompt)
    img = format_image(img)
    # display image & ask user whether the output is correct or not
    # TODO
    img_path = ""
    return img


# ask user for prompt
def get_prompt():
    # ask user for input as to what type of flower they want SD to generate
    prompt = input("what type of flower do you want to see an image of? ")
    return prompt


# assign label to image
def predict(img, model):
    # predict class for image
    new_img = format_image(img)
    new_img = np.array([list(new_img)])
    reshaped_img = np.squeeze(new_img, axis=1)
    predictions = model.predict(reshaped_img)
    print(predictions)

    y_classes = predictions.argmax(axis=-1)
    print(f"OUTPUT = {y_classes}")
    return predictions

if __name__ == "__main__":
    p = get_prompt()

    print("querying SD API...")
    img = query_sd_api(p)