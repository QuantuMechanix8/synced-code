import random
from math import *

def readCities(fileName):
    f = open(fileName, "r")
    cities = []
    for line in f.readlines():
        line = line.strip("\n").split(",")
        line[2], line[3] = float(line[2]), float(line[3])
        cities.append(tuple(line))
    f.close()
    return cities

def distance(lat1degrees, long1degrees, lat2degrees, long2degrees):

    earth_radius = 6371  # Kilometres (imaigne using imperial units - WACK)
    lat1 = radians(lat1degrees)
    long1 = radians(long1degrees)
    lat2 = radians(lat2degrees)
    long2 = radians(long2degrees)
    lat_difference = lat2 - lat1
    long_difference = long2 - long1
    sin_half_lat = sin(lat_difference / 2)
    sin_half_long = sin(long_difference / 2)
    a = sin_half_lat ** 2 + cos(lat1) * cos(lat2) * sin_half_long ** 2
    c = 2 * atan2(sqrt(a), sqrt(1.0 - a))
    return earth_radius * c

def outputCities(roadMap):
    for line in roadMap:
        line = list(line)
        line[2], line[3] = round(float(line[2]), 2), round(float(line[3]), 2)
        print(line)
    
def totalDistance(roadMap):
    totalDistance = 0
    for i, city in enumerate(roadMap):
        totalDistance += distance(roadMap[i-1][2], roadMap[i-1][3], city[2], city[3])
    return totalDistance

def swapAdjCities(roadMap, index):
    roadMap[index], roadMap[index+1] = roadMap[index+1], roadMap[index]
    return roadMap

def swapCities(roadMap, index1, index2):
    index1, index2 = int(index1), int(index2)
    if not(index1 == index2):
        roadMap[index1], roadMap[index2] = roadMap[index2], roadMap[index1]
    return roadMap

def findBestCycle(roadMap, swaps):
    print(f"the original distance is {round(totalDistance(roadMap), 2)}")
    currentPath = roadMap
    for i in range(swaps):
        num1, num2 = random.randint(0,49), random.randint(0,49)
        currentDist = totalDistance(currentPath)
        newDist = totalDistance(swapCities(currentPath.copy(), num1, num2))
        if (currentDist > newDist):
            currentPath = swapCities(currentPath, num1, num2)

    print(f"total distance is now {round(totalDistance(currentPath), 2)}km, for the roadmap")
    return currentPath

def main():
    roadMap = readCities("cityData.txt")
    roadMap = findBestCycle(roadMap, 10000)

main()

