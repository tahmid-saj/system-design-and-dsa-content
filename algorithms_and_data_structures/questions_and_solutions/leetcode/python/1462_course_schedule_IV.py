class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        if numCourses <= 0: return [False for _ in range(len(queries))]
        if len(prerequisites) == 0: return [False for _ in range(len(queries))]
        # perform bfs on graph and create a reacheable[i][j] matrix
        self.adjList = defaultdict(list)

        # self.reacheable = [[False for j in range(numCourses)] for i in range(numCourses)]
        self.reacheable = defaultdict(set)
        for u, v in prerequisites: 
            self.adjList[u].append(v)
            self.reacheable[u].add(v)

        for i in range(numCourses): self.bfs(numCourses, i, i)

        res = []
        for query in queries: 
            if query[1] in self.reacheable[query[0]]: res.append(True)
            else: res.append(False)
        return res
    
    @lru_cache(None)
    def bfs(self, numCourses, i, j):
        if j == numCourses: return

        for neighbour in self.adjList[j]:
            self.reacheable[i].add(neighbour)
            if j != i: self.reacheable[j].add(neighbour)
            if len(self.adjList[neighbour]) != 0: self.bfs(numCourses, i, neighbour)