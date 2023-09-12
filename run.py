import drawsvg as draw
import json
from configparser import ConfigParser
from node import *
from max_list import *

def Run() -> None:

    config = ConfigParser()
    config.read('config.ini')

    save_png = config.getboolean('SETTINGS', 'PNG')
    alpha_bg = config.getboolean('SETTINGS', 'AlphaBG')
    bg = config['SETTINGS']['BGColor']
    bg_color = bg.lower()
    save_svg = config.getboolean('SETTINGS', 'SVG')
    draw_lines = config.getboolean('SETTINGS', 'lines')
    filename = config['SETTINGS']['Filename']
    header_text_size = config.getint('SETTINGS', 'HeaderTextSize')
    item_text_size = config.getint('SETTINGS', 'ItemTextSize')
    vbox_padding = config.getint('SETTINGS', 'VBoxPadding')
    hbox_padding = config.getint('SETTINGS', 'HBoxPadding')
    max_boxes = config.getint('SETTINGS', 'MaxBoxWidth')

    with open(filename + '.json') as f:
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

    for n in nodes:
        n.calculate_dimensions(item_text_size, hbox_padding, vbox_padding)
        height += n.box_width * 0.3
        largest.calculate(n.box_width)

    width += largest.sum()

    w_padding = (width / len(nodes)) * 0.5 # these are for the boxes on the canvas
    h_padding = (height / len(nodes)) # the other similar variable is for interior text

    canvas_width = (width) + w_padding
    canvas_height = (height) + h_padding

    d = draw.Drawing(canvas_width, canvas_height)
    if not alpha_bg:
        d.append(draw.Rectangle(0, 0, canvas_width, canvas_height, fill=bg_color))

    x_ = w_padding
    y_ = h_padding

    ## THIS IS THE DRAWING ##

    for n in nodes:
        r = draw.Rectangle(x=x_,y=y_, width=n.box_width, height=n.box_height, fill='none', stroke='black')

        d.append(r)
        d.append(draw.Text(n.name, font_size=header_text_size, x=x_ + n.box_width, y=y_ - 2, font_weight='bold', text_anchor='end'))

        # Draw inner boxes
        x2 = x_
        for c in n.children:
            underline = ''
            if n.children[c]: # if is key
                underline = 'underline'
            width = n.item_boxes[c]

            t = draw.Text(
                text=c,
                font_size=item_text_size,
                dominant_baseline='middle',
                text_decoration=underline,
                x=x2 + hbox_padding,
                y=y_ + (0.5 * n.box_height)
                    )
            l = draw.Line(
                sx=x2+width,
                ex=x2+width,
                sy=y_,
                ey=n.box_height,
                stroke='black'
            )
            d.append(t)
            d.append(l)
            x2 += width + hbox_padding * 2

        # Move coordinates
        x_ += w_padding + n.box_width
        if x_ + n.box_width >= canvas_width:
            x_ = w_padding
            y_ += h_padding * 3


    ## END DRAWING ##

    d.set_pixel_scale(2)
    if save_png: d.save_png('out/' + filename + '.png')
    if save_svg: d.save_svg('out/' + filename + '.svg')

if __name__ == '__main__':
    Run()