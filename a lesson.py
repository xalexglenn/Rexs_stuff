import PIL
from PIL import Image
from PIL import ImageDraw
import arcade
tileset = Image.open("img/nature-paltformer-tileset-16x16.png")

tile1 = tileset.crop((6*16, 1*16, 6*16+16, 1*16+16))
tile1.save("img/buttback.png")
x=6
y=1
tile2 = Image.new("RGB", (16, 16), color=(0, 102, 0))
tile2.save("img/grass.png")