class Solution:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        seenSum, currSum, res = {0: 1}, 0, 0

        for i in range(len(nums)):
            currSum += nums[i]
            rem = currSum % k
            
            res += seenSum.get(rem, 0)
            seenSum[rem] = seenSum.get(rem, 0) + 1
        
        return res