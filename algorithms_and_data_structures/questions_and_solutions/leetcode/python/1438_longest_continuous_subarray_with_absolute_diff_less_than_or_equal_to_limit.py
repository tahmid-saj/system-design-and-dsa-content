from collections import deque

class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        # loop through nums keeping track of the current min and max using a sliding window
        # keep track of maxLength
        # while max - min > limit: start += 1
        start, res = 0, -math.inf
        freq = {}

        for end in range(0, len(nums)):
            freq[nums[end]] = freq.get(nums[end], 0) + 1

            while max(freq.keys()) - min(freq.keys()) > limit:
                if freq[nums[start]] == 1: freq.pop(nums[start])
                elif freq[nums[start]] > 1: freq[nums[start]] -= 1
                start += 1
            
            res = max(res, end - start + 1)
        
        return res