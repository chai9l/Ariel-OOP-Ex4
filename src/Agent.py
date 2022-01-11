
from Pokemon import Pokemon


class Agent:

    def __init__(self,id : int ,value : float ,src: int,dest : int,speed: float, pos: tuple):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.curr_path = []
        self.pokemon_list = []


    def getID(self):
        return self.id

    def getValue(self) -> float:
        return self.value

    def setValue(self, value: float):
        self.value = value

    def getSrc(self):
        return self.src

    def setSrc(self, src):
        self.src = src

    def getDest(self):
        return self.dest

    def setDest(self, dest: int):
        self.dest = dest

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed :float):
        self.speed = speed


    def setPos(self, x, y, z):
        self.pos = (x, y, z)

    def getPos(self):
        return self.pos

    def add_pokemon(self, pk):
        self.pokemon_list.append(pk)

    def remove_pokemon(self,pk):
        self.pokemon_list.remove(pk)

