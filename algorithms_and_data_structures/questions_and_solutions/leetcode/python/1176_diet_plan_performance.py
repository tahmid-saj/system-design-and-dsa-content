class Solution:
    def dietPlanPerformance(self, calories: List[int], k: int, lower: int, upper: int) -> int:
        start, t, res = 0, 0, 0
        for end in range(0, len(calories)):
            t += calories[end]

            while end - start + 1 > k:
                t -= calories[start]
                start += 1
            
            if end - start + 1 == k and t < lower: res -= 1
            elif end - start + 1 == k and t > upper: res += 1
        return res