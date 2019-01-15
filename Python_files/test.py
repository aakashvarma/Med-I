import os
os.environ['KERAS_BACKEND'] = 'theano'
import time
import h5py
import json
import requests
import numpy as np
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, MaxPooling2D, Dropout, Dense
from keras.models import model_from_json
from PIL import Image
from keras import backend as K




model = Sequential()
model.add(Conv2D(5, (40, 40), padding='same', activation='relu', input_shape=(176, 176, 1)))
model.add(Conv2D(3, (20, 20)))
model.add(Conv2D(3, (15, 15)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(20))
model.add(Dense(2, activation='softmax'))

class A(object):

    hf = h5py.File('dat.hdf5', 'r')
    X = hf.get('Images_2D')
    y = hf.get('Labels')
    X = np.array(X)
    y = np.array(y)
    hf.close()
    X = X[0:235, 16:192, 0:176]

    from keras.utils import to_categorical
    y = to_categorical(y)
    
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/image/api'
        self.dirPath = '/Users/aakashvarma/Documents/Coding/Med-I/Backend/uploads'

    def load_trained_model(self):
        os.chdir('/Users/aakashvarma/Documents/Coding/Med-I/Python_files')
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")



    # get data from the API
    def getData(self, link):
        response = requests.get(link)
        self.data = response.json()
        return self.data

    def extractImage(self, path):
        imgFilename= self.getData(self.url)['filename']
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


    def prediction(self):
        imfile = self.extractImage(self.dirPath)
        data=np.asarray(imfile, dtype="int32")
        # return json.dumps(data.shape)
        ynew = data.reshape(1,176,176,1)
        # Pred = model.predict(ynew)
        self.load_trained_model()
        self.predc = model.predict_classes(ynew)
        if self.predc == [0]:
            return "no"
        else:
            return "yes"






















