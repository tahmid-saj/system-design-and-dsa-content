class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # traverse from right to left using i (len(nums), -1, -1) looking for a decrease, if no decrease is found, return the reverse of nums
        # if a decrease is found, find the next largest element going to the right, swap them
        # reverse the digits from that point towards right right
        if len(nums) == 1: return
        dec = None
        for i in range(len(nums) - 1, 0, -1):
            if nums[i - 1] < nums[i]:
                dec = i - 1
                break
        if dec == None: return nums.reverse()
        
        diff = [0, math.inf]
        for i in range(dec + 1, len(nums)):
            if diff[1] > nums[i] - nums[dec] and nums[i] > nums[dec]:
                diff = [i, nums[i] - nums[dec]]

        nums[dec], nums[diff[0]] = nums[diff[0]], nums[dec]
        rev = nums[dec + 1::]
        rev.reverse()
        l1 = nums[:dec + 1]

        return l1 + rev