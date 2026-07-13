import pygame

LIGHTER_GREY = (110,110,110)

class Intersection:
    def __init__(self, pos, size, type, entrances, exits, id):
        self.pos = pos
        self.size = size
        self.type = type
        self.entrances = entrances
        self.exits = exits
        self.id = id

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHTER_GREY, pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1]))