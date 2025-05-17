class Solution:
    def isMajorityElement(self, nums: List[int], target: int) -> bool:
        if len(nums) == 1: return False
        l, r, start, end = 0, len(nums) - 1, -1, -1

        while l <= r:
            middle = l + (r - l) // 2
            if nums[middle] == target:
                if middle == 0 or (middle > 0 and nums[middle - 1] < nums[middle]): 
                    start = middle
                    break
            if nums[middle] < target: l = middle + 1
            else: r = middle - 1
        
        l, r = 0, len(nums) - 1
        while l <= r:
            middle = l + (r - l) // 2
            if nums[middle] == target:
                if middle == len(nums) - 1 or (middle < len(nums) - 1 and nums[middle] < nums[middle + 1]): 
                    end = middle
                    break
            if nums[middle] > target: r = middle - 1
            else: l = middle + 1
        
        return (end - start + 1) > len(nums) // 2