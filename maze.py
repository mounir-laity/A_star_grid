class Node:
    def __init__(self, row: int, column: int, parent: "Node" = None) -> None:
        self.position = (row, column)
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 999  # Distance to goal node
        self.f = 999  # Total cost

    def set_parent(self, new_parent: "Node") -> None:
        self.parent = new_parent

    def __eq__(self, other) -> bool:
        if other is None or type(self) != type(other):
            return False
        return self.position == other.position

    def __lt__(self, other) -> bool:
        if self.f < other.f:
            return True
        if other.f < self.f:
            return False
        return self.g > other.g

    def set_heuristic(self, dest_node: "Node", allow_diagonal: bool = False) -> None:
        row = self.position[0]
        column = self.position[1]

        dest_row = dest_node.position[0]
        dest_column = dest_node.position[1]

        row_diff_dest = abs(row - dest_row)
        column_diff_dest = abs(column - dest_column)

        if allow_diagonal:
            self.h = self.chebyshev_distance(row_diff_dest, column_diff_dest)
        else:
            self.h = self.manhattan_distance(row_diff_dest, column_diff_dest)
        self.f = self.g + self.h

    def manhattan_distance(self, row_diff: int, column_diff: int) -> int:
        return row_diff + column_diff

    def chebyshev_distance(self, row_diff: int, column_diff: int) -> int:
        if row_diff > column_diff:
            return row_diff
        else:
            return column_diff


class Graph:
    def __init__(
        self, rows: int, columns: int, start_node: Node = None, end_node: Node = None
    ) -> None:
        self.start_node: Node = start_node
        self.end_node: Node = end_node
        self.rows = rows
        self.columns = columns
        self.nodes = []
        self.walls: list[Node] = []
        for row in range(rows):
            list_nodes = []
            for column in range(columns):
                list_nodes.append(Node(row=row, column=column, parent=None))
            self.nodes.append(list_nodes)

    def add_wall(self, row: int, column: int) -> None:
        self.walls.append(self.get_node(row, column))

    def is_wall(self, node_to_check: Node) -> bool:
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

    def get_node(self, row: int, column: int) -> Node:
        try:
            return self.nodes[row][column]
        except IndexError:
            print(row, column)
            exit(1)

    def set_start_node(self, row: int, column: int) -> None:
        self.start_node = self.get_node(row, column)

    def set_end_node(self, row: int, column: int) -> None:
        self.end_node = self.get_node(row, column)

    def a_star_algo(self, allow_diagonal=True) -> list[tuple[int, int]]:
        explored = []
        to_explore = []
        self.start_node.g = 0
        self.start_node.set_heuristic(self.end_node, allow_diagonal)
        to_explore.append(self.start_node)
        while to_explore:
            to_explore.sort()
            current = to_explore.pop(0)
            explored.append(current)
            if current == self.end_node:
                path = []
                while current != self.start_node:
                    path.append(current.position)
                    current = current.parent
                path.append(self.start_node.position)
                # Return reversed path
                return path[::-1], explored

            neighbours = self.get_neighbours(current, allow_diagonal)
            for neighbour in neighbours:
                neighbour.g = current.g + 1
                neighbour.set_heuristic(self.end_node, allow_diagonal)
            neighbours.sort()
            for neighbour in neighbours:
                if self.is_wall(neighbour):
                    continue
                if neighbour in explored:
                    continue
                if neighbour not in to_explore:
                    neighbour.parent = current
                    to_explore.append(neighbour)
        return None, explored


if __name__ == "__main__":
    my_graph = Graph(10, 10, Node(7, 3), Node(7, 5))
    my_graph.walls.append(my_graph.get_node(1, 4))
    my_graph.walls.append(my_graph.get_node(2, 4))
    my_graph.walls.append(my_graph.get_node(7, 4))
    my_graph.walls.append(my_graph.get_node(3, 4))
    my_graph.walls.append(my_graph.get_node(4, 4))
    my_graph.walls.append(my_graph.get_node(5, 4))
    my_graph.walls.append(my_graph.get_node(6, 4))
    my_graph.walls.append(my_graph.get_node(8, 4))
