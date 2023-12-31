#! /usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout 
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report
import tensorflow as tf
import cv2
import os
import numpy as np


# Constants
DIRNAME = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIRNAME, '../data/flowers-four-types-dataset')
TULIP_DIR = os.path.join(DIRNAME, '../data/flowers-four-types-dataset/tulip')
DAISY_DIR = os.path.join(DIRNAME, '../data/flowers-four-types-dataset/daisy')
IMG_SIZE = 224


# Load data
def get_data(data_path):
    train_data = [] 
    test_data = []

    # Training
    path = os.path.join(data_path, 'train')
    for img in os.listdir(path):
        try:
            img_arr = cv2.imread(os.path.join(path, img))[...,::-1] # convert BGR to RGB format
            resized_arr = cv2.resize(img_arr, (IMG_SIZE, IMG_SIZE)) # reshape images to preferred size
            train_data.append([resized_arr])
        except Exception as e:
            print(e)

    # Testing
    path = os.path.join(data_path, 'test')
    for img in os.listdir(path):
        try:
            img_arr = cv2.imread(os.path.join(path, img))[...,::-1] # convert 
            resized_arr = cv2.resize(img_arr, (IMG_SIZE, IMG_SIZE)) # reshape
            test_data.append([resized_arr])
        except Exception as e:
            print(e)

    return np.array(train_data), np.array(test_data)


# Execute training & validation of classifier
def main():
    # Get train and test data
    tulip_train, tulip_test = get_data(TULIP_DIR)
    daisy_train, daisy_test = get_data(DAISY_DIR)
    # Add labels
    t_train_labels = np.array([0] * 787)
    t_test_labels = np.array([0] * 197)
    d_train_labels = np.array([1] * 611)
    d_test_labels = np.array([1] * 154)

    # Join train
    training = np.concatenate((tulip_train, daisy_train))
    # Join test
    testing = np.concatenate((tulip_test, daisy_test))

    # Visualize data
    l = []
    for i in tulip_train:
        l.append("tulip")
    for i in daisy_train:
            l.append("daisy")
    sns.set_style('darkgrid')
    sns.countplot(l)
    # plt.show( )

    # Preprocessing
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    for feature, label in zip(tulip_train, t_train_labels):
        x_train.append(feature)
        y_train.append(label)
    for feature, label in zip(daisy_train, d_train_labels):
        x_train.append(feature)
        y_train.append(label)
    
    for feature, label in zip(tulip_test, t_test_labels):
        x_test.append(feature)
        y_test.append(label)
    for feature, label in zip(daisy_test, d_test_labels):
        x_test.append(feature)
        y_test.append(label)

    # Normalize data
    x_train = np.array(x_train) / 255
    x_test = np.array(x_test) / 255

    x_train.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y_train = np.array(y_train)

    x_test.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y_test = np.array(y_test)
    print("data has been normalized")

    # Augment training data
    datagen = ImageDataGenerator(
        featurewise_center=False,               # set input mean to 0 over the dataset
        samplewise_center=False,                # set each sample mean to 0
        featurewise_std_normalization=False,    # divide inputs by std of the dataset
        samplewise_std_normalization=False,     # divide each input by its std
        zca_whitening=False,                    # apply ZCA whitening
        rotation_range = 30,                    # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.2,               # random zoom 
        width_shift_range=0.1,          # random shift horizontally (fraction of total width)
        height_shift_range=0.1,         # random shift vertically (fraction of total height)
        horizontal_flip = True,         # random flip
        vertical_flip=False)       
    
    reshaped_x_train_data = np.squeeze(x_train, axis=1)
    datagen.fit(reshaped_x_train_data)
    print(f"x_test shape = {np.shape(x_test)}")
    print(f"y_train shape = {np.shape(y_train)}")
    print(f"y_test shape = {np.shape(y_test)}")

    reshaped_x_test_data = np.squeeze(x_test, axis=1)

    # Define CNN with 3 convolutional layers
    print("defining CNN with 3 convolutional layers...")
    model = Sequential()
    model.add(Conv2D(32,3,padding="same", activation="relu", input_shape=(IMG_SIZE,IMG_SIZE,3)))
    model.add(MaxPool2D())

    model.add(Conv2D(32, 3, padding="same", activation="relu"))
    model.add(MaxPool2D())

    model.add(Conv2D(64, 3, padding="same", activation="relu"))
    model.add(MaxPool2D())
    model.add(Dropout(0.4))

    model.add(Flatten())
    model.add(Dense(128,activation="relu"))
    model.add(Dense(2, activation="softmax"))

    model.summary()
    print("model created!!")

    opt = tf.keras.optimizers.legacy.Adam(lr=0.000001) # lower learning rate
    # SparseCategoricalCrossentropy as loss function
    model.compile(  optimizer = opt,\
                    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),\
                    metrics = ['accuracy'])

    # Train model for 500 epochs
    print("\ntraining model...")
    history = model.fit(reshaped_x_train_data, y_train, epochs = 500, validation_data = (reshaped_x_test_data, y_test))
    model.save("CNN-RETRAIN-BASIC")

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(500)

    plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

    predictions = model.predict_classes(x_test)
    predictions = predictions.reshape(1,-1)[0]
    print(classification_report(y_test, predictions, target_names = ['Tulip (Class 0)','Daisy (Class 1)']))


if __name__ == "__main__":
    main()

