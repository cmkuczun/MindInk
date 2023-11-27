#!/usr/bin/env python3

# imports
from backend.classifier.predict import get_model, predict, get_prompt, format_image, get_image


# main body flow
def main():
    pass


# test control flow with hardcoded inputs (do not ask for user input)
def test():
    # load model
    model = get_model()
    print("got model")

    # ask user for flower to generate
    prompt = get_prompt()

    # query api with user input
    success, res_img_path = get_image(prompt)
    print(res_img_path)

    if success:
        # format the image & predict its class
        new_img = format_image(res_img_path)
        res = predict(new_img, model)
        print(f"got prediction: {res}")


if __name__ == "__main__":
    test()
    #main()
