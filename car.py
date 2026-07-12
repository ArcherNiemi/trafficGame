import pygame
import random
from intersection import Intersection

ORANGE = (255, 153, 0)
SIZE = [16,16]
MAX_SPEED = 5

class Car:
    def __init__(self, roadNetwork, color=-1, entrance=-1, exit=-1):
        self.size = SIZE
        if(color == -1):
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        else:
            self.color = color
        self.pos = [roadNetwork.roads[0].pos[0] - SIZE[0], roadNetwork.roads[0].pos[1] + 2]
        self.speed = MAX_SPEED
        if(color == -1):
            self.entrance = getRandomIndex(roadNetwork.entrances)["entrance"]
        else:
            self.entrance = entrance
        if(color == -1):
            self.exit = getRandomIndex(roadNetwork.exits)["exit"]
        else:
            self.exit = exit
        self.path = self.pathfind(roadNetwork)
        print(self.path)
        self.pathIndex = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1]))

    def move(self):
        if(self.path["path"][self.pathIndex].direction == "north"):
            self.pos[1] -= self.speed
        elif(self.path["path"][self.pathIndex].direction == "south"):
            self.pos[1] += self.speed
        elif(self.path["path"][self.pathIndex].direction == "west"):
            self.pos[0] -= self.speed
        elif(self.path["path"][self.pathIndex].direction == "east"):
            self.pos[0] += self.speed
        self.updatePathPart()
        
    
    def updatePathPart(self):
        currectPathPart = self.path["path"][self.pathIndex]
        if(currectPathPart.direction == "north"):
            if(self.pos[1] + self.size[1] < currectPathPart.pos[1]):
                self.pathIndex += 1
        elif(currectPathPart.direction == "south"):
            if(self.pos[1] > currectPathPart.pos[1] + currectPathPart.size[1]):
                self.pathIndex += 1
        elif(currectPathPart.direction == "west"):
            if(self.pos[0] - self.size[0] < currectPathPart.pos[0]):
                self.pathIndex += 1
        elif(currectPathPart.direction == "east"):
            if(self.pos[0] > currectPathPart.pos[0] + currectPathPart.size[0]):
                self.pathIndex += 1
        if(self.pathIndex > len(self.path["path"]) - 1):
            return
        currectPathPart = self.path["path"][self.pathIndex]
        if(type(currectPathPart) == Intersection):
            self.pathIndex += 1

    def pathfind(self,roadNetwork):
        paths = roadNetwork.paths
        return next((path for path in paths if path["entrance"] == self.entrance and path["exit"] == self.exit), None)

def getRandomIndex(list):
    randomNum = random.randint(0,len(list)-1)
    return list[randomNum]