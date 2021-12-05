from typing import List


class Node:
    def __init__(self, row, column, parent) -> None:
        self.row = row
        self.column = column
        self.parent = parent


class Graph:
    def __init__(self, rows, columns) -> None:
        self.nodes = List[List[Node]]
        for row in range(rows):
            list_nodes = []
            for column in range(columns):
                list_nodes.append(Node(row=row, column=column, parent=self))
            self.nodes.append(list_nodes)

    def get_neighbours(self, current_node: Node):
        row = current_node.row
        column = current_node.column
        list_neighbours = []
