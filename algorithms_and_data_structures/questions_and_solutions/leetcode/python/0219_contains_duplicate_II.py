class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        index = {}
        for i in range(len(nums)):
            if nums[i] in index and abs(i - index[nums[i]]) <= k: return True
            index[nums[i]] = i
        return False