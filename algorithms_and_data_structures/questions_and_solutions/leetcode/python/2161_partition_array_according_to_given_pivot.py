class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        return self.extraSpace(nums, pivot)
    
    def extraSpace(self, nums, pivot):
        smaller, pivots, larger = [], 0, []
        for i in range(len(nums)):
            if nums[i] < pivot: smaller.append(nums[i])
            elif nums[i] == pivot: pivots += 1
            elif nums[i] > pivot: larger.append(nums[i])
        
        return smaller + [pivot] * pivots + larger