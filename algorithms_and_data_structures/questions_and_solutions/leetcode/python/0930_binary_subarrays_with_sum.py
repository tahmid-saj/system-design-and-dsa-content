class Solution:
    def numSubarraysWithSum(self, nums: List[int], goal: int) -> int:
        currSum, seenSum, res = 0, defaultdict(int), 0

        for i in range(len(nums)):
            currSum += nums[i]

            if currSum == goal: res += 1
            if (currSum - goal) in seenSum: res += seenSum[currSum - goal]
            seenSum[currSum] += 1
        
        return res