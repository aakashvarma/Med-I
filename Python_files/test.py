import train

getdata = train.getScalledData([[0.0, 76.0, 16.0, 3.0, 26.0, 1391.0, 0.705, 1.262]])
print train.predict(getdata)[0]