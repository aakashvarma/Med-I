from test import A
from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def hello():
    obj = A()
    return json.dumps({
        "image_data" : obj.getData(obj.url),
        "prediction" : obj.prediction()
    })

if __name__ == '__main__':
    app.run(debug=True)


