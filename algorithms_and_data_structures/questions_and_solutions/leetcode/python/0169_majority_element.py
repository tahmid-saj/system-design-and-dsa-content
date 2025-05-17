class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # return self.sorting(nums)
        return self.greedy(nums)
    
    def sorting(self, nums):
        nums.sort()
        if len(nums) == 1: return nums[0]

        currNum, countNum = nums[0], 0
        for i in range(0, len(nums)):
            if currNum != nums[i]:
                currNum = nums[i]
                countNum = 1
            else: countNum += 1

            if countNum > len(nums) // 2: return currNum

        return currNum
    
    def greedy(self, nums):
        count = 0
        for num in nums:
            if count == 0:
                candidate = num
                count += 1
            elif candidate == num: count += 1
            else: count -= 1
        return candidate