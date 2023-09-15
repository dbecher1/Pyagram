import drawsvg as draw
import json
from configparser import ConfigParser
from node import *
from max_list import *
from helper import *

def Run() -> None:

    ## LOAD CONFIG ##

    config = ConfigParser()
    config.read('config.ini')

    save_png = config.getboolean('SETTINGS', 'PNG')
    alpha_bg = config.getboolean('SETTINGS', 'AlphaBG')
    bg = config['SETTINGS']['BGColor']
    bg_color = bg.lower()
    save_svg = config.getboolean('SETTINGS', 'SVG')
    draw_lines = config.getboolean('SETTINGS', 'lines')
    filename = config['SETTINGS']['Filename']
    header_text_size = config.getfloat('SETTINGS', 'HeaderTextSize')
    item_text_size = config.getint('SETTINGS', 'ItemTextSize')
    vbox_padding = config.getint('SETTINGS', 'VBoxPadding')
    hbox_padding = config.getint('SETTINGS', 'HBoxPadding')
    max_boxes = config.getint('SETTINGS', 'MaxBoxWidth')
    box_spacing_modifier = config.getfloat('SETTINGS', 'BoxSpacingModifier')
    final_scaling = config.getfloat('SETTINGS', 'Scale')

    ## END CONFIG ##

    ## PARSE JSON ##

    with open(filename + '.json') as f:
        data = json.load(f)

    nodes = []
    relations_temp = {}

    for node in data:

        new_node = Node(node)

        children = data[node].get('Children')
        keys = data[node].get('Keys')
        relations = data[node].get('Relations')

        if children is not None:
            for child in children:
                is_key = False
                if keys is not None and child in keys:
                    is_key = True
                new_node.add_child(child, is_key)

        if relations is not None:
            relations_temp[node] = {}
            for r in relations:
                relations_temp[node][r] = {}
                for r_ in relations[r]:
                    relations_temp[node][r][r_] = relations[r][r_]
                
        #print(relations_temp)

        nodes.append(new_node)

    ## END JSON ##

    width = 0
    height = 0

    largest = Max_List(max_boxes)

    for n in nodes:
        n.calculate_dimensions(item_text_size, hbox_padding, vbox_padding)
        height += n.box_width * 0.3
        largest.calculate(n.box_width)

    width += largest.sum()

    w_padding = (width / len(nodes)) * 0.3 # these are for the boxes on the canvas
    h_padding = (height / len(nodes)) * 0.9 # the other similar variable is for interior text

    canvas_width = width
    canvas_height = height

    d = draw.Drawing(canvas_width, canvas_height)
    if not alpha_bg:
        d.append(draw.Rectangle(0, 0, canvas_width, canvas_height, fill=bg_color))

    x_ = w_padding
    y_ = h_padding

    helper = Helper(canvas_width, canvas_height)

    ## DRAWING ##

    for n in nodes:

        r = draw.Rectangle(
            x=x_,
            y=y_,
            width=n.box_width,
            height=n.box_height,
            fill='none',
            stroke='black'
            )

        title = draw.Text(
            n.name,
            font_size=header_text_size,
            x=x_ + n.box_width,
            y=y_ - 2,
            font_weight='bold',
            text_anchor='end'
            )

        d.append(r)
        d.append(title)

        # Draw inner boxes
        x2 = x_
        for c in n.children:

            underline = 'none'
            if n.children[c]: # if this element is key
                underline = 'underline'
            box_width = n.item_boxes[c]
            box_height = n.box_height

            # pause the drawing, lets do some math

            helper.add_child(n.name, c, x_, y_, box_width, box_height)

            # resume drawing

            t = draw.Text(
                text=c,
                font_size=item_text_size,
                dominant_baseline='middle',
                text_anchor='middle',
                text_decoration=underline,
                x=x2 + (box_width * 0.5),
                y=y_ + (0.5 * n.box_height)
                    )
            
            l = draw.Line(
                sx=x2+box_width+hbox_padding,
                ex=x2+box_width+hbox_padding,
                sy=y_,
                ey=y_ + n.box_height,
                stroke='black',
                stroke_width=1
            )
            d.append(t)
            d.append(l)
            x2 += box_width + hbox_padding

        # Move coordinates
        x_ += w_padding + n.box_width
        if x_ + n.box_width >= canvas_width - w_padding:
            x_ = w_padding
            y_ += h_padding * box_spacing_modifier


    ## END DRAWING ##

    # more math
    helper.construct_graph(relations_temp)

    # TODO: colors
    colors = ['blue', 'green', 'red', 'pink', 'purple', 'orange', 'darkcyan']
    c = 0

    lines = helper.generate_lines()

    for line in lines:

        end_point = Point()
        for segment in line:

            line = draw.Line(sx=segment.sx, sy=segment.sy, ex=segment.ex, ey=segment.ey,stroke=colors[c], stroke_width=0.5)
            d.append(line)
            if segment is not None:
                end_point.x = segment.ex
                end_point.y = segment.ey

        test = 10
        # TODO: Arrows

        #d.append(Line(end_point.x, end_point.y, end_point.x - test, end_point.y - test))
        #d.append(Line(end_point.x, end_point.y, end_point.x + test, end_point.y - test))
        #d.append(line)
        #d.append(p)

        c += 1
        if c >= len(colors):
            c = 0

    d.set_pixel_scale(final_scaling)
    if save_png: d.save_png('out/' + filename + '.png')
    if save_svg: d.save_svg('out/' + filename + '.svg')

if __name__ == '__main__':
    Run()