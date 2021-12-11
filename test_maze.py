from typing import Tuple
import unittest
import maze


class TestMaze(unittest.TestCase):
    def test_create_node(self):
        my_node = maze.Node(0, 0)
        self.assertTrue(
            my_node.row == 0 and my_node.column == 0 and my_node.parent is None
        )

    def test_node_equ_when_same(self):
        node_a = maze.Node(4, 4)
        self.assertEqual(node_a, node_a)

    def test_two_nodes_equal(self):
        node_a = maze.Node(4, 4)
        node_b = maze.Node(4, 4)
        self.assertEqual(node_a, node_b)

    def test_two_nodes_not_same_row(self):
        node_a = maze.Node(4, 5)
        node_b = maze.Node(3, 5)
        self.assertNotEqual(node_a, node_b)

    def test_two_nodes_not_same_column(self):
        node_a = maze.Node(3, 0)
        node_b = maze.Node(3, 5)
        self.assertNotEqual(node_a, node_b)

    def test_two_nodes_not_same_row_or_column(self):
        node_a = maze.Node(0, 7)
        node_b = maze.Node(3, 5)
        self.assertNotEqual(node_a, node_b)


if __name__ == "__main__":
    unittest.main()
