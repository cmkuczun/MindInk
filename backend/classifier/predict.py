#!/usr/bin/env python3

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
CLASSIFIER = "/Users/claudia/intro-to-ai/ai-proj-mindink/MindInk/backend/classifier/resnet50_model"


# format/process image for prediction
def format_image(image_path):
    print(f"type of image_path: {type(image_path)}")
    # with open(image_path, "r") as f:
    #     img_crop_pil = Image.fromarray(np.array(list(f)))
    #     byte_io = BytesIO()
    #     img_crop_pil.save(byte_io, format="JPG")
    #     jpg_buffer = byte_io.getvalue()
    #     byte_io.close()

    # adjust target size to match model's input size
    img = image.load_img(image_path, target_size=(180, 180))  
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0 # normalize
        
    return img

    
# actually get the image with prompt
# TODO: build user prompt into actual request being sent!
def get_image(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
    "steps": 40,
    "width": 1024,
    "height": 1024,
    "seed": 0,
    "cfg_scale": 5,
    "samples": 1,
    "text_prompts": [
        {
        "text": "photograph of carnations",
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
    } # TODO: REMOVE API KEY?

    print("sending post response to api url...\n")
    try:
        response = requests.post(
        url,
        headers=headers,
        json=body,
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))
        print("got past status check")
        data = response.json()

        # make sure the out directory exists
        # if not os.path.exists("./out"):
        #     os.makedirs("./out")

        image_path = ""
        for i, image in enumerate(data["artifacts"]):
            image_path = f'./out/txt2img_{image["seed"]}.png'
            print(image_path)
            with open(f'./out/txt2img_{image["seed"]}.png', "wb") as f:
                f.write(base64.b64decode(image["base64"]))
            print("success!\n")
        
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
    class_names = [ 'astilbe', 'bellflower', 'black_eyed_susan', 'calendula', \
                    'california_poppy', 'carnation', 'common_daisy', 'coreopsis', \
                    'dandelion', 'iris', 'rose', 'sunflower', 'tulip', 'water_lily']
    
    # predict class for image
    # new_img = format_image(img)
    new_img = np.array([list(img)])
    reshaped_img = np.squeeze(new_img, axis=1)
    predictions = model.predict(reshaped_img)

    # get predicted class
    output = np.argmax(predictions)
    # print(f"PREDICTED CLASS = {class_names[output]}")
    # y_classes = predictions.argmax(axis=-1)
    # print(f"OUTPUT = {y_classes}")
    
    return class_names[output]


if __name__ == "__main__":
    p = get_prompt()
    get_image(p)
    print("querying dream api...\n")
