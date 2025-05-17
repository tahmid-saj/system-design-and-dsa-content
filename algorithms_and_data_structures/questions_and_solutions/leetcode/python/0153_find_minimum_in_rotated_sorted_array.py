class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r, res = 0, len(nums) - 1, nums[0]

        while l <= r:
            middle = l + (r - l) // 2
            if middle > 0 and nums[middle - 1] > nums[middle]: res = min(res, nums[middle])
            if middle < len(nums) - 1 and nums[middle] > nums[middle + 1]: res = min(res, nums[middle + 1])

            if nums[l] < nums[middle] and nums[middle] > nums[r]: l = middle + 1
            else: r = middle - 1
        
        return res