import math
from random import randint

from src.GraphInterface import GraphInterface


class NodeData:

    def __gt__(self, other):
        return self.weight > other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __init__(self, key: int, distance: int, tag: int = -1, weight: float = 0.0, info: str = "", pos: tuple = None):
        self.key = key
        self.tag = tag
        self.weight = weight
        self.info = info
        self.neighbors = {}
        self.pos = pos
        self.distance = distance

    def get_node_id(self):
        return self.key

    def get_weight(self) -> float:
        return self.weight

    def set_weight(self, weight: float):
        self.weight = weight

    def get_info(self):
        return self.info

    def set_info(self, info: str):
        self.info = info

    def get_tag(self):
        return self.tag

    def set_tag(self, tag: int):
        self.tag = tag

    def get_nei(self):
        return self.neighbors.keys()

    def add_nei(self, n, w: float):
        self.neighbors[n] = w

    def remove_nei(self, n):
        if n in self.neighbors.keys():
            self.neighbors.pop(n)

    def remove_all_nei(self):
        self.neighbors.clear()

    def set_pos(self, x, y, z):
        self.pos = (x, y, z)

    def get_pos(self):
        return self.pos

    def get_distance(self) -> float:
        return self.distance

    def set_distance(self, dist: int):
        self.distance = dist

    def __repr__(self) -> str:
        return f"{self.key}"


class DiGraph(GraphInterface):

    def __init__(self, mc: int = 0):
        self.graph = {}  # { Int : NodeData }
        self.edges = {}  # { Tuple : Float}
        self.mc = mc


    def v_size(self) -> int:
        if len(self.graph) is None:
            return 0
        return len(self.graph)

    def e_size(self) -> int:
        return len(self.edges)

    def get_all_v(self) -> dict:
        return self.graph

    def get_node(self, key) -> NodeData:
        if key in self.graph.keys():
            return self.graph[key]
        return None

    def get_edge(self, src: int, dest: int):
        edge = (src, dest)
        return self.edges.get(edge)

    def all_in_edges_of_node(self, key: int) -> dict:
        if key in self.graph.keys():
            connected_nodes = {}
            node = self.get_node(key)
            for temp in self.graph.values():
                if node.get_node_id() in temp.get_nei():
                    weight = node.get_weight()
                    connected_nodes[temp.get_node_id()] = weight
            return connected_nodes
        return None

    def all_out_edges_of_node(self, key: int) -> dict:
        if key in self.graph.keys():
            out_nodes = {}
            node = self.get_node(key)
            for ni in node.get_nei():
                temp = self.get_node(ni)
                weight = temp.get_weight()
                out_nodes[ni] = weight
            return out_nodes
        return None

    def get_mc(self) -> int:
        return self.mc

    def has_edge(self, node_id1: int, node_id2: int, ) -> bool:
        if node_id1 not in self.graph or node_id2 not in self.graph:
            return False
        src = self.get_node(node_id1)
        dest = self.get_node(node_id2)
        gen_key = (src.get_node_id(), dest.get_node_id())
        ret = self.edges.get(gen_key)
        if ret is None:
            return False
        return True

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.graph.keys() or id2 not in self.graph.keys() or weight <= 0:
            return False

        src = self.get_node(id1)
        gen_key = (id1, id2)

        if not self.has_edge(id1, id2):
            self.edges[gen_key] = weight
            dest = self.get_node(id2)
            dest.set_weight(weight)
            src.add_nei(id2, weight)
            self.mc = self.mc + 1
            return True

        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.graph.keys():
            return False

        new_node = NodeData(key=node_id, distance=0)
        if pos is not None:
            new_node.set_pos(pos[0], pos[1], pos[2])
        else:
            rnd = randint(0, 100)
            rnd2 = randint(0, 100)
            new_node.set_pos(rnd, rnd2, 0)

        self.graph[node_id] = new_node
        self.mc = self.mc + 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.graph:
            node = self.get_node(node_id)
            for n in self.all_in_edges_of_node(node_id):
                temp = self.get_node(n)
                temp.neighbors.pop(node.get_node_id())
            self.graph.pop(node_id)
            self.mc = self.mc + 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        gen_key = (node_id1, node_id2)
        if gen_key in self.edges:
            self.edges.pop(gen_key)
            node1 = self.get_node(node_id1)
            node2 = self.get_node(node_id2)
            node1.neighbors.pop(node_id2)
            self.mc = self.mc + 1
            return True
        return False

    def get_max_x_y(self):
        x = -1
        y = -1
        for v in self.get_all_v().values():
            if v.get_pos()[0] > x:
                x = v.get_pos()[0]
            if v.get_pos()[1] > y:
                y = v.get_pos()[1]
        return x,y

    def get_min_x_y(self):
        x = math.inf
        y = math.inf
        for v in self.get_all_v().values():
            if v.get_pos() is None:
                continue
            else:
                if v.get_pos()[0] < x:
                    x = v.get_pos()[0]
                if v.get_pos()[1] < y:
                    y = v.get_pos()[1]
        return x,y

