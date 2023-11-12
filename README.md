## MindInk

Website, dataset, and model(s) for CSE-20124 Intro to AI course project.
This repository contains three trained models, on three different datasets.

Model 1: General CNN with 3 Convolutional Layers
- Dataset: two flower types (tulip and daisy) split into training and testing/validation sets
- Overview: used to determine if model is trainable on flowers, acts as a starting point for work and introduction with training my own models
- Trained locally on MacBook Pro

Model 2: General CNN with 3 Convolutional Layers
- Dataset: 5 types of flower, also split into training and testing sets (full dataset of segment that was used above)
- Overview: initial test to see if CNN model trainable on many types of flowers
- Trained locally on MacBook Pro

Model 3: ResNet50 
- Dataset: 14 types of flowers, split into training and validation sets
- Overview: will be used for classification, but initially will compare a few test cases to look at this output versus output of previous model (CNN with 3 layers)
- Trained on Kaggle using GPU acceleration

Control Flow:
1. User selects a flower type to be generated
2. Make call to Stable Diffusion API (GET request)
3. Extract image from HTTP response
4. Have user confirm whether generated flower type is correct
5. Pass image through classifier
6. Have user confirm whether output label matches flower type (if flower is correctly generated)
7. Verify output of classifier with SD generation - 4 possible scenarios
  a. SD generates correct image but ResNet50 fails to classify correctly
  b. SD generates incorrect image but ResNet50 classifies correctly
  c. SD generates correct image and ResNet50 classifies correctly
  d. SD generates incorrect image and ResNet50 fails to classify correct label
8. Output a message to user containing SD and classifier output, comparing and seeing if one/both is/are wrong

Components:
1. Front-end -> website, user interface
2. Back-end -> datasets, models, training and testing scripts
