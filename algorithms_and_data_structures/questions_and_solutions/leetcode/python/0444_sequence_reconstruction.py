class Solution:
    def sequenceReconstruction(self, nums: List[int], sequences: List[List[int]]) -> bool:
        if len(nums) == 1 and len(sequences) == 1 and len(sequences[0]) == 1: return True

        inEdges = defaultdict(int)
        adjList = defaultdict(list)

        for edges in sequences:
            u = 0
            for v in range(1, len(edges)):
                inEdges[edges[v]] += 1
                adjList[edges[u]].append(edges[v])
                u += 1
        
        sources = deque()
        for v in adjList:
            if inEdges[v] == 0 or v not in inEdges: sources.append(v)
        
        res = []
        while sources:
            if len(sources) > 1: return False
            if nums[len(res)] != sources[0]: return False
            v = sources.popleft()
            res.append(v)
            for child in adjList[v]:
                inEdges[child] -= 1
                if inEdges[child] == 0 or v not in inEdges: sources.append(child)
        
        if res != nums: return False
        return True