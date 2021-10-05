
urlobj = request.urlopen(
    "https://opensource.com/sites/default/files/images/jupyter-image_7_0.png")

img = Image.open(urlobj)
result = img.rotate(90)
