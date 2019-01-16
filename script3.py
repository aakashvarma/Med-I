# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:46:42 2019

@author: abhis
"""

import h5py
import cv2
import numpy as np
#from matplotlib import pyplot as plt
np.set_printoptions(threshold=np.nan)
 
files={}
array={}
cnt=0
for i in range(2299,3065):
    filepath=r"D:\\datasets\\brainTumorDataPublic_2299-3064\\"+str(i)+'.mat'
    f=h5py.File(filepath)
    x=f['cjdata']
    img=np.array(x['image'])
    array['label']=int(np.array(x['label'][0][0]))
    array['tumormask']=np.array(x['tumorMask'])
    if array['label']==1:
        cv2.imwrite(r"D:\\datasets\\L1\\"+'test'+str(i)+'.jpg',img)
    if array['label']==2:
        cv2.imwrite(r"D:\\datasets\\L2\\"+'test'+str(i)+'.jpg',img)
    if array['label']==3:
        cv2.imwrite(r"D:\\datasets\\L3\\"+'test'+str(i)+'.jpg',img)
    files[i]=array

     