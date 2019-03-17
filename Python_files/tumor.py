# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 22:35:41 2019

@author: abhis
"""

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
from keras.models import load_model


class Pred_tumor(object):
    
    def __init__(self):
        self.model=None
        self.url = 'http://127.0.0.1:8000/image/api'
        self.dirPath = '/Users/aakashvarma/Documents/Coding/Med-I/backend/uploads'
        
    
    def load_train_model(self):
        os.chdir('/Users/aakashvarma/Documents/Coding/Med-I/python_files')
        
        self.model=load_model('mri_model_weights.h5')
        print("Loaded model from disk")
        
    def getData(self, link):
        response = requests.get(link)
        self.data = response.json()
        return self.data

    def extractImage(self,path):
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
        data = np.asarray(imfile.resize((128, 128), PIL.Image.ANTIALIAS))
        ynew = data.reshape(1,128,128,3)
        # Pred = model.predict(ynew)
        
        self.load_train_model()
        self.predc = self.model.predict_classes(ynew)
        
        if self.predc[0][0]==1:
            return "Tumor detected"
        else:
            return "Normal"