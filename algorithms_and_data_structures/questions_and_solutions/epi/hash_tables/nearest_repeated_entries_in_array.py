import math
class Solution:
    def nearestRepeatedEntriesArray(self, words):
        seen, res = {}, math.inf
        for i in range(len(words)):
            if words[i] in seen:
                res = min(res, i - seen[words[i]])
            seen[words[i]] = i
        
        return res