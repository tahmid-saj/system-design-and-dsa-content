class Solution:
    def numberOfPaths(self, n: int, corridors: List[List[int]]) -> int:
        # return self.manual(n, corridors)
        return self.intersection(n, corridors)
    
    def manual(self, n, corridors):
        adjList = defaultdict(set)
        for u, v in corridors: 
            adjList[u].add(v)
            adjList[v].add(u)

        res = set()
        for u, v in corridors:
            for node, neighbours in adjList.items():
                if u in neighbours and v in neighbours:
                    res.add(tuple(sorted([u, v, node])))
        
        return len(res)
    
    def intersection(self, n, corridors):
        neighbours = defaultdict(set)
        cycles = 0

        for room1, room2 in corridors:
            neighbours[room1].add(room2)
            neighbours[room2].add(room1)
            cycles += len(neighbours[room1].intersection(neighbours[room2]))

        return cycles