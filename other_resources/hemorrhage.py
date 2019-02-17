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
import PIL
from PIL import Image
from keras import backend as K
#import cv2

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




class Pred_hemo(object):
    
    def __init__(self):
        self.model=bigger_conv_model((128,128,3))
        self.url = 'http://127.0.0.1:8000/image/api'
        self.dirPath = 'image file directory.....'
        
    
    def load_train_model(self):
        os.chdir('.py file directory....')
        
        self.model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
        self.model.load_weights("bigger_model_chcekpoint_weights.h5")
        print("Loaded model from disk")
        
    def getData(self, link):
        response = requests.get(link)
        self.data = response.json()
        return self.data

    def extractImage(self,path):
        # imgFilename= self.getData(self.url)['filename']

        imgData = self.getData(self.url)
        imgFilename = imgData["imagedata"]["filename"]

        os.chdir(path)
        try:
            #img = Image.open(imgFilename)
           
           
            #img=cv2.imread('028.png')
            #imfile=img
            imfile=Image.open(imgFilename)
            return imfile
        except:
            print("Unable to load image")


    def prediction(self):
        imfile = self.extractImage(self.dirPath)
        #imfile = self.extractImage()
        #data=np.asarray(cv2.resize(imfile,(128,128)))
        data = np.asarray(imfile.resize((128, 128), PIL.Image.ANTIALIAS))
        ynew = data.reshape(1,128,128,3)
        # Pred = model.predict(ynew)
        
        self.load_train_model()
        self.predc = self.model.predict_classes(ynew)
        # return json.dumps({"ans" : self.predc})
        if self.predc == [0]:
            return "no"
        else:
            return "yes"
