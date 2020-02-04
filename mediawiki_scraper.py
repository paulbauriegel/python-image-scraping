from mediawiki import MediaWiki
from PIL import Image, ExifTags
import requests
from os.path import isfile,join
from os import makedirs
import time

show_img = False

wikipedia = MediaWiki()
pages = wikipedia.search('hd,i')
pages = [p_name for p_name in pages if not p_name.endswith('(disambiguation)')]

for p_name in pages:
    p = wikipedia.page(p_name)
    images = p.images

    for urlimg in images:
        if any([urlimg.lower().endswith(p) for p in ['svg', 'ogg', 'ogv']]):
            continue # cannot identify image file <_io.BytesIO object at 0x0000012E68413EB8>
        try:
            filename = urlimg.rsplit('/', 1)[1]
            filename = join(p_name, filename)
            makedirs(p_name, exist_ok=True) 
            if not isfile(filename):
                response = requests.get(urlimg, stream=True)
                trys = 0
                while response.status_code != 200 and trys < 5:
                    time.sleep(2)
                    response = requests.get(urlimg, stream=True)
                    print("try again", urlimg)
                if trys == 5:
                    print("could not download", urlimg)
                    continue
                else:
                    with open(filename, 'wb') as f:
                        for chunk in response:
                            f.write(chunk)
            
            img = Image.open(filename)
            if img.format not in ['PNG']:
                if img.format not in ['GIF'] and img._getexif():
                    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
                if show_img:
                    img.show()
        except OSError as ex:
            print(ex)
            print(urlimg)
