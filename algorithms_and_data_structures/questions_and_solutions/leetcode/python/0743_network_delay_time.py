from collections import defaultdict
from queue import PriorityQueue
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # return self.bruteForce(times, n, k)
        # return self.dijkstra(times, n, k)
        return self.dfsHelper(times, n, k)
    
    def bruteForce(self, times, n, k):
        adjList = {i: [] for i in range(n)}
        travelTimes = [math.inf for _ in range(n)]
        travelTimes[k - 1] = 0

        for i in range(len(times)): adjList[times[i][0] - 1].append((times[i][1] - 1, times[i][2]))
        print(adjList)

        for i in range(n):
            if i == k - 1: continue
            travelTimes[i] = self.bruteForceDfs(times, n, k - 1, i, adjList)
            if travelTimes[i] == math.inf: return -1

        return max(travelTimes)

    def bruteForceDfs(self, times, n, node, end, adjList):
        if node == end: return 0

        minPath = math.inf
        for i in range(len(adjList[node])):
            path = adjList[node][i][1] + self.bruteForceDfs(times, n, adjList[node][i][0], end, adjList)
            minPath = min(minPath, path)
        
        return minPath
    
    def dijkstra(self, times, n, k):
        adjList = defaultdict(list)
        for u, v, t in times: adjList[u].append((v, t))

        res, pq, visited = 0, PriorityQueue(), set()
        pq.put((0, k))

        while not pq.empty():
            time, node = pq.get()
            if node in visited: continue
            visited.add(node)
            res = max(res, time)

            for neighbour in adjList[node]:
                neighbourNode, neighbourTime = neighbour
                if neighbourNode not in visited:
                    pq.put((time + neighbourTime, neighbourNode))
        
        if len(visited) != n: return -1
        return res
    
    def dfsHelper(self, times, n, k):
        adjList = defaultdict(list)
        for u, v, t in times: adjList[u].append((v, t))

        for node in adjList.values(): node.sort(key=lambda x: x[1])
        travelTimes = [math.inf for _ in range(n + 1)]
        travelTimes[0] = 0
        
        self.bfs(times, n, travelTimes, adjList, k, 0)

        res = max(travelTimes)
        if res == math.inf: return -1

        return max(travelTimes)
    
    def dfs(self, times, n, travelTimes, adjList, node, time):
        if time >= travelTimes[node]: return
        travelTimes[node] = time

        if node not in adjList: return

        for neighbour in adjList[node]:
            neighbourNode, neighbourTime = neighbour
            self.dfs(times, n, travelTimes, adjList, neighbourNode, time + neighbourTime)
    
    def bfs(self, times, n, travelTimes, adjList, node, time):
        queue = deque([node])
        travelTimes[node] = time

        while queue:
            node = queue.popleft()
            if node not in adjList: continue

            for neighbour in adjList[node]:
                neighbourNode, neighbourTime = neighbour
                arrivalTime = travelTimes[node] + neighbourTime

                if travelTimes[neighbourNode] > arrivalTime:
                    travelTimes[neighbourNode] = arrivalTime
                    queue.append(neighbourNode)