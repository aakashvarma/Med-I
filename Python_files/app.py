
# 200 -- everything went okay, and the result has been returned (if any)
# 301 -- the server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.
# 401 -- the server thinks you're not authenticated. This happens when you don't send the right credentials to access an API (we'll talk about authentication in a later post).
# 400 -- the server thinks you made a bad request. This can happen when you don't send along the right data, among other things.
# 403 -- the resource you're trying to access is forbidden -- you don't have the right permissions to see it.
# 404 -- the resource you tried to access wasn't found on the server.


from alzheimers import Predict_alhzeimer
from hemorrhage import Pred_hemo
from tumor import Pred_tumor
import train

from flask import Flask
import json
import requests

app = Flask(__name__)

@app.route("/")
    

def hello():
    response = requests.get('http://127.0.0.1:8000/image/api')
    imgData = response.json()
    imgScanType = imgData["rawdata"]["scan"]

    try:
        age = imgData["rawdata"]["age"]
        if (imgData["rawdata"]["gender"] == 'm'):
            gender = 1.0
        else: 
            gender = 0.0
        educ = imgData["rawdata"]["educ"]
        ses = imgData["rawdata"]["ses"]
        mmse = imgData["rawdata"]["mmse"]
        etiv = imgData["rawdata"]["etiv"]
        nebv = imgData["rawdata"]["nebv"]
        asf = imgData["rawdata"]["asf"]

    # [0.0, 76.0, 16.0, 3.0, 26.0, 1391.0, 0.705, 1.262]

        getdata = train.getScalledData([[gender, age, educ, ses, mmse, etiv, nebv, asf]])
        ea_prediction = train.predict(getdata)[0]
    except:
        ea_prediction = 'none'

    if imgScanType == 'mri':
        try:
            obj = Predict_alhzeimer()
            return json.dumps({
                "image_data" : obj.getData(obj.url),
                "prediction" : obj.prediction(),
                "ea_prediction" : ea_prediction
            })
        except:
            obj=Pred_tumor()
            return json.dumps({
                "image_data":obj.getData(obj.url),
                "prediction":obj.prediction(),
                "ea_prediction" : ea_prediction
            })
    elif imgScanType == 'ct':
        obj = Pred_hemo()
        return json.dumps({
            "image_data":obj.getData(obj.url),
            "prediction":obj.prediction(),
            "ea_prediction" : ea_prediction
        })
    else:
        print "error"


if __name__ == '__main__':
    app.run(debug=True)


