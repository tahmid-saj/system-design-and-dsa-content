class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        l, r = 0, len(nums) - 1
        while l <= r:
            middle = l + (r - l) // 2
            if nums[middle] == target: return True

            if nums[l] == nums[r] and nums[middle] == nums[l]:
                l += 1
                r -= 1
            # left side
            elif nums[l] <= nums[middle]:
                if nums[l] <= target and target < nums[middle]: r = middle - 1
                else: l = middle + 1
            # right side
            else:
                if nums[middle] < target and target <= nums[r]: l = middle + 1
                else: r = middle - 1
        
        return False