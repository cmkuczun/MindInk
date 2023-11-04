#!/usr/bin/env python3
from keras.models import load_model
from sd_api import get_img
from keras.preprocessing import image
import numpy as np

# constants
CLASSIFIER = "cnn-5-flowers-model"


# predict the type of flower that it it
def keras_predict(model, img_path):
    # process the image
    image_path = img_path
    img = image.load_img(image_path, target_size=(224, 224))  # adjust target size to match model's input size
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0 # normalize

    # predict class for image
    predictions = model.predict(img)
    print(predictions)


# main function flow
def main():
    # get trained classifier
    model = load_model(CLASSIFIER)
    model.summary()

    # ask user for input as to what type of flower they want SD to generate
    prompt = input("what type of flower do you want to see an image of? ")
    
    # send request to SD api with user input
    img = get_img(prompt)

    # display image & ask user whether the output is correct or not
    # TODO
    img_path = ""

    # pass image through classifier
    keras_predict(model, img_path)

if __name__ == "__main__":
    main()