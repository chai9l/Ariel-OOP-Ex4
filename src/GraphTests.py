import unittest
from DiGraph import *


class GraphTests(unittest.TestCase):

    def test_add_node(self):
        g = DiGraph()
        self.assertTrue(g.add_node(5,(5,2,3)))

    def test_add_edge(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        self.assertTrue(g.add_edge(5,6,5.0))

    def test_get_node(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        self.assertTrue(g.get_node(5))

    def test_get_edge(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        g.add_edge(5, 6, 5.0)
        self.assertTrue(g.get_edge(5,6))
        self.assertFalse(g.get_edge(6,5))

    def test_v_size(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        self.assertEqual(g.v_size(),1)

    def test_e_size(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        g.add_edge(5, 6, 5.0)
        self.assertEqual(g.e_size(),1)

    def test_get_all_v(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        self.assertTrue(g.get_all_v())

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        g.add_edge(5, 6, 5.0)
        g.add_edge(6,5,3.0)
        self.assertTrue(g.all_in_edges_of_node(5))

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        g.add_edge(5, 6, 5.0)
        g.add_edge(6, 5, 3.0)
        self.assertTrue(g.all_out_edges_of_node(5))

    def test_get_mc(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        g.add_edge(5, 6, 5.0)
        g.add_edge(6, 5, 3.0)
        self.assertTrue(g.get_mc())

    def test_remove_node(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        g.add_edge(5, 6, 5.0)
        g.add_edge(6, 5, 3.0)
        self.assertTrue(g.remove_node(5))

    def test_remove_edge(self):
        g = DiGraph()
        g.add_node(5, (5, 2, 3))
        g.add_node(6, (3, 2, 1))
        g.add_edge(5, 6, 5.0)
        g.add_edge(6, 5, 3.0)
        self.assertTrue(g.remove_edge(5,6))







