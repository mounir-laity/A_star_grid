class Node:
    def __init__(self, row: int, column: int, parent=None) -> None:
        self.row = row
        self.column = column
        self.parent = parent

    def set_parent(self, new_parent):
        self.parent = new_parent

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def get_position(self):
        return self.row, self.column

    def get_heuristic(self, dest_node: "Node", allow_diagonal=False):
        row = self.row
        column = self.column
        dest_pos = dest_node.get_position()
        dest_row = dest_pos[0]
        dest_column = dest_pos[1]
        if row >= dest_row:
            row_diff = row - dest_row
        else:
            row_diff = dest_row - row

        if column >= dest_column:
            column_diff = column - dest_column
        else:
            column_diff = dest_column - column

        if allow_diagonal:
            return self.chebyshev_distance(row_diff, column_diff)
        else:
            return self.manhattan_distance(row_diff, column_diff)

    def manhattan_distance(self, row_diff, column_diff):
        return row_diff + column_diff

    def chebyshev_distance(self, row_diff, column_diff):
        if row_diff > column_diff:
            return row_diff
        else:
            return column_diff


class Graph:
    def __init__(self, rows, columns, start_node=None, end_node=None) -> None:
        self.start_node = start_node
        self.end_node = end_node
        self.rows = rows
        self.columns = columns
        self.nodes = []
        for row in range(rows):
            list_nodes = []
            for column in range(columns):
                list_nodes.append(Node(row=row, column=column, parent=None))
            self.nodes.append(list_nodes)

    def get_neighbours(self, current_node: Node, allow_diagonal=True):
        row = current_node.row
        column = current_node.column
        list_neighbours = []
        if allow_diagonal:
            for i in range(row - 1, row + 2):
                for j in range(column - 1, column + 2):
                    if i != current_node.row or j != current_node.column:
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

    def a_star_algo(self):
        explored_nodes = []
        nodes_to_explore = []


if __name__ == "__main__":
    my_graph = Graph(10, 10)
    print(my_graph.get_node(3, 3).get_heuristic(my_graph.get_node(5, 5), True))
    # my_list = my_graph.get_neighbours(my_graph.get_node(9, 9), True)
    # for my_node in my_list:
    #     print(my_node.get_position())
    # print(my_graph.get_node(3, 3).get_position())
