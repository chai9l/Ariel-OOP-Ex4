import functools
import itertools
from types import SimpleNamespace

from Agent import Agent
from DiGraph import DiGraph, NodeData
from GraphAlgo import GraphAlgo
from Pokemon import Pokemon
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from math import sqrt
import math

WIDTH, HEIGHT = 1080, 720
PORT = 6666
HOST = '127.0.0.1'


class Game:

    def __init__(self, g: GraphAlgo = None):
        self.g = g
        self.agents = []
        self.pokemons = []
        self.min_x = float
        self.min_y = float
        self.max_x = float
        self.max_y = float

    # def add_agents(self):
    #     pokemon_list = []
    #     dict_info = json.loads(client.get_info())
    #     info = dict_info['GameServer']
    #     num_of_agents = info['agents']
    #     pokemons_str = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    #     pokemons = [p.Pokemon for p in pokemons_str]
    #     for p in pokemons:
    #         x_str, y_str, _ = p.pos.split(',')
    #         new_pokemon = Pokemon(p.value, p.type, (float(x_str), float(y_str)))
    #         x1 = self.my_scale(float(x_str), x=True)
    #         y1 = self.my_scale(float(y_str), y=True)
    #         new_pokemon.set_edge(self.find_pokemon_edge(x1, y1, new_pokemon.type))
    #         pokemon_list.append(new_pokemon)
    #
    #     pokemon_list.sort(key=lambda x: x.value, reverse=True)
    #
    #     if num_of_agents == 1:
    #         src = pokemon_list[0].get_edge()[0]
    #         client.add_agent("{\"id\":" + str(src) + "}")


    def scale(self, data, min_screen, max_screen, min_data, max_data):
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, screen.get_height() - 50, self.min_y, self.max_y)

    def load_pokemons(self):

        pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        for p in pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=float(x), y=float(y))
            pokemon = Pokemon(p.value, p.type, (p.pos.x, p.pos.y))
            if pokemon.get_edge() != None:
                x1 = self.my_scale(p.pos.x, x=True)
                y1 = self.my_scale(p.pos.y, y=True)
                pokemon.set_edge(self.find_pokemon_edge(x1, y1, p.type))
            if len(self.pokemons) == 0:
                self.pokemons.append(pokemon)
            if len(self.pokemons) != 0:
                if self.duplicate_list(pokemon):
                    self.pokemons.append(pokemon)

        self.pokemons.sort(key=lambda x: x.value, reverse=True)

    def duplicate_list(self, pokemon: Pokemon):
        for p2 in self.pokemons:
            if pokemon == p2:
                return False
        return True

    def duplicate_list2(self, pokemon: Pokemon, list: []):
        for p2 in list:
            if pokemon == p2:
                return False
        return True

    def load_agents(self):
        agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for a in agents:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=float(x), y=float(y))
            agent = Agent(a.id, a.value, a.src, a.dest, a.speed, (a.pos.x, a.pos.y))
            self.agents.append(agent)

    def find_pokemon_edge(self, x: int, y: int, type):
        new_src = 0
        new_dest = 0

        if type == 1:
            for e in self.g.get_graph().edges:
                src = e[0]
                dest = e[1]
                if src > dest:
                    continue
                if self.check_if_on_edge(src, dest, x, y):
                    new_src = src
                    new_dest = dest
        else:
            for e in self.g.get_graph().edges:
                src = e[0]
                dest = e[1]
                if src < dest:
                    continue
                if self.check_if_on_edge(src, dest, x, y):
                    new_src = src
                    new_dest = dest

        return new_src, new_dest

    def check_if_on_edge(self, src: int, dest: int, x: int, y: int):
        Epsi = 0.01
        src_node = self.g.get_graph().get_node(src)
        dest_node = self.g.get_graph().get_node(dest)
        src_x = src_node.pos[0]
        src_y = src_node.pos[1]
        dest_x = dest_node.pos[0]
        dest_y = dest_node.pos[1]

        m = (dest_y - src_y) / (dest_x - src_x)
        y1 = src_y - m * src_x
        return abs(y - (m * x + y1)) < Epsi

    def load_graph(self):

        graph_json = client.get_graph()
        graph = json.loads(
            graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        gra2 = DiGraph()

        for n in graph.Nodes:
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))

            x1 = n.pos.x
            y1 = n.pos.y
            id = n.id
            gra2.add_node(id, (x1, y1, 0))

        gra1 = DiGraph()

        self.min_x, self.min_y = gra2.get_min_x_y()
        self.max_x, self.max_y = gra2.get_max_x_y()

        for n in graph.Nodes:
            x1 = self.my_scale(n.pos.x, x=True)
            y1 = self.my_scale(n.pos.y, y=True)
            id = n.id
            gra1.add_node(id, (x1, y1, 0))

        for e in graph.Edges:
            src = next(n for n in graph.Nodes if n.id == e.src)
            dest = next(n for n in graph.Nodes if n.id == e.dest)
            weight = e.w

            gra1.add_edge(src.id, dest.id, weight)

        self.g = GraphAlgo(gra1)

    def drawArrowLine(self, win: pygame.surface, x1, y1, x2, y2):

        dx = x2 - x1
        dy = y2 - y1

        d = 15
        h = 5
        D = sqrt(dx * dx + dy * dy)

        xm = D - d
        xn = xm
        ym = h
        yn = -h

        sin = dy / D
        cos = dx / D
        x = xm * cos - ym * sin + x1
        ym = xm * sin + ym * cos + y1
        xm = x

        x = xn * cos - yn * sin + x1
        yn = xn * sin + yn * cos + y1
        xn = x

        points = ((x2, y2), (xm, ym), (xn, yn))

        pygame.draw.line(win, (0, 0, 139), (x1, y1), (x2, y2))
        pygame.draw.polygon(win, (0, 0, 139), points)

    def update_agent(self, a1: Agent, a2: Agent):
        a1.setSrc(a2.getSrc())
        a1.setDest(a2.getDest())
        a1.setSpeed(a2.getSpeed())
        a1.setPos(a2.getPos()[0], a2.getPos()[1], 0)
        a1.setValue(a2.getValue())

    def paint(self, window: pygame.Surface):
        for node in self.g.get_graph().get_all_v().values():
            x = int(node.get_pos()[0])
            y = int(node.get_pos()[1])
            node_img = pygame.image.load("Images/pokenode.png")
            node_img = pygame.transform.scale(node_img, (45, 45))
            window.blit(node_img, (x - 20, y - 20))

            # pygame.draw.circle(window, node.get_tag(), (node.get_pos()[0], node.get_pos()[1]), 15)
            id_srf = FONT.render(str(node.get_node_id()), True, Color(0, 0, 139))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)
            curr_nei = self.g.get_graph().all_out_edges_of_node(node.get_node_id())
            for nei in curr_nei.keys():
                node_nei = self.g.get_graph().get_node(nei)
                x_nei = node_nei.get_pos()[0]
                y_nei = node_nei.get_pos()[1]

                pygame.draw.line(window, (0, 0, 139), (x, y), (x_nei, y_nei))
                self.drawArrowLine(window, x, y, x_nei, y_nei)

        agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]

        for a in agents:
            x, y, _ = a.pos.split(',')
            pos_x = self.my_scale(float(x), x=True)
            pos_y = self.my_scale(float(y), y=True)
            a.pos = SimpleNamespace(x=float(x), y=float(y))
            agent = Agent(a.id, a.value, a.src, a.dest, a.speed, (a.pos.x, a.pos.y))
            for a2 in self.agents:
                if a2.getID() == agent.getID():
                    self.update_agent(a2, agent)
                    a_image = pygame.image.load("Images/ash.png")
                    a_image = pygame.transform.scale(a_image, (30, 30))
                    window.blit(a_image, (int(pos_x) - 20, int(pos_y) - 20))

                    break
        pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]

        for p in pokemons:
            x, y, _ = p.pos.split(',')
            pos_x = self.my_scale(float(x), x=True)
            pos_y = self.my_scale(float(y), y=True)
            p.pos = SimpleNamespace(x=float(x), y=float(y))
            pokemon = Pokemon(p.value, p.type, (p.pos.x, p.pos.y))
            for p2 in self.pokemons:
                if p2 == pokemon:
                    if 0 < p2.get_value() < 7:
                        p_image = pygame.image.load("Images/Charmander.png")
                    elif 7 <= p2.get_value() < 12:
                        p_image = pygame.image.load("Images/Charmilion.png")
                    else:
                        p_image = pygame.image.load("Images/Charizard.png")
                    p_val = str(p2.get_value())
                    text = FONT2.render(p_val, True, (255, 0, 0))
                    p_image = pygame.transform.scale(p_image, (30, 30))
                    window.blit(p_image, (int(pos_x) - 20, int(pos_y) - 20))
                    rect = text.get_rect(center=(pos_x - 20, pos_y - 20))
                    window.blit(text, rect)
        display.update()
        clock.tick(60)

    def check_if_poke_list_correct(self):
        pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]

        list = []
        for p in pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=float(x), y=float(y))
            pokemon = Pokemon(p.value, p.type, (p.pos.x, p.pos.y))
            if len(list) == 0:
                list.append(pokemon)
            if len(list) != 0:
                if self.duplicate_list2(pokemon, list):
                    list.append(pokemon)

        for p in list:
            flag = False
            if p not in self.pokemons:
                flag = True
            if flag:
                self.pokemons.append(p)
            for p2 in self.pokemons:
                flag2 = False
                if p2 not in list:
                    flag2 = True
                if flag2:
                    self.pokemons.remove(p2)
                    for a in self.agents:
                        for pk in a.pokemon_list:
                            if p2 == pk:
                                a.pokemon_list.remove(p2)

    def create_all_list_tuple_permutations(self, node_lst) -> {}:
        ret = {}
        i = 0
        for perm in list(itertools.permutations(node_lst)):
            ret[i] = perm
            i += 1
        return ret

    def check_agent_pos(self, agent: Agent):
        if agent.getDest() == -1:
            agent_pos1 = a.getSrc()
        else:
            agent_pos1 = a.getDest()

        return agent_pos1

    def game_info(self, current_time):
        info_dict = json.loads(client.get_info())
        info = info_dict['GameServer']
        moves_str = "moves: " + str(info['moves'])
        grade_str = "grade: " + str(info['grade'])
        level_str = "level: " + str(info['game_level'])
        time_str = "timer: " + str(current_time)
        f1 = FONT.render(moves_str, True, (0, 0, 0))
        f2 = FONT.render(grade_str, True, (0, 0, 0))
        f3 = FONT.render(level_str, True, (0, 0, 0))
        f4 = FONT.render(time_str, True, (0, 0, 0))
        rect = f1.get_rect(center=(screen.get_width() / 2 - 300, 20))
        screen.blit(f1, rect)
        rect = f2.get_rect(center=(screen.get_width() / 2 - 120, 20))
        screen.blit(f2, rect)
        rect = f3.get_rect(center=(screen.get_width() / 2 + 120, 20))
        screen.blit(f3, rect)
        rect = f4.get_rect(center=(screen.get_width() / 2 + 300, 20))
        screen.blit(f4, rect)
        button = FONT.render('stop', True, (200, 200, 200))
        rect = button.get_rect(center=(900, 672))
        pygame.draw.rect(screen, (255, 0, 0), (850, 650, 100, 50))
        screen.blit(button, rect)

    def load_everyone(self, win: pygame.surface):
        self.load_graph()
        self.load_pokemons()
        self.paint(win)
        self.check_if_poke_list_correct()

    def load_agents_best_pos(self):
        dict_info = json.loads(client.get_info())
        dict_in_info = dict_info['GameServer']
        moves = dict_in_info['moves']
        num_of_agents = dict_in_info['agents']
        self.load_graph()
        self.load_pokemons()
        list_pk = self.pokemons
        list = []
        len_pk = len(self.pokemons)
        for i in range(len_pk):
            pk = self.pokemons[i].get_edge()[0]
            list.append(pk)
            if i == num_of_agents:
                break
        for i in range(num_of_agents):
            if i < len(list):
                k = str(list[i])
                client.add_agent("{\"id\":" + k + "}")
            else:
                client.add_agent("{\"id\":" + str(i) + "}")

if __name__ == '__main__':
    pygame.init()
    screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
    clock = pygame.time.Clock()
    pygame.font.init()
    FONT = pygame.font.SysFont('Arial', 20, bold=True)
    FONT2 = pygame.font.SysFont('Arial', 12)
    game = Game()
    client = Client()
    client.start_connection(HOST, PORT)

    # dict_info = json.loads(client.get_info())
    # dict_in_info = dict_info['GameServer']
    # moves = dict_in_info['moves']
    # num_of_agents = dict_in_info['agents']
    # game.load_graph()
    # for i in range(num_of_agents):
    #     k = str(i)
    #     client.add_agent("{\"id\":" + k + "}")
    game.load_agents_best_pos()

    game.load_agents()
    client.start()
    moves = 0
    time = int(client.time_to_end()) / 1000

    while client.is_running() == 'true':
        game.load_everyone(screen)
        bg = pygame.image.load("Images/bg.png")
        screen.blit(bg, (0, 0))
        current_time = int(client.time_to_end()) / 1000
        game.game_info(current_time)

        for p in game.pokemons:
            min_time = 100000
            curr_path_list = []
            id = -1

            if p.is_coming():
                continue
            for a2 in game.agents:
                p_edge = p.get_edge()
                curr_path_len = len(a2.curr_path)
                for c in range(curr_path_len - 1):
                    v = a2.curr_path[c]
                    v2 = a2.curr_path[c + 1]
                    curr_edge = (v, v2)
                    if curr_edge == p_edge:
                        p.set_agent()
                        a2.pokemon_list.append(p)
                        break
                break
            if p.is_coming():
                continue
            for a in game.agents:

                agent_pos = game.check_agent_pos(a)

                if a.getDest() == -1 and len(a.pokemon_list) == 0:

                    path_dist, node_list_path = game.g.shortest_path(agent_pos, p.get_edge()[0])
                    node_list_path.append(p.get_edge()[1])
                    time_dist = path_dist / a.getSpeed()
                    if time_dist < min_time:
                        min_time = time_dist
                        id = a.getID()
                        curr_path_list = node_list_path

                if len(a.pokemon_list) > 0:
                    tup_list = []
                    for pa in a.pokemon_list:
                        tup_list.append(pa.get_edge())
                    range_tup = len(tup_list)
                    tup_list = list(dict.fromkeys(tup_list))

                    p_edge = p.get_edge()
                    is_in = False
                    if p_edge in tup_list:
                        is_in = True
                    if not is_in:
                        tup_list.append(p_edge)
                    if is_in:
                        a.pokemon_list.append(p)
                        p.set_agent()
                        continue

                    perm_dict = game.create_all_list_tuple_permutations(tup_list)
                    for i in perm_dict.values():
                        tup_list2 = i
                        dist_sum = 0
                        path = []
                        for a2 in range(len(tup_list) - 1):
                            v = (tup_list2[a2])[1]
                            v2 = (tup_list2[a2 + 1])[0]
                            path2 = []
                            path2.append((tup_list2[a2])[0])
                            (sum, path3) = game.g.shortest_path(v, v2)
                            range_path3 = len(path3)
                            for pa in range(range_path3):
                                path2.append(path3[0])
                                path3.remove(path3[0])
                            path2.append((tup_list2[a2 + 1])[1])
                            dist_sum = dist_sum + sum
                            range_path2 = len(path2)
                            for pa2 in range(range_path2):
                                path.append(path2[0])
                                path2.remove(path2[0])
                        total_path = []
                        if agent_pos != path[0]:
                            agent_dist_sum, agent_path = game.g.shortest_path(agent_pos, path[0])
                            range_path = len(path)
                            for pa2 in range(range_path):
                                agent_path.append(path[0])
                                path.remove(path[0])
                            range_path2 = len(agent_path)
                            for pa2 in range(range_path2):
                                total_path.append(agent_path[0])
                                agent_path.remove(agent_path[0])
                            total_sum = agent_dist_sum + dist_sum
                            time_dist = total_sum / a.getSpeed()
                        else:
                            range_path = len(path)
                            for pa2 in range(range_path):
                                total_path.append(path[0])
                                path.remove(path[0])
                            total_sum = dist_sum
                            time_dist = total_sum / a.getSpeed()
                        if time_dist < min_time:
                            min_time = time_dist
                            id = a.getID()
                            curr_path_list = total_path

            if id != -1:
                p.set_agent()

            for agent in game.agents:
                if id == agent.getID():
                    agent.pokemon_list.append(p)
                    agent.curr_path = curr_path_list
                    break

        for agent in game.agents:
            if agent.curr_path is None or len(agent.curr_path) == 0 or len(agent.pokemon_list) == 0:
                continue
            first_id = agent.curr_path[0]
            agent.prev = first_id
            if agent.getDest() == -1 and len(agent.curr_path) > 0:
                agent.curr_path.remove(agent.curr_path[0])
                if len(agent.curr_path) == 0 or len(agent.pokemon_list) == 0:
                    continue
                first_id = agent.curr_path[0]
                client.choose_next_edge('{"agent_id":' + str(agent.getID()) + ', "next_node_id":' + str(first_id) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

        if moves < (time - current_time) * 10:
            client.move()
            moves = moves + 1

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 850 < mouse_pos[0] < 950 and 627 < mouse_pos[1] < 690:
                    client.stop_connection()
                    exit(0)
