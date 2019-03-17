# -*- coding: utf-8 -*-


#from keras.models import Sequential
import numpy as np
from keras.models import load_model
from keras.preprocessing import image


# returns a compiled model
# identical to the previous one
classifier1 = load_model('mri_model_weights.h5')

#Image index i
i = 4

#Predicting the Dogs dataset
image_name = 'tumor.'+str(i)+'.jpg'
#file_name = 'D:/datasets/brain_MRI_CNN-master/dataset/test_set/tumor/tumor.'+str(i)+'.jpg'
file_name = 'D:/datasets/brain_MRI_CNN-master/tumor/samples/s.'+str(i)+'.jpg'
test_image = image.load_img(file_name, target_size = (128, 128))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
#result = classifier1.predict(test_image)
result = classifier1.predict_classes(test_image)


if result[0][0] == 1:
     print('Model prediction for image '+image_name+':  TUMOR')
else:
     print('Model prediction for image '+image_name+':   NORMAL')
