from nodes import Node
from parser import Parser


class Printer:
    def __init__(self, n: Node):
        self.__n = n

    def __print_node(self, el: Node, is_last: bool = True, header: str = ''):
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        connector = elbow if is_last else tee
        print(header + connector + el.name)
        if el.has_children:
            children = el.get_children()
            for index, child in enumerate(children):
                tail = blank if is_last else pipe
                h = header + tail
                new_is_last = index == len(children) - 1
                self.__print_node(child, header=h, is_last=new_is_last)

    def print(self):
        return self.__print_node(self.__n)

