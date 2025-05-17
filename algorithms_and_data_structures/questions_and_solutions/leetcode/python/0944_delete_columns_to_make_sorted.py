class Solution:
    def minDeletionSize(self, strs: List[str]) -> int:
        res = 0
        for j in range(len(strs[0])):
            prev = 0
            for i in range(len(strs)):
                if ord(strs[i][j]) < prev:
                    res += 1
                    break
                prev = ord(strs[i][j])
        
        return res