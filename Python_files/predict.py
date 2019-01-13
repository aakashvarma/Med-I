# 200 -- everything went okay, and the result has been returned (if any)
# 301 -- the server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.
# 401 -- the server thinks you're not authenticated. This happens when you don't send the right credentials to access an API (we'll talk about authentication in a later post).
# 400 -- the server thinks you made a bad request. This can happen when you don't send along the right data, among other things.
# 403 -- the resource you're trying to access is forbidden -- you don't have the right permissions to see it.
# 404 -- the resource you tried to access wasn't found on the server.

import os
import h5py
import json
import requests
import numpy as np
from matplotlib import pyplot
from keras.models import  Sequential
from keras.layers import Conv2D, Flatten, MaxPooling2D, Dropout, Dense
from keras.models import model_from_json
from PIL import Image

url = 'http://127.0.0.1:8000/image/api'
dirPath = '/Users/aakashvarma/Documents/Coding/Med-I/uploads'

hf = h5py.File('dat.hdf5', 'r')
X = hf.get('Images_2D')
y = hf.get('Labels')
X = np.array(X)
y = np.array(y)
hf.close()
X = X[0:235, 16:192, 0:176]

from keras.utils import to_categorical
y = to_categorical(y)


def model(input_shape = (176, 176, 1)):
    layers = Sequential()
    layers.add(Conv2D(5, (40, 40), padding='same', activation='relu', input_shape=input_shape))
    layers.add(Conv2D(3, (20, 20)))
    layers.add(Conv2D(3, (15, 15)))
    layers.add(MaxPooling2D(pool_size=(2, 2)))
    layers.add(Dropout(0.25))
    layers.add(Flatten())
    layers.add(Dense(20))
    layers.add(Dense(2, activation='softmax'))
    return layers


model = model()

def load_trained_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

load_trained_model()


# get data from the API
def getData(link):
    response = requests.get(link)
    data = response.json()
    return data['filename']

def extractImage(path):
    imgFilename= getData(url)
    os.chdir(path)
    try:
        img = Image.open(imgFilename)
        img.load()
        gray = img.convert('L')
        bw = np.asarray(gray).copy()
        bw[bw<128] = 0
        bw[bw>=128] = 255
        imfile = Image.fromarray(bw)
        return imfile
    except:
        print "Unable to load image"


def prediction():
    imfile = extractImage(dirPath)
    data=np.asarray(imfile, dtype="int32")
    # print data.shape
    ynew = data.reshape(1,176,176,1)
    Pred = model.predict(ynew)
    predc = model.predict_classes(ynew)
    print predc

prediction()
# 



# 







