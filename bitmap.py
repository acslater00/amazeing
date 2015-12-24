from wand.image import Image
import numpy as np

pixels = []
image = Image(filename="mazes/easy2.png")
width, height = image.width, image.height
blob = image.make_blob(format='gray')

pixels = map(ord, blob)
array = np.array(pixels)
array = array.reshape(width, height)