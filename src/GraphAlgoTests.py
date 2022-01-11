import unittest
from GraphAlgo import *


class GraphAlgoTests(unittest.TestCase):

    def test_get_graph(self):
        file = '../data/A5.json'
        g = GraphAlgo()
        g.load_from_json(file)
        self.assertTrue(g.get_graph())


    def test_load(self):
        file = '../data/A5.json'
        g = GraphAlgo()
        g.load_from_json(file)
        self.assertTrue(g.load_from_json(file))
        self.assertEqual(g.graph.v_size(), 48)


    def test_save(self):
        file = '../data/A5_save_test.json'
        file2 = '../data/A5.json.json'
        g = GraphAlgo()
        g.load_from_json(file2)
        self.assertTrue(g.save_to_json(file))
        print("saved")

    def test_isConnected(self):
        file = '../data/A5.json'
        g = GraphAlgo()
        g.load_from_json(file)
        self.assertTrue(g.isConnected())

    def test_shortestPath(self):
        file = '../data/A5.json'
        g = GraphAlgo()
        g.load_from_json(file)
        self.assertEqual(g.shortest_path(3,40),(6.035861657209951, [3, 13, 14, 15, 39, 40]))

    def test_center(self):
        file = '../data/A5.json'
        g = GraphAlgo()
        g.load_from_json(file)
        node_id,dist = g.centerPoint()
        self.assertEqual(node_id,40)
        self.assertEqual(dist,9.291743173960954)

    def test_tsp(self):
        file = '../data/A5.json'
        g = GraphAlgo()
        g.load_from_json(file)
        self.assertEqual(g.TSP([19,20,30]),([19,20,21,32,31,30],6.515229750630192))


