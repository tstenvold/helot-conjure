from PIL import Image
import urllib.request
from io import BytesIO

urlobj = urllib.request.urlopen(
    "https://opensource.com/sites/default/files/images/jupyter-image_7_0.png")

img = Image.open(urlobj)
result = img.rotate(90)
