class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        res = [-1, -1]

        l, r = 0, len(nums) - 1
        # lower bound
        while l <= r:
            middle = l + (r - l) // 2
            if nums[middle] == target and (middle == 0 or (middle > 0 and nums[middle - 1] < nums[middle])):
                res[0] = middle
                break
            elif nums[middle] < target: l = middle + 1
            else: r = middle - 1
        if res[0] == -1: return [-1, -1]

        l, r = res[0], len(nums) - 1
        while l <= r:
            middle = l + (r - l) // 2
            if nums[middle] == target and (middle == len(nums) - 1 or (middle < len(nums) - 1 and nums[middle] < nums[middle + 1])):
                res[1] = middle
                break
            elif nums[middle] > target: r = middle - 1
            else: l = middle + 1
        
        return res