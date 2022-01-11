import functools
import itertools
import math
import queue
import sys
from abc import ABC
from collections import deque
from typing import List

from numpy import square

from src import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph, NodeData
import json
from queue import *
import matplotlib.pyplot as plt
import random
from src.GraphAlgoInterface import GraphAlgoInterface


def check_location(n1: NodeData) -> float:
    pos = n1.get_pos()
    x = pos[0]
    y = pos[1]
    z = pos[2]
    d = math.sqrt(x * x + y * y + z * z)
    return d


def compare(n1: NodeData, n2: NodeData) -> int:
    d1 = check_location(n1)
    d2 = check_location(n2)
    if d1 > d2:
        return 1
    elif d1 < d2:
        return -1
    else:
        return 0


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = None):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        loaded_graph = DiGraph()

        try:
            with open(file_name, 'r') as j_file:
                json_str = j_file.read()
                j_graph = json.loads(json_str)

            for node in j_graph['Nodes']:
                pos = node.get('pos')
                if pos is not None:
                    pos = tuple(map(float, node['pos'].split(',')))
                key = node['id']
                loaded_graph.add_node(key, pos)

            for edge in j_graph['Edges']:
                if edge['w'] is None:
                    loaded_graph.add_edge(int(edge['src']), int(edge['dest']), 0.0)
                else:
                    loaded_graph.add_edge(int(edge['src']), int(edge['dest']), float(edge['w']))

            self.graph = loaded_graph
        except IOError:
            return False

        if self.graph is not None:
            return True

        return False

    def save_to_json(self, file_name: str) -> bool:

        if self.graph is None:
            return False

        j_graph = dict()
        j_nodes = []
        j_edges = []

        try:
            with open(file_name, 'w') as file:

                for node in self.graph.get_all_v().values():
                    node_info = dict()
                    pos = node.get_pos()
                    if pos is not None:
                        pos_str = str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2])
                        node_info["pos"] = pos_str
                    node_info["id"] = node.get_node_id()
                    j_nodes.append(node_info)

                for edge in self.graph.edges:
                    edge_info = dict()
                    edge_info["src"] = edge[0]
                    edge_info["dest"] = edge[1]
                    edge_info["w"] = self.graph.get_edge(edge[0], edge[1])
                    j_edges.append(edge_info)
                j_graph["Edges"] = j_edges
                j_graph["Nodes"] = j_nodes

                json.dump(j_graph, indent=4, fp=file)
            return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.graph is None:
            return []
        src = self.graph.get_node(id1)
        dest = self.graph.get_node(id2)
        # prio_que = PriorityQueue()
        p_que = deque()
        prev = {}
        vis = {}
        directions = []
        if src is not None and dest is not None:

            if id1 == id2:
                directions.append(id1)
                return 0, directions

            for t in self.graph.get_all_v():
                self.graph.get_node(t).set_tag(-1)

            src.set_tag(0)
            # prio_que.put(src)
            p_que.append(src)
            vis[src.get_node_id()] = True
            current = src
            new_ret = src

            # while not prio_que.empty():
            while len(p_que) != 0:

                # current = prio_que.get()
                current = p_que.pop()

                # if current.get_node_id() == dest.get_node_id():
                #     break

                for out_node in self.graph.all_out_edges_of_node(current.key):
                    d = self.graph.get_edge(current.get_node_id(), out_node)
                    node_dest = self.graph.get_node(out_node)
                    node_dest_id = out_node

                    if node_dest.get_tag() == -1:
                        node_dest.set_tag(sys.maxsize)

                    new_dis = current.get_tag() + d
                    prev_dis = node_dest.get_tag()

                    if new_dis < prev_dis:
                        node_dest.set_tag(new_dis)
                        prev[node_dest.get_node_id()] = current.get_node_id()
                        # prio_que.put(node_dest)
                        p_que.appendleft(node_dest)
                if current.get_node_id() == dest.get_node_id():
                    new_ret = current

                vis[new_ret.get_node_id] = True

            eq = new_ret.get_node_id() == dest.get_node_id()
            if not eq:
                return float('inf'), []

            node_finish = dest
            directions.append(dest.get_node_id())
            temp_weight = 0

            while node_finish is not None:
                node_finish = prev.get(node_finish.get_node_id())
                if node_finish is not None:
                    directions.append(node_finish)
                node_finish = self.graph.get_node(node_finish)

            for s, d in prev.items():
                if s in directions and d in directions:
                    e = (d, s)
                    if e in self.graph.edges.keys():
                        temp_weight = temp_weight + self.graph.edges[e]

            directions.reverse()

            return temp_weight, directions

        elif src is None or dest is None:
            return float('inf'), []

        else:
            return directions

    def isConnected(self):
        if self.graph is None:
            return False
        keys = []
        for key in self.graph.get_all_v().keys():
            keys.append(key)
        id = keys[0]

        i = 0
        for key in self.graph.get_all_v():
            self.graph.get_node(keys[i]).set_tag(0)
            i = i + 1

        node_id = self.graph.get_node(id)
        node_id.set_tag(1)
        que = [node_id]
        connected = []
        gIsConnected = False
        gtIsConnected = False
        # check = False
        while len(que) != 0:
            curr = que.pop()
            connected.append(curr)
            curr_nei = self.graph.all_out_edges_of_node(curr.get_node_id())
            for nei in curr_nei.keys():
                node_nei = self.get_graph().get_node(nei)

                if node_nei.get_tag() == 0:
                    node_nei.set_tag(1)
                    que.append(node_nei)

        i = 0
        for key in self.graph.get_all_v():
            self.graph.get_node(key).set_tag(0)
            i = i + 1
        if len(connected) == len(self.graph.get_all_v()):
            gIsConnected = True

        tran_graph = self.transpose_graph(self.graph)
        node_id.set_tag(1)
        que = [node_id]
        trans_connected = []
        while len(que) != 0:
            curr = que.pop()
            trans_connected.append(curr)
            curr_nei = tran_graph.all_out_edges_of_node(curr.get_node_id())
            for nei in curr_nei.keys():
                node_nei = self.get_graph().get_node(nei)
                if node_nei.get_tag() == 0:
                    que.append(node_nei)
                    node_nei.set_tag(1)

        if len(trans_connected) == len(tran_graph.get_all_v()):
            gtIsConnected = True

        if gIsConnected and gtIsConnected:
            return True

        return False

    ########################## TO DO #################################

    def create_path_dict(self, node_lst: List[int]) -> {}:
        path_dict = {}  # { (node1_id, node2_id) : (path_length, path)
        for node1_id in node_lst:
            for node2_id in node_lst:
                if node1_id == node2_id:
                    path_dict[(node1_id, node2_id)] = (0.0, [])
                else:
                    sp = self.shortest_path(node1_id, node2_id)
                    path_dict[(node1_id, node2_id)] = sp
        return path_dict

    def create_all_list_permutations(self, node_lst: List[int], path_dict: {}) -> {}:
        ret = {}
        for perm in list(itertools.permutations(node_lst)):
            list_to_string = str(perm)
            ret[list_to_string] = self.create_val(node_lst, path_dict)
        return ret

    def create_val(self, lst: List[int], path_dict: {}) -> (float, list):
        ret = []
        length = 0
        for i in range(len(lst)):
            if i + 1 == len(lst):
                break
            src = lst[i]
            dest = lst[i + 1]
            temp_tup = path_dict.get((src, dest))
            for ele in temp_tup[1]:
                if ele not in ret:
                    ret.append(ele)
                else:
                    continue
            length = length + temp_tup[0]
        return length, ret

    def choose_best_path(self, perm_dict: {}) -> (List[int], float):
        min = math.inf
        tup = (float, List[int])
        for perm in perm_dict.values():
            if perm[0] < min:
                min = perm[0]
                tup = perm
        ret = (tup[1], tup[0])
        return ret




    def TSP(self, node_lst: List[int]) -> (List[int], float):
        path_dict = self.create_path_dict(node_lst)  # { (node1_id, node2_id) : (path_length, path)
        permutations_dict = self.create_all_list_permutations(node_lst, path_dict)
        ret = self.choose_best_path(permutations_dict)
        return ret

    def sort_queue(self, q: {}) -> int:
        ret = -1
        min_dist = sys.float_info.max
        for v in q.values():
            dist = v.get_distance()
            if dist < min_dist:
                min_dist = dist
                ret = v.get_node_id()
        return ret

    def dijkstra(self, source: NodeData) -> None:
        q = {}
        for v in self.get_graph().get_all_v().values():
            v.set_distance(sys.float_info.max)
            q[v.get_node_id()] = v

        source.set_distance(0)
        while len(q) != 0:
            temp_min = self.sort_queue(q)
            if temp_min == -1:
                break
            temp_min_node = self.get_graph().get_node(temp_min)
            q.pop(temp_min)
            for neighbour_id in temp_min_node.get_nei():
                neighbour = self.graph.get_node(neighbour_id)
                edge_weight = self.graph.get_edge(temp_min, neighbour_id)
                dist_from_src = temp_min_node.get_distance() + edge_weight
                if dist_from_src < neighbour.get_distance():
                    neighbour.set_distance(dist_from_src)

    def centerPoint(self) -> (int, float):
        connected = self.isConnected()
        if connected is not True:
            return None, math.inf
        ret = NodeData
        shortest_dist = math.inf
        for v in self.get_graph().get_all_v().values():
            max_dist = -1
            self.dijkstra(v)
            for vi in self.get_graph().get_all_v().values():
                if vi.get_distance() > max_dist:
                    max_dist = vi.get_distance()
            if max_dist < shortest_dist:
                shortest_dist = max_dist
                ret = v.get_node_id()
        return ret, shortest_dist

    ###################################################################

    def plot_graph(self) -> None:
        if self.graph is None:
            return None

        plt.grid(color='purple', linestyle='dashed', linewidth=0.4)
        for e in self.get_graph().edges:
            src = self.get_graph().get_node(e[0])
            dest = self.get_graph().get_node(e[1])

            if src.get_pos() is None:
                src.set_pos(random.uniform(0, 100), random.uniform(0, 100), 0)
            if dest.get_pos() is None:
                dest.set_pos(random.uniform(0, 100), random.uniform(0, 100), 0)
            x1 = src.get_pos()[0]
            x2 = dest.get_pos()[0]
            y1 = src.get_pos()[1]
            y2 = dest.get_pos()[1]
            plt.annotate("", xy=(x1, y1), xytext=(x2, y2), arrowprops=dict(arrowstyle="->"))

        for node_id, node in self.get_graph().get_all_v().items():
            plt.annotate(str(node_id), (node.get_pos()[0], node.get_pos()[1]), color='black')
            plt.plot(node.get_pos()[0], node.get_pos()[1], ".", color='red', markersize=10)

        plt.xlabel(
            "X ------------------------------------------------------------------------------------------------------>")
        plt.ylabel("Y -------------------------------------------------------------------------->")
        plt.title("Ex3")
        plt.show()

    def transpose_graph(self, to_transpose: DiGraph) -> DiGraph:

        ret = DiGraph()

        for node in to_transpose.graph:
            temp_node = to_transpose.get_node(node)
            temp_node.set_tag(0)
            ret.add_node(temp_node.get_node_id())

        for edge, weight in to_transpose.edges.items():
            e_temp = edge
            w_temp = weight
            ret.add_edge(e_temp[1], e_temp[0], w_temp)

        return ret

    # def create_path_tup_dict(self, tup_lst) -> {}:
    #     path_dict = {}
    #     for tup1 in tup_lst:
    #         for tup2 in tup_lst:
    #             if tup1 == tup2:
    #                 continue
    #             else:
    #                 src1 = tup1[0]
    #                 dest1 = tup1[1]
    #                 src2 = tup2[0]
    #                 dest2 = tup2[1]
    #                 sp = [src1, dest2]
    #                 sp.insert(src1, self.shortest_path(dest1, src2)[1])
    #                 path_dict[(tup1, tup2)] = sp
    #     return path_dict

    def graph_reset(self):
        for node in self.graph.graph:
            node = self.graph.get_node(node)
            node.set_tag(0)


    def create_path_tup_dict(self, tup_lst) -> {}:
        path_dict = {}
        for tup1 in tup_lst:
            for tup2 in tup_lst:
                if tup1 == tup2:
                    continue
                else:
                    src1 = tup1[0]
                    dest1 = tup1[1]
                    src2 = tup2[0]
                    dest2 = tup2[1]
                    val = []
                    val.append(src1)
                    end_w = self.get_graph().get_edge(src2, dest2)
                    (path_cost, sp) = self.shortest_path(dest1, src2)
                    path_cost += end_w
                    for n in sp:
                        val.append(n)
                    val.append(dest2)
                    path_dict[(tup1, tup2)] = (path_cost, val)
                    # IMPORTANT
                    # MISSING THE FIRST EDGE WEIGHT IN THE CALC ADD IT
        return path_dict

    def create_all_list_tuple_permutations(self, node_lst, path_dict) -> {}:
        ret = {}
        for perm in list(itertools.permutations(node_lst)):
            list_to_string = str(perm)
            ret[list_to_string] = self.create_val_tup(node_lst, path_dict)
        return ret

    def create_val_tup(self, tup_lst, path_dict) -> (float, list):
        ret = []
        length = 0
        first = tup_lst[0]
        start_weight = self.graph.get_edge(first[0],first[1])
        for i in range(len(tup_lst)):
            if i + 1 == len(tup_lst):
                break
            tup1 = tup_lst[i]
            tup2 = tup_lst[i + 1]
            node_lst = path_dict.get((tup1, tup2))[1]  ## tup1_src -> tup1_dest -> .... -> tup2_src -> tup2_dest
            path_cost = path_dict.get((tup1, tup2))[0]
            for n in node_lst:
                if n not in ret:
                    ret.append(n)
                else:
                    continue
            length = length + path_cost
        length = length + start_weight
        return length, ret

    def choose_best_path_tuples(self, perm_dict) -> (List[int], float):
        min = math.inf
        tup = (float, List[(tuple)])
        for perm in perm_dict.values():
            if perm[0] < min:
                min = perm[0]
                tup = perm
        ret = (tup[1], tup[0])
        return ret

    def tup_TSP(self, node_lst) -> (List[int], float):
        path_dict = self.create_path_tup_dict(node_lst)  # { ((src1, dest1), (src2, dest2)) : (path_length, path)
        permutations_dict = self.create_all_list_tuple_permutations(node_lst, path_dict)
        ret = self.choose_best_path_tuples(permutations_dict)
        return ret

    def tup_TSP_nomin(self, node_lst):
        path_dict = self.create_path_tup_dict(node_lst)  # { ((src1, dest1), (src2, dest2)) : (path_length, path)
        permutations_dict = self.create_all_list_tuple_permutations(node_lst, path_dict)
        return permutations_dict

    # def create_all_list_tuple_permutations(self, node_lst, path_dict) -> {}:
    #     ret = {}
    #     for perm in list(itertools.permutations(node_lst)):
    #         list_to_string = str(perm)
    #         ret[list_to_string] = self.create_val_tup(node_lst, path_dict)
    #     return ret
    #
    # def create_val_tup(self, tup_lst, path_dict) -> (float, list):
    #     ret = []
    #     length = 0
    #     for i in range(len(tup_lst)):
    #         if i + 1 == len(tup_lst):
    #             break
    #         tup1 = tup_lst[i]
    #         tup2 = tup_lst[i + 1]
    #         temp_tup = path_dict.get((tup1, tup2))  ## tup1_src -> tup1_dest -> .... -> tup2_src -> tup2_dest
    #         for ele in temp_tup[1]:
    #             if ele not in ret:
    #                 ret.append(ele)
    #             else:
    #                 continue
    #         length = length + temp_tup[0]
    #     return length, ret
    #
    # def choose_best_path_tuples(self, perm_dict) -> (List[int], float):
    #     min = math.inf
    #     tup = (float, List[(tuple)])
    #     for perm in perm_dict.values():
    #         if perm[0] < min:
    #             min = perm[0]
    #             tup = perm
    #     ret = (tup[1], tup[0])
    #     return ret
    #
    # def tup_TSP(self, node_lst) -> (List[int], float):
    #     path_dict = self.create_path_tup_dict(node_lst)  # { ((src1, dest1), (src2, dest2)) : (path_length, path)
    #     permutations_dict = self.create_all_list_tuple_permutations(node_lst, path_dict)
    #     ret = self.choose_best_path_tuples(permutations_dict)
    #     return ret