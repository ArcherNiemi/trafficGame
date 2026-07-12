import pygame
import random
from intersection import Intersection

ORANGE = (255, 153, 0)
SIZE = [16,16]
MAX_SPEED = 5
ACCELERATION = 1


class Car:
    def __init__(self, roadNetwork, id, color=-1, entrance=-1, exit=-1):
        self.size = SIZE
        if(color == -1):
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        else:
            self.color = color
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
        self.roadNetwork = roadNetwork

        if(self.path["path"][0].direction == "east"):
            self.pos = [self.path["path"][0].pos[0] - SIZE[0], self.path["path"][0].pos[1] + 2]
        elif(self.path["path"][0].direction == "west"):
            self.pos = [self.path["path"][0].pos[0] + self.path["path"][0].size[0] + SIZE[0], self.path["path"][0].pos[1] + 2]
        
        self.id = id

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1]))

    def move(self, cars, usedIntersections):
        tempPos = [self.pos[0], self.pos[1]]
        if(not(self.speed + ACCELERATION > MAX_SPEED)):
            self.speed += ACCELERATION
        if(self.path["path"][self.pathIndex].direction == "north"):
            tempPos[1] -= self.speed
        elif(self.path["path"][self.pathIndex].direction == "south"):
            tempPos[1] += self.speed
        elif(self.path["path"][self.pathIndex].direction == "west"):
            tempPos[0] -= self.speed
        elif(self.path["path"][self.pathIndex].direction == "east"):
            tempPos[0] += self.speed
        if(not(self.isCarWithinInWay(tempPos,cars)) and self.notMovingintoUsedIntersection(tempPos, usedIntersections)):
            self.pos = tempPos
        else:
            self.speed = 0
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
            if(self.pos[0] + self.size[0] < currectPathPart.pos[0]):
                self.pathIndex += 1
        elif(currectPathPart.direction == "east"):
            if(self.pos[0] > currectPathPart.pos[0] + currectPathPart.size[0]):
                self.pathIndex += 1
        if(self.pathIndex > len(self.path["path"]) - 1):
            return
        currectPathPart = self.path["path"][self.pathIndex]
        if(type(currectPathPart) == Intersection):
            self.pathIndex += 1

    def isCarWithinInWay(self, pos, cars):
        for i,car in enumerate(cars):
            if(rects_overlap(car.pos, car.size, pos, self.size) and car != self):
                return True
        return False
    
    def notMovingintoUsedIntersection(self, pos, usedIntersections):
        if(len(self.path["path"]) > self.pathIndex + 1):
            if(type(self.path["path"][self.pathIndex + 1]) == Intersection):
                usedIntersectionIds = [sublist[0] for sublist in usedIntersections]
                if(not([self.path["path"][self.pathIndex + 1].id, self.id] in usedIntersections) and 
                   self.path["path"][self.pathIndex + 1].id in usedIntersectionIds and 
                   rects_overlap(self.path["path"][self.pathIndex + 1].pos, self.path["path"][self.pathIndex + 1].size, pos, self.size)):
                    return False
        return True

    def pathfind(self,roadNetwork):
        paths = roadNetwork.paths
        return next((path for path in paths if path["entrance"] == self.entrance and path["exit"] == self.exit), None)

def getRandomIndex(list):
    randomNum = random.randint(0,len(list)-1)
    return list[randomNum]

def rects_overlap(pos1, size1, pos2, size2):
    return (
        pos1[0] < pos2[0] + size2[0] and
        pos1[0] + size1[0] > pos2[0] and
        pos1[1] < pos2[1] + size2[1] and
        pos1[1] + size1[1] > pos2[1]
    )