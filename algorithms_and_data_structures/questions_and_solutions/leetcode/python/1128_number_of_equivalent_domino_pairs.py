class Solution:
    def numEquivDominoPairs(self, dominoes: List[List[int]]) -> int:
        res, seen = 0, {}
        for domino in dominoes:
            domino = tuple(sorted(domino))
            if domino not in seen: seen[domino] = 1
            else: seen[domino] += 1
            
        for k, v in seen.items(): res += v * (v - 1) // 2
        return res