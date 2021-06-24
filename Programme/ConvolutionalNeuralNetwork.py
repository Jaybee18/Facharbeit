import os
from tkinter import messagebox, filedialog, Tk
import ast
import keras
from Nebenskripte.showimage import showImage
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from Nebenskripte.presentResults import Editor


def formatData(filename:str):
    file = open(filename+'.txt', 'r')
    content:str = file.readline()
    file.close()
    images, labels = list(map(ast.literal_eval, content.split(';')))

    # grayscale images first
    images = convertAllImagesToGrayScale(images)
    return images, labels

if __name__ == '__main__':
    # load the data-sets
    (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

    # Normalize pixel values to be between 0 and 1
    train_images, test_images = train_images / 255.0, test_images / 255.0

    # ask the user if he wants to load a pre-trained model
    root = Tk()
    root.withdraw()
    load_model = messagebox.askyesno("Model", "Load a pretrained model?")
    model = None
    if load_model:
        # load a pre-trained model
        model = models.load_model(filedialog.askdirectory(initialdir = os.curdir, title="Select a Model"))
    else:
        # create the model
        model = models.Sequential([
            layers.Conv2D( 32, (3, 3), activation="relu", padding="same", input_shape=(32, 32, 3) ),
            layers.BatchNormalization(),
            layers.Conv2D( 32, (3, 3), activation="relu", padding="same" ),
            layers.BatchNormalization(),
            layers.MaxPooling2D( (2, 2), strides=2 ),
            layers.SpatialDropout2D( 0.1 ),

            layers.Conv2D( 64, (3, 3), activation="relu", padding="same" ),
            layers.BatchNormalization(),
            layers.Conv2D( 64, (3, 3), activation="relu", padding="same" ),
            layers.BatchNormalization(),
            layers.MaxPooling2D( (2, 2), strides=2 ),
            layers.SpatialDropout2D( 0.1 ),

            layers.Flatten(),
            layers.Dense( 256, activation='relu' ),
            layers.Dropout( 0.5 ),
            layers.Dense( 10 , activation='softmax')
        ])

        # configure the model for training
        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        # train the model on the training data-set
        # and validate it with the testing data-set
        model.fit( train_images, train_labels, epochs=20,
                             validation_data=(test_images, test_labels))

    # make predictions for every testing image
    predictions = model.predict( test_images ).tolist()

    # present the results with the Editor
    class_names = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
    e = Editor()
    for i in range( len( predictions ) ):
        output = class_names[ predictions[ i ].index( max( predictions[ i ] ) ) ]
        actual_label = class_names[test_labels[ i ][0]]
        info = f"Actual Label : {actual_label}\nPredicted Label : {output}"
        
        e.newEntry( f"#{i} {str(actual_label)}       // {output}", test_images[ i ], info, actual_label == output )
    e.mainloop()
    exit()