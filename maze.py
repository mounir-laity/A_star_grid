from tkinter.constants import NO


class Node:
    def __init__(self, row: int, column: int, parent=None) -> None:
        self.position = (row, column)
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    def set_parent(self, new_parent):
        self.parent = new_parent

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def set_heuristic(
        self, start_node: "Node", dest_node: "Node", allow_diagonal=False
    ):
        row = self.position[0]
        column = self.position[1]

        start_row = start_node.position[0]
        start_column = start_node.position[1]

        dest_row = dest_node.position[0]
        dest_column = dest_node.position[1]

        row_diff_start = abs(row - start_row)
        column_diff_start = abs(column - start_column)

        row_diff_dest = abs(row - dest_row)
        column_diff_dest = abs(column - dest_column)

        if allow_diagonal:
            self.g = self.chebyshev_distance(row_diff_start, column_diff_start)
            self.h = self.chebyshev_distance(row_diff_dest, column_diff_dest)
        else:
            self.g = self.manhattan_distance(row_diff_start, column_diff_start)
            self.h = self.manhattan_distance(row_diff_dest, column_diff_dest)
        self.f = self.g + self.h

    def manhattan_distance(self, row_diff, column_diff):
        return row_diff + column_diff

    def chebyshev_distance(self, row_diff, column_diff):
        if row_diff > column_diff:
            return row_diff
        else:
            return column_diff


class Graph:
    def __init__(self, rows, columns, start_node=None, end_node=None) -> None:
        self.start_node: Node = start_node
        self.end_node: Node = end_node
        self.rows = rows
        self.columns = columns
        self.nodes = []
        self.walls = []
        for row in range(rows):
            list_nodes = []
            for column in range(columns):
                list_nodes.append(Node(row=row, column=column, parent=None))
            self.nodes.append(list_nodes)

    def add_wall(self, row, column):
        self.walls.append(self.get_node(row, column))

    def is_wall(self, node_to_check):
        return node_to_check in self.walls

    def get_neighbours(self, current_node: Node, allow_diagonal=True) -> list[Node]:
        row = current_node.position[0]
        column = current_node.position[1]
        list_neighbours = []
        if allow_diagonal:
            for i in range(row - 1, row + 2):
                for j in range(column - 1, column + 2):
                    if i != row or j != column:
                        if i >= 0 and j >= 0 and i < self.rows and j < self.columns:
                            list_neighbours.append(self.nodes[i][j])
        else:
            for i in range(row - 1, row + 2):
                for j in range(column - 1, column + 2):
                    if (i == row and not j == column) or (
                        not i == row and j == column
                    ):  # xor
                        if i >= 0 and j >= 0 and i < self.rows and j < self.columns:
                            list_neighbours.append(self.nodes[i][j])
        return list_neighbours

    def get_node(self, row, column) -> Node:
        return self.nodes[row][column]

    def a_star_algo(self, allow_diagonal=True):
        explored_nodes: list[Node] = []
        nodes_to_explore: list[Node] = []
        self.start_node.set_heuristic(
            start_node=self.start_node,
            dest_node=self.end_node,
            allow_diagonal=allow_diagonal,
        )
        nodes_to_explore.append(self.start_node)
        while nodes_to_explore:
            nodes_to_explore.sort()
            current_node: Node = nodes_to_explore.pop(0)
            explored_nodes.append(current_node)

            if current_node == self.end_node:
                path = []
                while current_node != self.start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]

            neighbours = self.get_neighbours(current_node, allow_diagonal)
            for neighbour in neighbours:
                if self.is_wall(neighbour):
                    continue
                else:
                    neighbour.set_heuristic(
                        start_node=self.start_node,
                        dest_node=self.end_node,
                        allow_diagonal=allow_diagonal,
                    )
                    if (
                        neighbour not in explored_nodes
                        and neighbour not in nodes_to_explore
                    ):
                        if neighbour.f <= current_node.f:
                            neighbour.parent = current_node
                            nodes_to_explore.append(neighbour)

        return None


if __name__ == "__main__":
    my_graph = Graph(10, 10, Node(0, 0), Node(5, 7))
    print(my_graph.a_star_algo(False))
