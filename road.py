import pygame

GREY = (90, 90, 90)

class Road:
    def __init__(self, pos, size, direction, enterance, exit, id):
        self.pos = pos
        self.size = size
        self.direction = direction
        self.enterance = enterance
        self.exit = exit
        self.id = id

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1]))