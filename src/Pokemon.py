
class Pokemon:

    def __init__(self,value: float=None,type: int=None,pos: tuple=None):
        self.value = value
        self.type = type
        self.pos = pos
        self.edge = tuple
        self.agent_inc = False
        self.picked = False
        self.start_on = False

    def __eq__(self, other):
        if self.value == other.value and self.type == other.type and self.pos == other.pos:
            return True
        return False

    def get_start_on(self):
        return self.start_on

    def set_start_on(self, b: bool):
        self.start_on = b

    def get_edge(self):
        return self.edge

    def set_edge(self,edge):
        self.edge = edge

    def set_value(self,value):
        self.value = value

    def set_type(self,type):
        self.type = type

    def set_pos(self,pos):
        self.pos = pos

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def get_pos(self):
        return self.pos

    def set_agent(self):
        self.agent_inc = True

    def is_coming(self):
        return self.agent_inc

