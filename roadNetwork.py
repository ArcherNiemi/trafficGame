import random

#id: 0-4 are entrances, id: 5-9 are exits, id: 10-99 are intersections and id: 100+ are roads

class RoadNetwork:
    def __init__(self, entrances=[], exits=[], roads=[], intersections=[]):
        self.entrances = entrances
        self.exits = exits
        self.roads = roads
        self.intersections = intersections
        self.paths = []

    def draw(self, screen):
        for i,road in enumerate(self.roads):
            road.draw(screen)
        for i,intersection in enumerate(self.intersections):
            intersection.draw(screen)

    def initialiseNetworkPaths(self):
        self.paths = self.createPaths()

    def createPaths(self):
        paths = []
        entrancesAndExits = []
        for i in range(100000):
            path = self.createPath()
            if(not([path["entrance"],path["exit"]] in entrancesAndExits)):
                paths.append(path)
                entrancesAndExits.append([path["entrance"],path["exit"]])
        print(paths)
        return paths
    
    def createPath(self):
        entrance = getRandomIndex(self.entrances)
        pathPart = self.getId(entrance["exit"])
        path = []
        currentId = entrance["exit"]
        count = 0
        while(not(currentId >= 5 and currentId <= 9) and count < 100):
            path.append(pathPart)
            currentId = pathPart.id
            if(currentId >= 100):
                if(pathPart.exit >= 5 and pathPart.exit <= 9):
                    currentId = pathPart.exit
                else:
                    pathPart = self.getId(pathPart.exit)
            else:
                pathPart = self.getId(getRandomIndex(pathPart.exits))
            count += 1
        return {"path": path, "entrance": entrance["entrance"], "exit": currentId}


    def getId(self, id):
        if(id <= 99):
            for i,intersection in enumerate(self.intersections):
                if(id == intersection.id):
                    return intersection
        else:
            for i,road in enumerate(self.roads):
                if(id == road.id):
                    return road
        return -1

def getRandomIndex(list):
    randomNum = random.randint(0,len(list)-1)
    return list[randomNum]
