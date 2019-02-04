# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 22:35:41 2019

@author: abhis
"""
import keras
from keras.models import Sequential
from keras.layers import Dense,Input,Flatten,Dropout,Conv2D,MaxPooling2D,GlobalAveragePooling2D,GlobalMaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix

import math

def bigger_conv_model(input_shape):
    model=Sequential()
    model.add(Conv2D(32,kernel_size=3,strides=2,padding='same',activation='relu',input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(32,kernel_size=3,strides=2,padding='same',activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(64,kernel_size=3,strides=2,padding='same',activation='relu'))
    model.add(GlobalAveragePooling2D())
    model.add(Dropout(0.4))
    model.add(Dense(64,activation='relu'))
    model.add(Dropout(0.4))
    
    model.add(Dense(1,activation='sigmoid'))
    return model


#model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
#model.load_weights("bigger_model_chcekpoint_weights.h5")

#modification
import os
os.environ['KERAS_BACKEND'] = 'theano'
import time
import h5py
import json
import requests
import numpy as np
from keras.models import model_from_json
from PIL import Image
from keras import backend as K

class Pred_hemo(object):
    
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/image/api'
        self.dirPath = '...'
    
    def load_train_model(self):
        os.chdir('....')
        '''
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        '''
        model=bigger_conv_model((128,128,3))
        model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
        model.load_weights("bigger_model_chcekpoint_weights.h5")
        print("Loaded model from disk")
        
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
            print("Unable to load image")


    def prediction(self):
        imfile = self.extractImage(self.dirPath)
        data=np.asarray(imfile, dtype="int32")
        # return json.dumps(data.shape)
        ynew = data.reshape(1,128,128,3)
        # Pred = model.predict(ynew)
        
        self.load_trained_model()
        self.predc = model.predict_classes(ynew)
        # return json.dumps({"ans" : self.predc})
        if self.predc == [0]:
            return "no"
        else:
            return "yes"