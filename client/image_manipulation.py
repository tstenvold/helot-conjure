from PIL import Image
import urllib.request
from io import BytesIO

urllib.request.urlretrieve(
    "https://opensource.com/sites/default/files/images/jupyter-image_7_0.png", "deer.jpg")

img = Image.open("deer.jpg")
result = img.rotate(90)
