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
FPS = 60

WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 250)
ORANGE = (255, 153, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

roadNetwork = RoadNetwork([{"entrance": 0,"exit": 100}],[{"entrance": 101,"exit": 5},{"entrance": 102,"exit": 6},{"entrance": 103,"exit": 7}],[Road([0,290],[390,20],"east", 0, 10, 100),Road([390,0],[20,290],"north", 10, 5, 101),Road([410,290],[390,20],"east", 10, 6, 102),Road([390,310],[20,290],"south", 10, 7, 103)],[Intersection([390,290], [20,20], "4-way", [100], [101,102,103], 10)])
cars = []

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    cars.append(Car(roadNetwork))

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
        car.move()
        if(car.pathIndex > len(car.path["path"])-1):
            cars.pop(i)
    


if __name__ == "__main__":
    main()

# Cleanup
pygame.quit()
sys.exit()