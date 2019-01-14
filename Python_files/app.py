from test import A
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    obj = A()
    return obj.prediction()


if __name__ == '__main__':
    app.run(debug=True)


