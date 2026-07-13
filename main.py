import pygame
import sys
from road import Road
from intersection import Intersection
from roadNetwork import RoadNetwork
from car import Car
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 250)
BLUE = (60, 100, 255)
ORANGE = (255, 153, 0)
BLACK = (0, 0, 0)
GREY = (90, 90, 90)
LIGHTER_GREY = (110,110,110)

PLACER_SIZE = 80

PLACEMENT_ITEMS = ["road", "intersection"]

PLACEMENT_ITEM_SIZE = 60
PLACEMENT_MARGIN = 20

ROAD_SIZE = 20

GRID_SIZE = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

#RoadNetwork([{"entrance": 0,"exit": 100},{"entrance": 1,"exit": 102}],[{"entrance": 101,"exit": 5},{"entrance": 103,"exit": 6}],[Road([0,290],[440,20],"east", 0, 10, 100),Road([440,0],[20,290],"north", 10, 5, 101),Road([460,290],[340,20],"west", 1, 10, 102),Road([440,310],[20,290],"south", 10, 6, 103)],[Intersection([440,290], [20,20], "4-way", [100,102], [101,103], 10)])

roadNetwork = RoadNetwork([{"entrance": 0,"exit": 100},{"entrance": 1,"exit": 101}],[{"entrance": 102,"exit": 5},{"entrance": 103,"exit": 6}],[Road([0,200],[50,20],"east", 0, -1, 100),Road([750,280],[50,20],"west", 1, -1, 101),Road([0,280],[50,20],"west", -1, 5, 102),Road([750,200],[50,20],"east", -1, 6, 103)])
cars = []

def main():
    clock = pygame.time.Clock()
    running = True

    carIdCount = 0
    entranceIdCount = 2
    exitIdCount = 7
    intersectionIdCount = 10
    roadIdCount = 104

    gamePlaying = False
    selectedItem = ""

    roadStart = [-1,-1]

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if(gamePlaying):
                        cars.append(Car(roadNetwork, carIdCount))
                        carIdCount += 1
                elif event.key == pygame.K_1:
                    gamePlaying = not(gamePlaying)
                    configureIdsAndPath()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # event.button: 1 = Left, 2 = Middle, 3 = Right
                if event.button == 1: 
                    if(event.pos[1] > HEIGHT - PLACER_SIZE):
                        for i, item in enumerate(PLACEMENT_ITEMS):
                            if(clicked_on_rect(event.pos, [PLACEMENT_MARGIN + (PLACEMENT_MARGIN + PLACEMENT_ITEM_SIZE)*i, HEIGHT - PLACER_SIZE + (PLACER_SIZE - PLACEMENT_ITEM_SIZE)/2], [PLACEMENT_ITEM_SIZE,PLACEMENT_ITEM_SIZE])):
                                selectedItem = item
                    elif(selectedItem == "road"):
                        gridMousePos = [round(event.pos[0]/GRID_SIZE)*GRID_SIZE,round(event.pos[1]/GRID_SIZE)*GRID_SIZE]
                        if(roadStart[0] == -1):
                            roadStart = [gridMousePos[0] - ROAD_SIZE/2,gridMousePos[1] - ROAD_SIZE/2]
                        else:
                            if(abs(roadStart[0] - gridMousePos[0]) > abs(roadStart[1] - gridMousePos[1])):
                                if(roadStart[0] - gridMousePos[0] <= 0):
                                    roadNetwork.roads.append(Road([roadStart[0],roadStart[1]],[gridMousePos[0]-roadStart[0],ROAD_SIZE], "east", -1, -1, roadIdCount))
                                else:
                                    roadNetwork.roads.append(Road([gridMousePos[0],roadStart[1]],[roadStart[0]-gridMousePos[0]+ROAD_SIZE,ROAD_SIZE], "west", -1, -1, roadIdCount))
                            else:
                                if(roadStart[1] - gridMousePos[1] <= 0):
                                    roadNetwork.roads.append(Road([roadStart[0],roadStart[1]],[ROAD_SIZE,gridMousePos[1]-roadStart[1]], "south", -1, -1, roadIdCount))
                                else:
                                    roadNetwork.roads.append(Road([roadStart[0],gridMousePos[1]],[ROAD_SIZE,roadStart[1]-gridMousePos[1]+ROAD_SIZE], "north", -1, -1, roadIdCount))
                            roadIdCount += 1
                            roadStart = [-1,-1]
                    elif(selectedItem == "intersection"):
                        gridMousePos = [round(event.pos[0]/GRID_SIZE)*GRID_SIZE,round(event.pos[1]/GRID_SIZE)*GRID_SIZE]
                        roadNetwork.intersections.append(Intersection([gridMousePos[0] -ROAD_SIZE/2 ,gridMousePos[1]-ROAD_SIZE/2],[ROAD_SIZE,ROAD_SIZE], "none", [], [], intersectionIdCount))
                        intersectionIdCount += 1
                elif event.button == 3:
                    roadStart = [-1,-1] 

        if(gamePlaying):
            updateCars()

        draw(selectedItem, roadStart, [round(pygame.mouse.get_pos()[0]/GRID_SIZE)*GRID_SIZE,round(pygame.mouse.get_pos()[1]/GRID_SIZE)*GRID_SIZE])

def draw(selectedItem, roadStart, mousePos):
    screen.fill(LIGHT_BLUE)

    pygame.draw.rect(screen, BLUE, pygame.Rect(0, HEIGHT - PLACER_SIZE, WIDTH, PLACER_SIZE))

    roadNetwork.draw(screen)

    drawPlacementItems()

    drawSelectedItem(selectedItem, roadStart, mousePos)

    for i,car in enumerate(cars):
        car.draw(screen)

    pygame.display.flip()

def drawPlacementItems():
    for i,item in enumerate(PLACEMENT_ITEMS):
        pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(PLACEMENT_MARGIN + (PLACEMENT_MARGIN + PLACEMENT_ITEM_SIZE)*i, HEIGHT - PLACER_SIZE + (PLACER_SIZE - PLACEMENT_ITEM_SIZE)/2, PLACEMENT_ITEM_SIZE, PLACEMENT_ITEM_SIZE))

def drawSelectedItem(selectedItem, roadStart, mousePos):
    if(selectedItem == "intersection"):
        drawTransparentRect(screen, GREY, pygame.Rect(mousePos[0] -ROAD_SIZE/2 ,mousePos[1]-ROAD_SIZE/2,ROAD_SIZE,ROAD_SIZE),180)
    elif(selectedItem == "road"):
        if(roadStart[0] == -1):
            drawTransparentRect(screen, GREY, pygame.Rect(mousePos[0] -ROAD_SIZE/2 ,mousePos[1]-ROAD_SIZE/2,ROAD_SIZE,ROAD_SIZE),180)
        else:
            if(abs(roadStart[0] - mousePos[0]) > abs(roadStart[1] - mousePos[1])):
                if(roadStart[0] - mousePos[0] <= 0):
                    drawTransparentRect(screen, GREY, pygame.Rect(roadStart[0],roadStart[1],mousePos[0]-roadStart[0],ROAD_SIZE),180)
                else:
                    drawTransparentRect(screen, GREY, pygame.Rect(mousePos[0],roadStart[1],roadStart[0]-mousePos[0]+ROAD_SIZE,ROAD_SIZE),180)
            else:
                if(roadStart[1] - mousePos[1] <= 0):
                    drawTransparentRect(screen, GREY, pygame.Rect(roadStart[0],roadStart[1],ROAD_SIZE,mousePos[1]-roadStart[1]),180)
                else:
                    drawTransparentRect(screen, GREY, pygame.Rect(roadStart[0],mousePos[1],ROAD_SIZE,roadStart[1]-mousePos[1]+ROAD_SIZE),180)

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

def clicked_on_rect(mouse_pos, rect_pos, rect_size):
    return (
        rect_pos[0] <= mouse_pos[0] <= rect_pos[0] + rect_size[0] and
        rect_pos[1] <= mouse_pos[1] <= rect_pos[1] + rect_size[1]
    )

def drawTransparentRect(screen, color, rect, alpha):
    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surf.fill((*color, alpha))
    screen.blit(surf, rect.topleft)

def configureIdsAndPath():
    for i,activeRoad in enumerate(roadNetwork.roads):
        for i,road in enumerate(roadNetwork.roads):
            if(activeRoad.direction == "east"):
                if(clicked_on_rect([activeRoad.pos[0]-5,activeRoad.pos[1]+10],road.pos,road.size)):
                    activeRoad.entrance = road.id
                if(clicked_on_rect([activeRoad.pos[0]+activeRoad.size[0]+5,activeRoad.pos[1]+10],road.pos,road.size)):
                    print(f"{activeRoad.id}, {road.id}")
                    activeRoad.exit = road.id
            elif(activeRoad.direction == "west"):
                if(clicked_on_rect([activeRoad.pos[0]+activeRoad.size[0]+5,activeRoad.pos[1]+10],road.pos,road.size)):
                    activeRoad.entrance = road.id
                if(clicked_on_rect([activeRoad.pos[0]-5,activeRoad.pos[1]+10],road.pos,road.size)):
                    activeRoad.exit = road.id
            elif(activeRoad.direction == "north"):
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]-5],road.pos,road.size)):
                    activeRoad.entrance = road.id
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]+activeRoad.size[1]+5],road.pos,road.size)):
                    activeRoad.exit = road.id
            elif(activeRoad.direction == "south"):
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]+activeRoad.size[1]+5],road.pos,road.size)):
                    activeRoad.entrance = road.id
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]-5],road.pos,road.size)):
                    activeRoad.exit = road.id
        for i,intersection in enumerate(roadNetwork.intersections):
            if(activeRoad.direction == "east"):
                if(clicked_on_rect([activeRoad.pos[0]-5,activeRoad.pos[1]+10],intersection.pos,intersection.size)):
                    activeRoad.entrance = intersection.id
                if(clicked_on_rect([activeRoad.pos[0]+activeRoad.size[0]+5,activeRoad.pos[1]+10],intersection.pos,intersection.size)):
                    activeRoad.exit = intersection.id
            elif(activeRoad.direction == "west"):
                if(clicked_on_rect([activeRoad.pos[0]+activeRoad.size[0]+5,activeRoad.pos[1]+10],intersection.pos,intersection.size)):
                    activeRoad.entrance = intersection.id
                if(clicked_on_rect([activeRoad.pos[0]-5,activeRoad.pos[1]+10],intersection.pos,intersection.size)):
                    activeRoad.exit = intersection.id
            elif(activeRoad.direction == "south"):
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]-5],intersection.pos,intersection.size)):
                    activeRoad.entrance = intersection.id
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]+activeRoad.size[1]+5],intersection.pos,intersection.size)):
                    activeRoad.exit = intersection.id
            elif(activeRoad.direction == "north"):
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]+activeRoad.size[1]+5],intersection.pos,intersection.size)):
                    activeRoad.entrance = intersection.id
                if(clicked_on_rect([activeRoad.pos[0]+10,activeRoad.pos[1]-5],intersection.pos,intersection.size)):
                    activeRoad.exit = intersection.id
    for i,activeIntersection in enumerate(roadNetwork.intersections):
        for i,road in enumerate(roadNetwork.roads):
            if(road.direction == "west"):
                if(clicked_on_rect([road.pos[0]-5,road.pos[1]+10],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.entrances.append(road.id)
                if(clicked_on_rect([road.pos[0]+road.size[0]+5,road.pos[1]+10],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.exits.append(road.id)
            elif(road.direction == "east"):
                if(clicked_on_rect([road.pos[0]+road.size[0]+5,road.pos[1]+10],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.entrances.append(road.id)
                if(clicked_on_rect([road.pos[0]-5,road.pos[1]+10],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.exits.append(road.id)
            elif(road.direction == "north"):
                if(clicked_on_rect([road.pos[0]+10,road.pos[1]-5],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.entrances.append(road.id)
                if(clicked_on_rect([road.pos[0]+10,road.pos[1]+road.size[1]+5],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.exits.append(road.id)
            elif(road.direction == "south"):
                if(clicked_on_rect([road.pos[0]+10,road.pos[1]+road.size[1]+5],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.entrances.append(road.id)
                if(clicked_on_rect([road.pos[0]+10,road.pos[1]-5],activeIntersection.pos,activeIntersection.size)):
                    activeIntersection.exits.append(road.id)
    for i,road in enumerate(roadNetwork.roads):
        print(f"{road}, {road.entrance}, {road.exit}, {road.id}")
    for i,intersection in enumerate(roadNetwork.intersections):
        print(f"{intersection}, {intersection.entrances}, {intersection.exits}, {intersection.id}")
    roadNetwork.initialiseNetworkPaths()

if __name__ == "__main__":
    main()

# Cleanup
pygame.quit()
sys.exit()