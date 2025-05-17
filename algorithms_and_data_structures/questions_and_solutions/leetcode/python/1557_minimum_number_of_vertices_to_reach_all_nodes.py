class Solution:
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        inDegrees, res = set(), []

        for u, v in edges: inDegrees.add(v)

        for node in range(n):
            if node not in inDegrees: res.append(node)
        
        return res