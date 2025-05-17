class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        lastOccurence = {}
        for i in range(len(s)): lastOccurence[s[i]] = i

        end, prev, res = -math.inf, 0, []
        for i in range(len(s)):
            if lastOccurence[s[i]] > end: end = lastOccurence[s[i]]
            if i == end: 
                res.append(end - prev + 1)
                prev = end + 1
        
        return res