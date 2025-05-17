class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        # return self.stack(n, edges, source, destination)
        return self.helper(n, edges, source, destination)

    def stack(self, n, edges, start, end):
        adjList = [[] for _ in range(n)]
        visited = [False for _ in range(n)]

        for u, v in edges:
            adjList[u].append(v)
            adjList[v].append(u)
        
        stk = [start]
        visited[start] = True

        while stk:
            node = stk.pop()
            if node == end: return True

            for neighbor in adjList[node]:
                if visited[neighbor] == False:
                    visited[neighbor] = True
                    stk.append(neighbor)
        
        return False
    
    def helper(self, n, edges, start, end):
        adjList = defaultdict(list)
        visited = set()

        for u, v in edges:
            adjList[u].append(v)
            adjList[v].append(u)
        
        return self.dfs(n, edges, start, end, adjList, visited)
    
    def dfs(self, n, edges, node, end, adjList, visited):
        if node == end: return True
        visited.add(node)

        for neighbor in adjList[node]:
            if neighbor not in visited and self.dfs(n, edges, neighbor, end, adjList, visited): return True

        return False