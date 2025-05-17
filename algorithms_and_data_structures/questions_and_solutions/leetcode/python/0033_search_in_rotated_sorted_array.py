class Solution:
    def search(self, nums: List[int], target: int) -> int:
        return self.oneBinarySearch(nums, target)
    
    def oneBinarySearch(self, nums, target):
        l, r = 0, len(nums) - 1

        while l <= r:
            middle = l + (r - l) // 2
            if nums[middle] == target: return middle
            # left side
            if nums[middle] >= nums[l]:
                if target >= nums[l] and target < nums[middle]: r = middle - 1
                else: l = middle + 1
            # right side
            else:
                if target > nums[middle] and target <= nums[r]: l = middle + 1
                else: r = middle - 1
        
        return -1