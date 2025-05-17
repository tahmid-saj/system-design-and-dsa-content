class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        maxSum = currSum = sum(nums[:k])

        for i in range(1, len(nums) - k + 1):
            currSum = currSum - nums[i - 1] + nums[i + k - 1]
            maxSum = max(maxSum, currSum)
        
        return maxSum / k