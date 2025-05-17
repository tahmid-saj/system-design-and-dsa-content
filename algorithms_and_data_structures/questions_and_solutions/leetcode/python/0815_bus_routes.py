class Solution:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        return self.stationAsNode(routes, source, target)

    def stationAsNode(self, routes, source, target):
        # convert routes to adjList containing station: bus number
        # use a queue to perform bfs
        # in BFS: if a station is encountered that is target: return busesTaken
        #         if a station is encountered that has a bus not in visited, add all the stations (busesTaken + 1) for that bus in the queue and add the bus to visited
        adjList = {}
        for i in range(len(routes)):
            for s in routes[i]:
                if s not in adjList: adjList[s] = []
                adjList[s].append(i)
        
        queue = deque([(source, 0)])
        visited = set()

        while queue:
            station, busesTaken = queue.popleft()
            if station == target: return busesTaken

            if station in adjList:
                for bus in adjList[station]:
                    if bus not in visited:
                        for s in routes[bus]: queue.append((s, busesTaken + 1))
                        visited.add(bus)
        
        return -1