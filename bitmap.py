from wand.image import Image
import numpy as np

pixels = []
image = Image(filename="mazes/mazewhite.png")
width, height = image.width, image.height
blob = image.make_blob(format='gray')

pixels = map(ord, blob)
array = np.array(pixels)
array = array.reshape(width, height)


# import gridlines
# gd = gridlines.GridlineDetector(array)
# print gd.detect_gridlines()

import dotgraph
dg = dotgraph.DotDetector(array)
graph = dg.generate_graph()
