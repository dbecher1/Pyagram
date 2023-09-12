import drawsvg as draw
import json
from configparser import ConfigParser
from node import *
from max_list import *

def Run() -> None:

    config = ConfigParser()
    config.read('config.ini')

    save_png = config.getboolean('SETTINGS', 'PNG')
    save_svg = config.getboolean('SETTINGS', 'SVG')
    draw_lines = config.getboolean('SETTINGS', 'lines')
    filename = config['SETTINGS']['Filename']
    header_text_size = config.getint('SETTINGS', 'HeaderTextSize')
    item_text_size = config.getint('SETTINGS', 'ItemTextSize')
    vbox_padding = config.getint('SETTINGS', 'VBoxPadding')
    hbox_padding = config.getint('SETTINGS', 'HBoxPadding')
    max_boxes = config.getint('SETTINGS', 'MaxBoxWidth')

    with open('diagram.json') as f:
        data = json.load(f)

    nodes = []

    for node in data:

        new_node = Node(node)

        children = data[node].get('Children')
        keys = data[node].get('Keys')
        relations = data[node].get('Relations')

        relations_temp = {}

        if children is not None:
            for child in children:
                is_key = False
                if keys is not None and child in keys:
                    is_key = True
                new_node.add_child(child, is_key)

        if relations is not None:
            for r in relations:
                relations_temp[r] = {}
                for r_ in relations[r]:
                    relations_temp[r] = {}
                    relations_temp[r][r_] = relations[r][r_]
                
        nodes.append(new_node)

    width = hbox_padding + item_text_size
    height = vbox_padding + item_text_size

    largest = Max_List(max_boxes)

    j = 0

    for n in nodes:
        n.calculate_dimensions(item_text_size, hbox_padding, vbox_padding)
        height += n.box_width
        largest.calculate(n.box_width)

    width += largest.sum()

    w_padding = width / len(nodes)
    h_padding = height / len(nodes)

    canvas_width = (width * 2) + w_padding
    canvas_height = (height * 2) + h_padding

    d = draw.Drawing(canvas_width, canvas_height)

    x_ = w_padding
    y_ = h_padding

    for n in nodes:
        r = draw.Rectangle(x=x_,y=y_, width=n.box_width, height=n.box_height)
        r.append_title(n.name)
        d.append(r)
        x_ += w_padding
        if x_ >= canvas_width:
            x_ = w_padding
            y_ += h_padding







    #d.save_svg('test.svg')
    if save_png: d.save_png('out/' + filename + '.png')
    if save_svg: d.save_svg('out/' + filename + '.svg')

if __name__ == '__main__':
    Run()