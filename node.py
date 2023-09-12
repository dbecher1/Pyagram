
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
        self.box_width = 0
        for c in self.children:
            length = len(c)
            w = (length * 0.8) * (text_size * 1.1)
            self.item_boxes[c] = w
            self.box_width += w + h_padding
        self.box_height = text_size + v_padding

if __name__ == '__main__':
    pass