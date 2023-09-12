
class Node:
    def __init__(self, node_name:str) -> None:
        self.children = {} # maps children to a bool if they are a key or not
        self.relations = {}
        self.item_boxes = {} # maps children names to box width
        self.box_width = 0 # total box width
        self.box_height = 0
        self.name = node_name

    def add_child(self, child:str, key:bool) -> None:
        self.children[child] = key

    def __repr__(self) -> str:
        # quick and dirty just for debug
        out = ""
        for c in self.children:
            out += c + "\n"
        for r in self.relations:
            out += r + ': '
            for r_ in r:
                out += r_
        return out
    
    def calculate_dimensions(self, text_size:int = 8, h_padding:int = 0, v_padding:int = 0) -> None:
        for c in self.children:
            length = len(c)
            self.item_boxes[c] = (length * text_size * 0.5) + h_padding
        self.box_height = text_size + v_padding
        self.box_width = h_padding
        for i in self.item_boxes.values():
            self.box_width += i

if __name__ == '__main__':
    pass