import sys
def tsp(distances):
    numCities = len(distances)
    tour = [0]
    visited = set([0])

    currentCity = 0
    totalDistance = 0

    while len(visited)<numCities:
        min = sys.maxsize
        nearestCity = None
        for next in range (numCities):
            if(next not in visited and distances[currentCity][next]<min):
                min = distances[currentCity][next]
                nearestCity = next
        tour.append(nearestCity)
        visited.add(nearestCity)
        totalDistance += min
        currentCity = nearestCity
    tour.append(0)
    totalDistance += distances[currentCity][0]
    return tour, totalDistance

distances = [
    [0,4,8,9,12],
    [4,0,6,8,9],
    [8,6,0,10,11],
    [9,8,10,0,7],
    [12,9,11,7,0]
]

tour, totalDistance = tsp(distances)

print("Path is:",tour)
print("Total distance:",totalDistance)
