import pygame
import sys
from road import Road
from intersection import Intersection
from roadNetwork import RoadNetwork
from car import Car

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 250)
ORANGE = (255, 153, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

roadNetwork = RoadNetwork([{"entrance": 0,"exit": 100},{"entrance": 1,"exit": 102}],[{"entrance": 101,"exit": 5},{"entrance": 103,"exit": 6}],[Road([0,290],[440,20],"east", 0, 10, 100),Road([440,0],[20,290],"north", 10, 5, 101),Road([460,290],[340,20],"west", 1, 10, 102),Road([440,310],[20,290],"south", 10, 6, 103)],[Intersection([440,290], [20,20], "4-way", [100,102], [101,103], 10)])
cars = []

def main():
    clock = pygame.time.Clock()
    running = True
    carIdCount = 0

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    cars.append(Car(roadNetwork, carIdCount))
                    carIdCount += 1

        updateCars()

        draw()

def draw():
    screen.fill(LIGHT_BLUE)

    roadNetwork.draw(screen)

    for i,car in enumerate(cars):
        car.draw(screen)

    pygame.display.flip()

def updateCars():
    for i,car in enumerate(cars):
        usedIntersections = findUsedIntersections()
        car.move(cars,usedIntersections)
        if(car.pathIndex > len(car.path["path"])-1):
            cars.pop(i)

def findUsedIntersections():
    usedIntersections = []
    for i,intersection in enumerate(roadNetwork.intersections):
        for i,car in enumerate(cars):
            if(rects_overlap(car.pos, car.size, intersection.pos, intersection.size)):
                usedIntersections.append([intersection.id, car.id])
    return usedIntersections

def rects_overlap(pos1, size1, pos2, size2):
    return (
        pos1[0] < pos2[0] + size2[0] and
        pos1[0] + size1[0] > pos2[0] and
        pos1[1] < pos2[1] + size2[1] and
        pos1[1] + size1[1] > pos2[1]
    )

if __name__ == "__main__":
    main()

# Cleanup
pygame.quit()
sys.exit()