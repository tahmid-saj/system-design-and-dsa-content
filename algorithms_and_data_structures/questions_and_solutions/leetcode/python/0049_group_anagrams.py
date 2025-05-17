class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # return self.sortedTuple(strs)
        return self.hashingByCount(strs)
    
    def sortedTuple(self, strs):
        res = defaultdict(list)
        for i in range(len(strs)): res[tuple(sorted(strs[i]))].append(strs[i])

        return res.values()
    
    def hashingByCount(self, strs):
        res = defaultdict(list)
        for i in range(len(strs)):
            counts = [0 for _ in range(26)]
            for j in range(len(strs[i])): counts[ord(strs[i][j]) - ord('a')] += 1
            res[tuple(counts)].append(strs[i])
        
        return res.values()