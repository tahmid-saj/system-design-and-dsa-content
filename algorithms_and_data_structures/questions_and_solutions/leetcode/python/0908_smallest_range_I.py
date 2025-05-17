class Solution:
    def smallestRangeI(self, nums: List[int], k: int) -> int:
        return max(0, (max(nums) - k) - (min(nums) + k))