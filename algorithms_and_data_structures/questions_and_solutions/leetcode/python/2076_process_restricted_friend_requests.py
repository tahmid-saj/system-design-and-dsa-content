class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.size = [0 for i in range(n)]
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return iSet, jSet, False

        if self.size[iSet] < self.size[jSet]: self.parent[iSet] = jSet
        elif self.size[iSet] > self.size[jSet]: self.parent[jSet] = iSet
        else:
            self.size[jSet] += 1
            self.parent[iSet] = jSet
            return iSet, jSet, True
        
        return iSet, jSet, False

    def unUnion(self, i, iSet, j, jSet, decSize):
        self.parent[i] = iSet
        self.parent[iSet] = iSet
        self.parent[j] = jSet
        self.parent[jSet] = jSet
        if decSize: self.size[jSet] -= 1

class Solution:
    def friendRequests(self, n: int, restrictions: List[List[int]], requests: List[List[int]]) -> List[bool]:
        dsu = DSU(n)
        res = []
        for request in requests:
            iSet, jSet, decSize = dsu.union(request[0], request[1])
            restrict = False
            for restriction in restrictions:
                if dsu.parent[restriction[0]] == dsu.parent[restriction[1]]: 
                    res.append(False)
                    restrict = True
                    dsu.unUnion(request[0], iSet, request[1], jSet, decSize)
                    break
            if restrict == False: res.append(True)
        
        return res