from typing import List
from random import randrange

class Point:
    def __init__(self, x_ = 0, y_ = 0) -> None:
        self.x = x_
        self.y = y_

    def __eq__(self, other) -> bool:
        epsilon = 1
        return (abs(self.x - other.x) <= epsilon) and (abs(self.y - other.y) <= epsilon)
    
    def __repr__(self) -> str:
        return 'X: ' + str(self.x) + ' Y: ' + str(self.y)

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
    def __init__(self, sx, sy, ex, ey) -> None:
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.points_of_delta = {}

    def __repr__(self) -> str:
        s = 'Line:\n'
        s += 'start: '
        s += str(self.sx) + ' ' + str(self.sy) + '\n'
        s += 'end: '
        s += str(self.ex) + ' ' + str(self.ey) + '\n'
        return s
    
def epsilon_equals(lhs:float, rhs:float, epsilon:float = 0.1) -> bool:
    return abs(lhs - rhs) <= epsilon

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class Helper(object):
    # idk what to call this

    def __init__(self, width, height) -> None:
        # width and height of canvas
        self.quadtree = []
        self.lines = []
        self.collision_boxes = {}
        self.node_child_relations = {}

        self.width = width
        self.height = height

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

        self.manual_offset = 0

    def __enter__ (self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass

    def add_child(self, parent, child, x_, y_, w_, h_) -> None:

        if parent not in self.node_child_relations:
            self.node_child_relations[parent] = {}

        # b = Box(x_, y_, x_ + w_, y_ + h_)
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
                        # rel is the name of the other parent
                        # r the name of the other child
                        # rel[r] is the data
                        if r in self.node_child_relations and rel[r] in self.node_child_relations[r]:
                            other_child_data = self.node_child_relations[r][rel[r]]
                            self.node_child_relations[parent][child]['relations'].append(other_child_data['box'])

                        else:
                            print('something went wrong...')

    def construct_lines_test(self) -> None:

        for p in self.node_child_relations:
            for c in self.node_child_relations[p]:

                b = self.node_child_relations[p][c]['box']

                for r in self.node_child_relations[p][c]['relations']:
                    line = Line(sx=b.x, sy=b.y, ex=r.x, ey=r.y)
                    self.lines.append(line)

    def construct_lines(self) -> None:

        for p in self.node_child_relations:
            for c in self.node_child_relations[p]:

                b = self.node_child_relations[p][c]['box']

                for r in self.node_child_relations[p][c]['relations']:
                    line = Line(sx=b.x + (b.w * 0.5), sy=b.y, ex=r.x, ey=r.y)
                    self.lines.append(line)

    def draw_lines_helper(self, start:Point, end:Point, first:bool=False) -> List[Line]:
        
        if start == end: return []

        resolution = 8
        
        step_size_x = int(self.width / resolution) # tinker with these
        step_size_y = int(self.height / resolution)

        # a value -1 or 1, up or down respectively
        if not epsilon_equals(start.y, end.y):
            direction_y = (start.y - end.y) / abs(start.y - end.y)
        elif first:
            # the hedge case where they're on the same row and it's the first pass
            direction_y = -1

        if not epsilon_equals(start.x, end.x):
            # a value -1 or 1, left or right respectively
            direction_x = (start.x - end.x) / abs(start.x - end.x)

        dx = start.x - end.x # distance from where we are to the goal

        if abs(dx) > step_size_x:
            # clamp to step size if the distance is larger
            dx = step_size_x * direction_x

        dx *= -1 # reverse direction of distance

        dy = start.y - end.y # vertical distance
        # positive if box is above, negative if below

        if abs(dy) > step_size_y:
            # clamp
            dy = step_size_y * direction_y
        dy *= -1 # same as above

        # TODO gotta do collision

        # for this step of the recursion only move toward the further value
        start_x = start.x
        if first:
            # quick and dirty
            r1 = randrange(-5, 5)
            if r1 == 0:
                r1 = 1
            r2 = randrange(-3, 3)
            r3 = randrange(-10, 10)
            dy = (r1 + step_size_y) * -(direction_y) + r2
            dx = 0
            start_x += r3
        else:
            if epsilon_equals(dx, 0) or epsilon_equals(dy, 0):
                pass
            if abs(dx) > abs(dy):
               
               dy = 0
            else:
                
                if epsilon_equals(start_x, dx):
                    dy = 0
                else:
                    
                    dx = 0

        new_end_x = start_x + dx
        new_end_y = start.y + dy

        return [Line(start_x, start.y, new_end_x, new_end_y)] + self.draw_lines_helper(Point(new_end_x, new_end_y), end)

    def generate_lines(self) -> List[List[Line]]:
        lines = []
        for p in self.node_child_relations:
            for c in self.node_child_relations[p]:

                b = self.node_child_relations[p][c]['box']
                # b is the start
                y_ = 5 # dummy value

                for r in self.node_child_relations[p][c]['relations']:

                    goal_x = r.x + (r.w * 0.5) + self.manual_offset
                    start_x = b.x + (b.w * 0.5) + self.manual_offset

                    dy = b.y - r.y
                    # negative: r is above

                    if dy > 0:
                        start_y = b.y
                        goal_y = r.y + r.h
                    elif dy < 0:
                        start_y = b.y + b.h
                        goal_y = r.y
                    else:
                        if b.y < (self.height * 0.5):
                            start_y = b.y + b.h
                            goal_y = r.y + r.h
                        else:
                            start_y = b.y
                            goal_y = r.y

                    if b.y == r.y:
                        # if on the same row
                        test = [Line(start_x, start_y, start_x, start_y + y_)]
                    else:
                        test = []

                    lines.append(self.draw_lines_helper(Point(start_x, start_y), Point(goal_x, goal_y), True))
        return lines

                    
