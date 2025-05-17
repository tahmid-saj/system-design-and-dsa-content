class Solution:
    def maxNumberOfApples(self, weight: List[int]) -> int:
        weight.sort()
        res, basket = 0, 5000
        for w in weight:
            basket -= w
            if basket < 0: break
            res += 1
        return res