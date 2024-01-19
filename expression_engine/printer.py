from expression_engine.nodes import Node


class Printer:
    def __init__(self, n: Node):
        self._n = n

    def _print_node(self, el: Node, is_last: bool = True, header: str = ''):
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        connector = elbow if is_last else tee
        print(header + connector + el.name)
        if el.children:
            children = el.children
            for index, child in enumerate(children):
                tail = blank if is_last else pipe
                h = header + tail
                new_is_last = index == len(children) - 1
                self._print_node(child, header=h, is_last=new_is_last)

    @staticmethod
    def print(n: Node):
        p = Printer(n)
        return p._print_node(n)
