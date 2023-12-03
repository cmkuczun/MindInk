#!/usr/bin/env python3

'''
predict.py: contains all methods required to make API calls, save images, 
            format images, and make predictions using the classifier
'''

# imports
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import requests
import os
import base64
from PIL import Image
from io import BytesIO


# constants
CLASSIFIER = "/Users/claudia/intro-to-ai/ai-proj-mindink/MindInk/backend/classifier/cnn-5-flowers-model"


# format/process image for prediction
def format_image(image_path):  
    # adjust target size to match model's input size
    img = image.load_img(image_path, target_size=(224, 224))  # TODO: change back to 180x180
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0 # normalize
        
    return img

    
# actually get the image with prompt
def get_image(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    text = f"photograph of {prompt}"

    body = {
    "steps": 40,
    "width": 1024,
    "height": 1024,
    "seed": 0,
    "cfg_scale": 5,
    "samples": 1,
    "text_prompts": [
        {
        "text": text,
        "weight": 1
        },
        {
        "text": "blurry, bad",
        "weight": -1
        }
    ],
    }

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-KvlbMwLxHqnqVe2oHgCwtMYTguPsYZzfqHq9w2gUJ1AssMQO", 
    }

    try:
        response = requests.post(
        url,
        headers=headers,
        json=body,
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))
        data = response.json()

        # make sure the out directory exists
        if not os.path.exists("./out"):
            os.makedirs("./out")

        image_path = ""
        for i, image in enumerate(data["artifacts"]):
            image_path = f'./out/txt2img_{image["seed"]}.png'
            with open(f'./out/txt2img_{image["seed"]}.png', "wb") as f:
                f.write(base64.b64decode(image["base64"]))
        
            return True, image_path
    except:
        print("something went wrong during POST call or saving the image:(")
        return False, ""

        
# get model instance
def get_model():
    model = load_model(CLASSIFIER)
    return model


# ask user for flower
def get_prompt():
    prompt = input("what type of flower do you want to see an image of? ")
    return prompt


# assign label to image
def predict(img, model):
    # class_names = [ 'astilbe', 'bellflower', 'black_eyed_susan', 'calendula', \
    #                 'california_poppy', 'carnation', 'common_daisy', 'coreopsis', \
    #                 'dandelion', 'iris', 'rose', 'sunflower', 'tulip', 'water_lily']
    
    class_names = ['Tulip', 'Daisy', 'Rose', 'Sunflower', 'Dandelion']
    # predict class for image
    new_img = np.array([list(img)])
    reshaped_img = np.squeeze(new_img, axis=1)
    predictions = model.predict(reshaped_img)

    # get predicted class
    output = np.argmax(predictions)
    
    return class_names[output]


if __name__ == "__main__":
    p = get_prompt()
    get_image(p)
    print("querying dream api...\n")
