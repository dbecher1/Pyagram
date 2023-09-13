
class Point:
    def __init__(self, x_, y_) -> None:
        self.x = x_
        self.y = y_

class Box:
    def __init__(self, x_ = 0, y_ = 0, w_ = 0, h_ = 0) -> None:
        self.x = x_
        self.y = y_
        self.w = w_
        self.h = h_

    def is_intersecting(self, x_, y_) -> bool:
        # returns true if a point is intersecting this box
        return x_ > self.x and y_ < self.y and x_ < (self.x + self.w) and y_ > (self.y + self.h)
    
    def point_is_intersecting(self, p:Point) -> bool:
        return self.is_intersecting(p.x, p.y)
    
class Line:
    def __init__(self, start_x, end_x, start_y, end_y) -> None:
        self.sx = start_x
        self.sy = start_y
        self.ex = end_x
        self.ey = end_y
        self.points_of_delta = {}
    

class Helper:
    # idk what to call this

    def __init__(self, width, height) -> None:
        # width and height of canvas
        self.quadtree = []
        self.lines = []
        self.collision_boxes = {}
        self.node_child_relations = {}

        half_w = width / 2
        half_h = height / 2

        b1 = Box(0, 0, half_w, half_h)
        b2 = Box(half_w, 0, half_w, half_h)
        b3 = Box(0, half_h, half_w, half_h)
        b4 = Box(half_w, half_h, half_w, half_h)

        self.quadtree.append(b1)
        self.quadtree.append(b2)
        self.quadtree.append(b3)
        self.quadtree.append(b4)

        self.collision_boxes[b1] = []
        self.collision_boxes[b2] = []
        self.collision_boxes[b3] = []
        self.collision_boxes[b4] = []

    def add_child(self, parent, child, x_, y_, w_, h_) -> None:

        if parent not in self.node_child_relations:
            self.node_child_relations[parent] = {}

        b = Box(x_, y_, w_, h_)

        self.node_child_relations[parent][child] = {}
        self.node_child_relations[parent][child]['box'] = b
        self.node_child_relations[parent][child]['relations'] = []

        for qt in self.quadtree:
            if qt.is_intersecting(b.x, b.y):
                self.collision_boxes[qt].append(b)

    def construct_graph(self, data:{}) -> None:

        for parent in self.node_child_relations:
            for child in self.node_child_relations[parent]:
                if parent in data and child in data[parent]:
                    rel = data[parent][child]

                    for r in rel:
                        # r is the name of the other parent
                        # rel[r] is the name of the other child
                        if r in self.node_child_relations and rel[r] in self.node_child_relations[r]:
                            other_child_data = self.node_child_relations[r][rel[r]]
                            self.node_child_relations[parent][child]['relations'].append(other_child_data['box'])

                        else:
                            print('something went wrong...')