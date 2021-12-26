class Node:
    """This class represents the Nodes of the Graph where the search algorithm is used."""

    def __init__(self, row: int, column: int, parent: "Node" = None) -> None:
        """Creates a Node with the given position and default heuristics

        Attributes:
            position (tuple): The position (row, column) of the Node

            parent (Node) : The parent Node of this Node.
                This is used to find the path to the destination in the a star algorithm.

            g (int): The number of Nodes separating this Node to the starting Node
            h (int): The number of Nodes separating this Node to the goal Node
            f (int): The total cost of the Node (calculated by doing g + h)

        Args:
            row (int): The row of the Node

            column (int): The column of the Node

            parent (Node, optional): The Node's parent Node.
                Defaults to None.
        """
        self.position = (row, column)
        self.parent = parent
        self.g = 0
        self.h = 999
        self.f = self.g + self.h

    def __eq__(self, other) -> bool:
        """Checks if the Node is equal to the other object.

        Args:
            other (Object): The other object to check if the Node is equal to.

        Returns:
            bool: True if the two are equal, False otherwise.
        """
        if other is None or type(self) is not type(other):
            return False
        return self.position == other.position

    def __lt__(self, other: "Node") -> bool:
        """Decides in which order the Nodes should be sorted based on their heuristics.

        Args:
            other (Node): The other Node to see if it should be put before
            or after this Node during sorting.

        Returns:
            bool: True if this Node should be put first.
            False if the other Node should be put first.
        """
        if self.f < other.f:
            return True
        if other.f < self.f:
            return False
        return self.g > other.g

    def set_heuristic(self, dest_node: "Node", allow_diagonal: bool = False) -> None:
        """Set the heuristics of a Node. If diagonal movement is allowed,
         the chebyshev distance is used for that. Otherwise, the simple
         manhattan distance is used for that.

        Args:
            dest_node (Node): The goal Node to calculate the distance to.
            allow_diagonal (bool, optional): The flag that tells if
            diagonal movement is allowed.
            Defaults to False.
        """
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
        """Calculates the distance between two Nodes using the manhattan distance technique.
        see http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html

        Args:
            row_diff (int): The difference between the two nodes row values
            column_diff (int): The difference between the two column values

        Returns:
            int: The total distance
        """
        return row_diff + column_diff

    def chebyshev_distance(self, row_diff: int, column_diff: int) -> int:
        """Calculates the distance between two Nodes using the Chebyshev distance method.
        see http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html

        Args:
            row_diff (int): The difference between the two nodes row values
            column_diff (int): The difference between the two column values

        Returns:
            int: The total distance
        """
        if row_diff > column_diff:
            return row_diff
        else:
            return column_diff


class Graph:
    """This class represents the maze containing all the Nodes for the a star algorithm."""

    def __init__(
        self, rows: int, columns: int, start_node: Node = None, dest_node: Node = None
    ) -> None:
        """Creates a Graph of given size containing default Nodes
        and initializes an empty list of walls.

        Attributes:
            start_node (Node, optional): The starting Node for the algorithm.
            dest_node (Node, optional): The goal Node for the algorithm.
            rows (int): The number of rows of the graph.
            columns (int): The number of columns of the graph.
            nodes (list): The list of all Nodes rows.
            walls (list): The list of all walls. Walls are Nodes that can't be crossed
            by the algorithm

        Args:
            rows (int): The number of rows of the graph.
            columns (int): The number of columns of the graph.
            start_node (Node, optional): The starting Node for the algorithm.
            Defaults to None.
            dest_node (Node, optional): The goal Node for the algorithm.
            Defaults to None.
        """
        self.start_node: Node = start_node
        self.dest_node: Node = dest_node
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
        """Adds a wall to the Graph's walls list.

        Args:
            row (int): The row of the Node to add to the list
            column (int): The column of the Node to add to the list
        """
        self.walls.append(self.get_node(row, column))

    def is_wall(self, node_to_check: Node) -> bool:
        """Checks if the given Node is a wall.

        Args:
            node_to_check (Node): The Node to check

        Returns:
            bool: True if it the Node to check is a wall. False otherwise.
        """
        return node_to_check in self.walls

    def get_neighbours(self, current_node: Node, allow_diagonal=True) -> list[Node]:
        """Gets all Nodes accessible to the current Node with only one step.
        These are the Nodes that are directly above, under, to the left and
        to the right of the current Node if diagonal movement is not allowed.
        Otherwise, they are all adjacent Nodes.

        Args:
            current_node (Node): The Node from which we must obtain all neighbours.
            allow_diagonal (bool, optional): The flag that tells if
            diagonal movement is allowed.
            Defaults to True.

        Returns:
            list[Node]: The list of all neighbouring Nodes of the current Node.
        """
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
        """Gets the Node at the given row and column values.

        Args:
            row (int): The row of the Node to get.
            column (int): The column of the Node to get.

        Returns:
            Node: The Node at the given row and column.

        Raises:
            IndexError: If the row or column is bigger than the Graph's
            row or columns or is smaller than 0.
        """
        try:
            return self.nodes[row][column]
        except IndexError:
            print(row, column)
            exit(1)

    def set_start_node(self, row, column):
        """Sets the starting Node to the one given by its row and column.

        Args:
            row ([type]): The row of the Node to set as the starting Node.
            column ([type]): The column of the Node to set as the starting Node.
        """
        self.start_node = self.get_node(row, column)

    def set_dest_node(self, row, column):
        """Sets the goal Node to the one given by its row and column.

        Args:
            row ([type]): The row of the Node to set as the goal Node.
            column ([type]): The column of the Node to set as the goal Node.
        """
        self.dest_node = self.get_node(row, column)

    def a_star_algo(self, allow_diagonal=True) -> list[tuple[int, int]]:
        """Uses the a star algorithm to find the shortest path between
        the starting Node and the goal Node.
        See https://en.wikipedia.org/wiki/A*_search_algorithm

        Args:
            allow_diagonal (bool, optional): The flag that tells if
            diagonal movement is allowed. Defaults to True.

        Returns:
            list[tuple[int, int]]: The list of positions of all Nodes in the shortest path.
        """
        explored = []
        to_explore = []
        self.start_node.g = 0
        self.start_node.set_heuristic(self.dest_node, allow_diagonal)
        to_explore.append(self.start_node)
        while to_explore:
            to_explore.sort()
            current = to_explore.pop(0)
            explored.append(current)
            if current == self.dest_node:
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
                neighbour.set_heuristic(self.dest_node, allow_diagonal)
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
