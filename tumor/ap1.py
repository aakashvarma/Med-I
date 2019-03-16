# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:36:13 2019

@author: abhis
"""
from tumor import Pred_tumor
from flask import Flask
import json

app=Flask(__name__)

@app.route("/")
def hello():
    obj=Pred_tumor()
    
    return json.dumps({"image_data":obj.getData(obj.dirPath),"prediction":obj.prediction()})

if __name__=='__main__':
    #hel=hello()
    #print(hel)
    app.run(debug=True)