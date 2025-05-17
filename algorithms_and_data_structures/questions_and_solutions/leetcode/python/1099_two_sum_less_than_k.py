class Solution:
    def twoSumLessThanK(self, nums: List[int], k: int) -> int:
        nums.sort()

        res = -1
        for i in range(len(nums) - 1):
            j = bisect_left(nums, k - nums[i], i + 1) - 1
            if j > i: res = max(res, nums[i] + nums[j])
        return res