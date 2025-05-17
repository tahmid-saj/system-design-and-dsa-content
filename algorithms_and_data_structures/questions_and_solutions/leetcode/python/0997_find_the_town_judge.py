class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        if len(trust) == 0 and n == 1: return 1
        if len(trust) == 0: return -1
        adjList = defaultdict(set)
        for u, v in trust: adjList[u].add(v)

        judge = -1
        for i in range(1, n + 1):
            if i not in adjList:
                judge = i
        
        if judge == -1: return judge
        
        for u in adjList:
            if judge not in adjList[u]: return -1
        
        return judge