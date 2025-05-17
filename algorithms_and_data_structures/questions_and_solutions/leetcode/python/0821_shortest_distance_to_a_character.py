class Solution:
    def shortestToChar(self, s: str, c: str) -> List[int]:
        # return self.distances(s, c)
        return self.minArray(s, c)

    def distances(self, s, c):
        index, res, j = [i for i in range(len(s)) if s[i] == c], [], 0
        for i in range(len(s)):
            dist1 = abs(i - index[j])
            dist2 = abs(i - index[j + 1]) if j + 1 < len(index) else math.inf
            if dist1 <= dist2: res.append(dist1)
            else:
                res.append(dist2)
                j += 1
        return res
    
    def minArray(self, s, c):
        prev = -math.inf
        res = []
        for i, x in enumerate(s):
            if x == c: prev = i
            res.append(i - prev)

        prev = math.inf
        for i in range(len(s) - 1, -1, -1):
            if s[i] == c: prev = i
            res[i] = min(res[i], prev - i)

        return res