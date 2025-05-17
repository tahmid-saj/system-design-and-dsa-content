class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # binary search over solution space
        l, r = 1, max(piles)
        while l < r:
            k = l + (r - l) // 2

            hrs = 0
            for pile in piles: hrs += math.ceil(pile / k)
            if hrs <= h: r = k
            else: l = k + 1
        
        return l