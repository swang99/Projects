import cv2
import numpy as np
import os
import sys

import tensorflow as tf
from tensorflow.keras import models, layers, optimizers, utils
import keras_tuner as kt
from sklearn.model_selection import train_test_split

###############################################################################
#                                PARAMETERS
###############################################################################

IS_TUNING = False
IMG_WIDTH, IMG_HEIGHT = 30, 30
NUM_CATEGORIES = 43
EPOCHS = 20 # Number of epochs per general trial
NUM_TRIALS = 15
TEST_SIZE = 0.2 # Size of testing dataset

###############################################################################
#                              KERASTUNER OPTIMIZATION
###############################################################################

def build_model(hp):
    """ Returns a model chosen by KerasTuner based on search conditions """

    model = models.Sequential()

    # convolutional layers
    conv_l1_unit = hp.Int(f"conv_l1_units", 32, 128, 32)
    model.add(layers.Conv2D(conv_l1_unit, (3,3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    print(conv_l1_unit)
    
    conv_l2_unit = hp.Int(f"conv_l2_units", conv_l1_unit, 256, 32)
    model.add(layers.Conv2D(conv_l2_unit, (3,3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    
    # hidden layers
    model.add(layers.Flatten())
    hidden_start_unit = hp.Int("hidden_l1_unit", 32, 256, 32)
    for i in range(hp.Choice('num_hidden_layers', [1, 2, 3])):
        next_unit = np.ceil(hidden_start_unit / (2**i))
        model.add(layers.Dense(next_unit, activation='relu'))
        model.add(layers.Dropout(0.2))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
    
    model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adagrad(), metrics=["accuracy"])
    return model
    

def test_model(x_train, y_train, x_test, y_test):
    """ Test a specific neural network when not tuning hyperparameters """
    model = models.Sequential([
        layers.Conv2D(64, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adamax(), metrics=["accuracy"])
    model.fit(x_train, y_train, validation_split=0.2, epochs=EPOCHS)
    model.evaluate(x_test, y_test)
    return model

###############################################################################
#                              MAIN
###############################################################################

def main():
    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    images = tf.cast(images, tf.float32)
    labels = utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Tune convolutional neural network
    if IS_TUNING:
        tuner = kt.BayesianOptimization(
            build_model,
            objective='val_accuracy',
            max_trials=NUM_TRIALS,
            executions_per_trial=2,
            overwrite=False,
            directory='num_layers_and_units',
        )
        tuner.search(x_train, y_train, validation_split=0.2, epochs=EPOCHS)
        best_model = tuner.get_best_models()
        tuner.results_summary(num_trials=5)
    else:
        best_model = test_model(x_train, y_train, x_test, y_test)
    
    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        best_model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Loads image data from directory `data_dir`.
    Returns tuple `(images, labels)`
    * `images` is a list of all of the images in the data directory, where each image is formatted as a
    numpy array with dimensions IMG_WIDTH x IMG_HEIGHT x 3. 
    * `labels` is a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    for i in range(NUM_CATEGORIES):
        print(f"Loading images from folder {i}")
        dir_path = os.path.join(data_dir, str(i))
        j = 0
        for image in os.listdir(dir_path):
            img = cv2.imread(os.path.join(dir_path, image))
            res = cv2.resize(img, (IMG_HEIGHT,IMG_WIDTH), interpolation=cv2.INTER_AREA)
            images.append(res)
            labels.append(i)
            j += 1

    return images, labels

if __name__ == "__main__":
    main()
