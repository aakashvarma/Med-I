import requests
import json

link = "http://127.0.0.1:8000/image/api"

response = requests.get(link)
data = response.json()
# jsondata = json.load(data)

print data["imagedata"]["filename"]


















