class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        if len(nums) == 1: return nums[0]

        max1, max2, max3 = None, None, None

        for i in range(0, len(nums)):
            if nums[i] == max1 or nums[i] == max2 or nums[i] == max3: continue

            if max1 == None or nums[i] > max1:
                max3 = max2
                max2 = max1
                max1 = nums[i]
            elif max2 == None or nums[i] > max2:
                max3 = max2
                max2 = nums[i]
            elif max3 == None or nums[i] > max3:
                max3 = nums[i]

        return max3 if max3 != None else max1