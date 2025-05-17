class DSU:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
    
    def find(self, i):
        if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        iSet, jSet = self.find(i), self.find(j)
        if iSet == jSet: return
        self.parent[jSet] = iSet

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        dsu = DSU(len(accounts))

        # emailParent = {}
        # loop through accounts using i:
        # loop through email in accounts[i][1:]:
        #   if email in emailParent:
        #       if account[0] != accounts[emailParent[email]][0]: return
        #       union(emailParent[email], i)
        #   emailParent[email] = i
        # merged = defaultdict(list)
        # loop through emailParent.items() using k, v:
        #   merged[dsu.find(v)].append(k)
        # res = []
        # for k, v in merged.items():
        #   res.append([accounts[k][0]] + sorted(v))
        emailSeen = {}
        for i in range(len(accounts)):
            emails = accounts[i][1:]
            for email in emails:
                if email in emailSeen:
                    if accounts[i][0] != accounts[emailSeen[email]][0]: return
                    dsu.union(emailSeen[email], i)
                emailSeen[email] = i
        
        merged = defaultdict(list)
        for k, v in emailSeen.items(): merged[dsu.find(v)].append(k)

        res = []
        for k, v in merged.items(): res.append([accounts[k][0]] + sorted(v))

        return res