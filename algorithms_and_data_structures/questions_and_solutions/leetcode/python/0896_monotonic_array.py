class Solution:
    def isMonotonic(self, nums: List[int]) -> bool:
        incDec = None
        for i in range(1, len(nums)):
            if incDec == None and nums[i] < nums[i - 1]: incDec = False
            elif incDec == None and nums[i] > nums[i - 1]: incDec = True

            if incDec == True and nums[i] < nums[i - 1]: return False
            elif incDec == False and nums[i] > nums[i - 1]: return False
        return True