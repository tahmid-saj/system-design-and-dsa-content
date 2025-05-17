class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # return self.dfsStack(n, edges)

        if len(edges) != n - 1: return False
        adjList = defaultdict(list)
        visited = set()

        for u, v in edges: 
            adjList[u].append(v)
            adjList[v].append(u)

        self.dfs(n, edges, adjList, visited, 0)
        print(visited)
        if len(visited) == n: 
            return True
        return False
    
    def dfsStack(self, n, edges):
        if len(edges) != n - 1: return False
        adjList = defaultdict(list)
        visited = set()

        for u, v in edges: 
            adjList[u].append(v)
            adjList[v].append(u)

        stk = [0]
        visited.add(0)

        while stk:
            node = stk.pop()
            
            for neighbour in adjList[node]:
                if neighbour in visited: continue
                else:
                    visited.add(neighbour)
                    stk.append(neighbour)
        
        if len(visited) == n: return True
        return False
    
    def dfs(self, n, edges, adjList, visited, node):
        visited.add(node)

        for neighbour in adjList[node]:
            if neighbour not in visited: self.dfs(n, edges, adjList, visited, neighbour)