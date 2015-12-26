from wand.image import Image
import numpy as np

pixels = []
image = Image(filename="mazes/easy2.png")
#image = Image(filename="mazes/mazewhite.png")
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

import search

start = (340, 33)
end = (215, 365 )
start_id = graph.pixel_to_node(start).id
end_id = graph.pixel_to_node(end).id

cost, path = search.min_path2(graph, start_id, end_id)


# EASY 400X400 MAZE
# start = (340, 33)
# end = (215, 367)

# path is a list of nodes

def pixels_to_highlight(graph, path):
    all_pixels = set()
    for node_id in path:
        node = graph.node(node_id)
        pixels = set(node.pixels)
        all_pixels |= pixels
    return all_pixels

from wand.drawing import Drawing
from wand.color import Color

pth = pixels_to_highlight(graph, path)
with Drawing() as draw:
    draw.fill_color=Color("red")
    for pixel in pth:
        draw.point(pixel[1], pixel[0])
    draw(image)
    image.save(filename="mazes/easy-solved.png")
