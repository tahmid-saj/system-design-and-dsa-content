from collections import defaultdict, deque
class Solution:
    def buildOrder(self, projects, dependencies):
        res = []
        if len(projects) == 0: return res

        inEdges = {project: 0 for project in projects}
        adjList = defaultdict(list)

        for u, v in dependencies:
            adjList[u].append(v)
            inEdges[v] += 1
        
        queue = deque()
        for node in inEdges:
            if inEdges[node] == 0:
                queue.append(node)
                inEdges[node] -= 1
        
        while queue:
            node = queue.popleft()
            res.append(node)
            for neighbour in adjList[node]:
                inEdges[neighbour] -= 1
                if inEdges[neighbour] == 0: queue.append(neighbour)
        
        if len(res) != len(projects): return False
        return res