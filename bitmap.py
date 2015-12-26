from wand.image import Image
import numpy as np
import dotgraph
from wand.drawing import Drawing
from wand.color import Color

import search

def pixels_to_highlight(graph, path):
    all_pixels = set()
    for node_id in path:
        node = graph.node(node_id)
        pixels = set(node.pixels)
        all_pixels |= pixels
    return all_pixels

def pixels_to_highlight2(graph, path):
    all_pixels = set()
    for node_id in path:
        node = graph.node(node_id)
        pixels = set(node.pixels)
        all_pixels |= pixels

        # find all *white* neighbors of these pixels
        # and color them too
        neighbors = node.get_neighbors()
        for neighbor in neighbors:
            _r, _c = neighbor
            if dotgraph.DotDetector._pixel_is_white(node.graph.array[_r][_c]):
                all_pixels.add(neighbor)

    return all_pixels

def easy_maze():
    pixels = []
    image = Image(filename="mazes/easy2.png")
    #image = Image(filename="mazes/mazewhite.png")
    width, height = image.width, image.height
    blob = image.make_blob(format='gray')

    pixels = map(ord, blob)
    array = np.array(pixels)
    array = array.reshape(height, width)


    dg = dotgraph.DotDetector(array)
    graph = dg.generate_graph()

    start = (340, 33)
    end = (215, 365 )
    start_id = graph.pixel_to_node(start).id
    end_id = graph.pixel_to_node(end).id

    cost, path = search.min_path2(graph, start_id, end_id)

    pth = pixels_to_highlight(graph, path)
    with Drawing() as draw:
        draw.fill_color=Color("red")
        for pixel in pth:
            draw.point(pixel[1], pixel[0])
        draw(image)
        image.save(filename="mazes/easy-solved.png")

def hard_maze():
    pixels = []
    image = Image(filename="mazes/mazewhite.png")
    #image = Image(filename="mazes/mazewhite.png")
    width, height = image.width, image.height
    blob = image.make_blob(format='gray')

    pixels = map(ord, blob)
    array = np.array(pixels)
    array = array.reshape(height, width)


    dg = dotgraph.DotDetector(array)
    graph = dg.generate_graph()

    start = (34, 821)
    end = (2065, 849)

    start_id = graph.pixel_to_node(start).id
    end_id = graph.pixel_to_node(end).id

    cost, path = search.min_path2(graph, start_id, end_id)

    pth = pixels_to_highlight2(graph, path)
    with Drawing() as draw:
        draw.fill_color=Color("red")
        for pixel in pth:
            draw.point(pixel[1], pixel[0])
        draw(image)
        image.save(filename="mazes/hard-solved.png")








