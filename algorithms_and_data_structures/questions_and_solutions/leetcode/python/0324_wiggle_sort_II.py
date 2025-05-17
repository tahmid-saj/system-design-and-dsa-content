class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        countArray = [0 for _ in range(max(nums) + 1)]
        outputArray = [0 for _ in range(len(nums))]

        for num in nums: countArray[num] += 1
        for i in range(1, len(countArray)): countArray[i] += countArray[i - 1]
        for i in range(len(nums)):
            outputArray[countArray[nums[i]] - 1] = nums[i]
            countArray[nums[i]] -= 1
        
        # odd indices
        j, i = 1, len(outputArray) - 1
        while i >= 0:
            if j < len(nums): 
                nums[j] = outputArray[i]
                j += 2
                i -= 1
            else: break
        
        # even indices
        j = 0
        while i >= 0:
            if j < len(nums):
                nums[j] = outputArray[i]
                j += 2
                i -= 1
            else: break