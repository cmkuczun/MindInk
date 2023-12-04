#!/usr/bin/env python3

'''
predict.py: contains all methods required to make API calls, save images, 
            format images, and make predictions using the classifier
'''

from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import requests
import os
import base64
from PIL import Image
from io import BytesIO
import json


# Constants
DIRNAME = os.path.dirname(__file__)
CLASSIFIER = os.path.join(DIRNAME, 'cnn-5-flowers-model')
# CLASSIFIER = os.path.join(DIRNAME, 'resnet50_fin') # Uncomment for ResNet50



# Format/process image for prediction
def format_image(image_path):  
    # Adjust target size to match model's input size
    img = image.load_img(image_path, target_size=(224, 224))  # Change to 180x180 for ResNet50
    # img = image.load_img(image_path, target_size=(180, 180))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0 # normalize
        
    return img

    
# Actually get the image with prompt
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

        
# Get model instance
def get_model():
    model = load_model(CLASSIFIER)
    print(CLASSIFIER)
    return model


# Ask user for flower
def get_prompt():
    prompt = input("what type of flower do you want to see an image of? ")
    return prompt


# Assign label to image
def predict(img, model):
    # Uncomment for ResNet50
    # class_names = [ 'astilbe', 'black-eyed susan', 'black_eyed_susan', 'calendula', \
    #                 'california_poppy', 'carnation', 'common_daisy', 'coreopsis', \
    #                 'dandelion', 'iris', 'rose', 'sunflower', 'tulip', 'water_lily']
    
    class_names = ['Tulip', 'Daisy', 'Rose', 'Sunflower', 'Dandelion']
    
    # Predict class for image
    new_img = np.array([list(img)])
    reshaped_img = np.squeeze(new_img, axis=1)
    predictions = model.predict(reshaped_img)

    # Get predicted class
    output = np.argmax(predictions)
    return class_names[output]


def resnet_decode_predictions(preds, top=1, class_list_path='index.json'):
  if len(preds.shape) != 2 or preds.shape[1] != 14: # your classes number
    raise ValueError('`decode_predictions` expects '
                     'a batch of predictions '
                     '(i.e. a 2D array of shape (samples, 14)). '
                     'Found array with shape: ' + str(preds.shape))
  json_path = os.path.join(DIRNAME, class_list_path)
  index_list = json.load(open(json_path))
  results = []
  for pred in preds:
    top_indices = pred.argsort()[-top:][::-1]
    result = [tuple(index_list[str(i)]) + (pred[i],) for i in top_indices]
    result.sort(key=lambda x: x[2], reverse=True)
    results.append(result)

  res = results[0][0]
  str_res = ""
  for elem in res:
      if isinstance(elem, str):
          str_res += elem
  return str_res


if __name__ == "__main__":
    p = get_prompt()
    get_image(p)
    print("querying dream api...\n")
