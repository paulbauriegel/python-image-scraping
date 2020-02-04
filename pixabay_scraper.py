import json
from pprint import pprint
import sys  # Importing the System Library
from os.path import isfile, join
from os import makedirs
import requests
import time


def download_image(folder_name, urlimg, number_trys=5, wait_seconds=5):
    filename = urlimg.rsplit('/', 1)[1]
    filename = join(folder_name, filename)
    makedirs(folder_name, exist_ok=True)
    if not isfile(filename):
        response = requests.get(urlimg, stream=True)
        trys = 0
        while response.status_code != 200 and trys < number_trys:
            time.sleep(wait_seconds)
            response = requests.get(urlimg, stream=True)
            print("try again", trys, urlimg)
            trys += 1
        if trys >= number_trys:
            print("could not download", urlimg)
            return False
        else:
            with open(filename, 'wb') as f:
                for chunk in response:
                    f.write(chunk)
    return True

API_KEY="define yourself"
p_name = "Display%2CPort"
url = "https://pixabay.com/api/?key=" + API_KEY + "&q=" + p_name + "&image_type=photo&pretty=true&per_page=200"
response = requests.get(url)
with open('pixabay.com.json', 'w') as f:
    f.write(response.text)

with open('pixabay.com.json') as data_file:
    data = json.load(data_file)
    for hello in data["hits"]:
        image = hello
        lal = hello
        imageuri = lal["previewURL"]
        imageuri = imageuri.replace(' ', '')[:-8].upper()
        temp = "_960_720.jpg"
        imageuri = imageuri+temp
        imageuri = imageuri.lower()
        print(imageuri)
        result = download_image(p_name, imageuri)
        if not result:
            print('Error', imageuri)

