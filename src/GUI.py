import json
from idlelib import window
from math import sqrt
from types import SimpleNamespace

import pygame
from pygame import *
from pygame import gfxdraw

from GraphAlgo import GraphAlgo
from Agent import Agent
from client import Client
from Game import Game, FONT, screen, game
from Pokemon import Pokemon


class GUI:

    def __init__(self, client: Client, algo: GraphAlgo):
        self.width, self.height = 800, 659
        self.client = client
        self.window = pygame.display.set_mode((self.width, self.height), depth=32, flags=RESIZABLE)
        pygame.font.init()
        pygame.display.set_caption("Pokemon Game")
        self.algo = algo

    def load_and_draw(self, game: Game):
        pos = pygame.mouse.get_pos()
        bg_pic

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

    def draw_everything(self, game: Game):
        back_ground = pygame.image.load("Images/background.png")
        self.window.blit(back_ground, 0, 0)
        self.draw_graph(self.window)
        self.draw_agents(game)
        self.draw_pokemons(game)

    def draw_graph(self, window: pygame.Surface):
        for node in self.algo.get_graph().get_all_v().values():
            x = int(node.get_pos()[0])
            y = int(node.get_pos()[1])
            pygame.draw.circle(window, node.get_tag(), (node.get_pos()[0], node.get_pos()[1]), 15)
            id_srf = FONT.render(str(node.get_node_id()), True, Color(0, 0, 139))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)
            curr_nei = self.algo.get_graph().all_out_edges_of_node(node.get_node_id())
            for nei in curr_nei.keys():
                node_nei = self.algo.get_graph().get_node(nei)
                x_nei = node_nei.get_pos()[0]
                y_nei = node_nei.get_pos()[1]

                pygame.draw.line(window, (0, 0, 139), (x, y), (x_nei, y_nei))
                self.drawArrowLine(window, x, y, x_nei, y_nei)

    def draw_pokemons(self, game: Game):
        game.load_pokemons()
        font = pygame.font.SysFont('Arial', 12)
        for p in game.pokemons:
            p_value = str(p.get_value())
            text = font.render(p_value, True, (255, 0, 0))
            if 0 < p.get_value() < 10:
                p_image = pygame.image.load("Images/Charmander.png")
            elif 10 < p.get_value() < 15:
                p_image = pygame.image.load("Images/Charmilion.png")
            else:
                p_image = pygame.image.load("Images/Charizard.png")
            self.window.blit(p_image, p.get_pos()[0], p.get_pos()[1])
            rect = text.get_rect(center=(p.get_pos()[0] - 15, p.get_pos()[1] - 15))
            self.window.blit(text, rect)

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    def my_scale(self, data, x=False, y=False, ):
        if x:
            return self.scale(data, 50, screen.get_width() - 50, game.min_x, game.max_x)
        if y:
            return self.scale(data, 50, screen.get_height() - 50, game.min_y, game.max_y)

    def draw_agents(self, game: Game):
        game.load_agents()
        font = pygame.font.SysFont('Arial', 12)
        for a in game.agents:
            x, y, _ = a.pos.split(',')
            scaled_x = self.my_scale(a.pos.x, x=True)
            scaled_y = self.my_scale(a.pos.y, y=True)
            a.pos = SimpleNamespace(x=float(x), y=float(y))
            agent = Agent(a.id, a.value, a.src, a.dest, a.speed, (a.pos.x, a.pos.y))
            for a2 in game.agents:
                if a2.getID() == agent.getID():
                    game.update_agent(a2, agent)

                    t1 = font.render(str(a.id), True, (0, 0, 0))
                    agent_image = pygame.image.load("Images/ash.png")

                    self.window.blit(agent_image, (int(scaled_x), int(scaled_y)))
                    rect = t1.get_rect(center=(int(scaled_x), int(scaled_y)))
                    self.window.blit(t1, rect)
                    break
