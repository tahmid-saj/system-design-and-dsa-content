class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            middle = l + (r - l) // 2

            if nums[middle] == target: return middle
            elif nums[middle] < target: l = middle + 1
            else: r = middle - 1
        
        return -1