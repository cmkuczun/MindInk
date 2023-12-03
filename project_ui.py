#!/usr/bin/env python3

'''
project_ui.py:  final product that allows user to generate flower images using 
                the Stable Diffusion API, use the ResNet50 classifier to predict
                classes, and compare accuracy of the image generation model and 
                the image classifier over a series of runs
'''

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from main import *
from backend.classifier.predict import *
import time


def main():
    print()
    print("  MINDINK  ")
    print("  - ")
    print("   - ")
    print("     - ")
    print("     - ")
    print("   *****   ")
    print(" *       * ")
    print(" *  O O  * ")
    print(" *   ∆   * ")
    print(" *   -   * ")
    print(" *       * ")
    print("   *****   ")

    for i in range(3):
        print("   - ")
        time.sleep(.75)

    # print("-"*125)
    print("\nWelcome to MINDINK: generate images using image generation model, and classify them using the ResNet50 image classifier!\n\n")
    # print("-"*125)
    

    print("*"* 41)
    print("{FLOWER OPTIONS} ")
    print("  TULIP, DAISY, ROSE, SUNFLOWER, DANDELION")
    # Uncomment for options for ResNet50 model
    # print("  ASTILBE, BLACK EYED SUSAN, CALENDULA,")
    # print("  CALIFORNIA POPPY, CARNATION, TULIP,")
    # print("  COMMON DAISY, COREOPSIS, DANDELION,")
    # print("  IRIS, ROSE, SUNFLOWER, WATER LILY")
    print("*"* 41)
    time.sleep(1)

    # Indicate to user that the model is being loaded
    print("\nLoading trained image classifier...\n")
    model = get_model()

    # Add note just to warn user (kind of user manual?)
    print("\n!!! [USER INPUT] indicates that you need to input either a word or symbol.\n\n\n")
    time.sleep(3)

    # Initialize to track overall accuracy for both SD model and classifier
    total_attempts = 0
    sd_correct = 0
    classifier_correct = 0
    
    while True:
        total_attempts += 1

        # Get user input
        prompt = input("\n[USER INPUT] What type of flower do you want to see an image of (press ENTER)? ")
        
        # Query the API to get the image
        print("\nSending POST request to API...")
        success, res_img_path = get_image(prompt)
        
        # Display image for 5 seconds before closing it automatically
        ImageAddress = res_img_path
        ImageItself = Image.open(ImageAddress)
        ImageNumpyFormat = np.asarray(ImageItself)
        plt.imshow(ImageNumpyFormat)
        plt.draw()
        plt.pause(5) # Pause 5 seconds
        plt.close()

        # Ask user whether the model generated the correct image
        print("\nHere is the image Stable Diffusion generated for you!")
        sd_res = input("\n[USER INPUT] Is this the flower you wanted to see (Y/N)? ").upper()

        # Pass the image into ResNet50 classifier for predicting!
        if success:
            # Format the image & predict its class
            new_img = format_image(res_img_path)
            print()
            res = predict(new_img, model)

            # Clean up labels: replace any underscores with spaces
            res.replace("_", " ")
            print(f"\nClassifier predicted class: {res.upper()}")
            
            # Ask user whether this image matches what was 
            classifier_res = input("\n[USER INPUT] Was the image classified correctly (Y/N)? ").upper()

            # On success, track performance of SD model and classifier
            if sd_res == "Y":
                sd_correct += 1
            if classifier_res == "Y":
                classifier_correct += 1
            
            # Report results to user
            try:
                print()
                print("-"*40)
                print("CURRENT RESULTS")
                print(f"  SD accuracy: {str((sd_correct/total_attempts)*100)}%")
                print(f"  Classifier accuracy: {str((classifier_correct/total_attempts)*100)}%")
                print("-"*40)
            except:
                print("\nWARNING: Some of your inputs may have been wrong!")
                continue

        else:
            # Raise a sort of error indication
            print("\nSomething went wrong. Please try again!")
        
        # Check if user wants to do another round of generation
        cont = input("\n[USER INPUT] Do you want to try again (Y/N)? ").upper()
        if cont == "N":
            print()
            print("   *****   ")
            print(" *       * ")
            print(" *  > <  * ")
            print(" *   ∆   * ")
            print(" *   ^   * ")
            print(" *       * ")
            print("   *****   ")
            print("\n  GOODBYE  \n")
            
            break


if __name__ =="__main__":
    main()