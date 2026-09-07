from PIL import Image, ImageDraw
import numpy as np
Size = 60
img = Image.new("RGB", (Size,Size), color=(20,20,20))
draw = ImageDraw.Draw(img)
draw.ellipse([5,15,30,40], fill=(60,90,200))
draw.rectangle([35,10,55,50], fill=(220,130,40))
img.save("imagenprueba.png")
print("imagen guardad")