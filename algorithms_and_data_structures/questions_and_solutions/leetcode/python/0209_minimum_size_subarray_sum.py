class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        res, start, currSum = math.inf, 0, 0

        for end in range(len(nums)):
            currSum += nums[end]

            while currSum >= target:
                res = min(res, end - start + 1)
                currSum -= nums[start]
                start += 1
        
        if res == math.inf: return 0
        return res