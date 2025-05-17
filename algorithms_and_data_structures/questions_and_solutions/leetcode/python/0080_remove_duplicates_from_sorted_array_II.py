class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # return self.poppingElements(nums)
        return self.usingCounter2(nums)
    
    def poppingElements(self, nums):
        i, count = 1, 1

        while i < len(nums):
            if nums[i] == nums[i - 1]:
                count += 1
                if count > 2:
                    nums.pop(i)
                    i -= 1
            else:
                count = 1
            i += 1
        
        return len(nums)

    def usingCounter(self, nums):
        if len(nums) <= 2: return len(nums)
        
        i, j, count = 0, 1, 1
        while j < len(nums):
            if nums[i] == nums[j]: count += 1
            else: count = 1

            if count < 3:
                nums[i + 1], nums[j] = nums[j], nums[i + 1]
                i += 1
            elif count == 3 and nums[i] != nums[j]:
                nums[i + 1], nums[j] = nums[j], nums[i + 1]
                i += 1
                count = 1
            j += 1
        
        return i + 1
    
    def usingCounter2(self, nums):
        i, j, count = 1, 1, 1

        while j < len(nums):
            if nums[j] == nums[j - 1]: count += 1
            else: count = 1

            if count <= 2:
                nums[i] = nums[j]
                i += 1
            j += 1
        
        return i