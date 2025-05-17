class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        return self.topologicalBFS(numCourses, prerequisites)

    def topologicalBFS(self, numCourses, prerequisites):
        if numCourses == 0: return []

        adjList = {numCourse: [] for numCourse in range(numCourses)}
        inDegrees = {numCourse: 0 for numCourse in range(numCourses)}

        for u, v in prerequisites:
            adjList[v].append(u)
            inDegrees[u] += 1
        
        queue = deque()
        for node in inDegrees:
            if inDegrees[node] == 0: queue.append(node)
        
        res = []
        while queue:
            node = queue.popleft()
            res.append(node)

            for neighbor in adjList[node]:
                inDegrees[neighbor] -= 1
                if inDegrees[neighbor] == 0: queue.append(neighbor)
        
        if len(res) != numCourses: return []
        return res